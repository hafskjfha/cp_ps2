"""Check a single-file solver before creating an immutable checkpoint.

Example: python tools/check_submission.py solvers/current.py --random 30 \
    --timeout 5 --output results/check_current.json

This is a conservative readiness check, not a proof of arbitrary Python code.
Suspicious file/dynamic-code calls require review and prevent an automatic pass.
Solver-specific duplicated transition logic still needs a separate differential
test against tools.simulate; this script does not import or execute solver code
inside the evaluator process.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import random
import subprocess
import sys
import tempfile
import threading
import time
import tokenize
from pathlib import Path

if __package__:
    from .compact_submission import decode_literal_wrapper
    from .simulate import Instance, format_instance, match_count, simulate
    from .validate_output import validate_output
else:
    from compact_submission import decode_literal_wrapper
    from simulate import Instance, format_instance, match_count, simulate
    from validate_output import validate_output


def inspect_source(path: Path) -> dict:
    """Return explicit static failures and conservative manual-review flags."""
    result = {"valid": False, "errors": [], "review_flags": [], "imports": []}
    errors, flags = result["errors"], result["review_flags"]
    if path.suffix.lower() != ".py" or not path.is_file():
        errors.append("The submission must be one existing .py file.")
        return result
    try:
        with tokenize.open(path) as stream:
            source = stream.read()
        tree = ast.parse(source, filename=str(path))
        compile(tree, str(path), "exec")
    except (OSError, UnicodeError, SyntaxError, ValueError, RecursionError) as exc:
        errors.append(f"Cannot read/compile submission: {exc}")
        return result
    data=path.read_bytes()
    result["sha256"] = hashlib.sha256(data).hexdigest()
    result['source_bytes']=len(data)
    if len(data)>100000:
        errors.append('Submitted source exceeds the official 100,000-byte limit.')
    # Only the exact literal codec wrapper is accepted. Decode without executing
    # it, then apply all existing import/filesystem/dynamic-execution checks to
    # the actual program. A nested wrapper is rejected by the normal exec rule.
    try:
        decoded=decode_literal_wrapper(source)
    except ValueError:
        pass
    else:
        result['packed_source']=dict(codec='lzma/latin1' if source.startswith('# coding: latin-1') else 'lzma/base85',decoded_bytes=len(decoded.encode()),
                                    decoded_sha256=hashlib.sha256(decoded.encode()).hexdigest())
        try:
            tree=ast.parse(decoded,filename=str(path)+' [decoded]')
            compile(tree,str(path)+' [decoded]','exec')
        except (SyntaxError,ValueError,RecursionError) as exc:
            errors.append(f'Cannot compile decoded source: {exc}')
            return result
    modules = set()
    sys_aliases = {"sys"}
    stdin_aliases = set()
    stdlib = set(getattr(sys, "stdlib_module_names", ()))
    stdlib.update(sys.builtin_module_names)
    stdlib.add("__future__")
    if not getattr(sys, "stdlib_module_names", None):
        errors.append("Static import checking requires Python 3.10 or later.")
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".")[0]
                modules.add(root)
                if root not in stdlib:
                    errors.append(f"Line {node.lineno}: non-standard import {alias.name!r}.")
                if alias.name == "sys":
                    sys_aliases.add(alias.asname or alias.name)
        elif isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".")[0]
            modules.add(root)
            if node.level or root not in stdlib:
                errors.append(f"Line {node.lineno}: local/non-standard import {node.module!r}.")
            if node.module == "sys" and not node.level:
                stdin_aliases.update(alias.asname or alias.name for alias in node.names if alias.name == "stdin")
    reads_stdin = False
    file_methods = {
        "open", "read_text", "read_bytes", "write_text", "write_bytes",
        "load", "loads_file", "read_pickle", "read_csv", "read_json",
    }
    dynamic_calls = {"eval", "exec", "compile", "__import__"}
    process_methods = {"system", "popen", "Popen", "run_path", "run_module", "import_module"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and node.attr == "stdin":
            if isinstance(node.value, ast.Name) and node.value.id in sys_aliases:
                reads_stdin = True
        elif isinstance(node, ast.Name) and node.id in stdin_aliases:
            reads_stdin = True
        if not isinstance(node, ast.Call):
            continue
        name = node.func.id if isinstance(node.func, ast.Name) else (
            node.func.attr if isinstance(node.func, ast.Attribute) else ""
        )
        if name == "input":
            reads_stdin = True
        descriptor_stdin = name == "open" and node.args and isinstance(node.args[0], ast.Constant) and node.args[0].value == 0
        if descriptor_stdin:
            reads_stdin = True
        elif name in file_methods:
            flags.append(f"Line {node.lineno}: potential filesystem access through {name}().")
        if name in dynamic_calls or name in process_methods:
            flags.append(f"Line {node.lineno}: dynamic/external execution through {name}().")
    if not reads_stdin:
        errors.append("No direct sys.stdin, imported stdin, input(), or open(0) access was found.")
    result.update(imports=sorted(modules), reads_stdin=reads_stdin, valid=not errors and not flags)
    return result


def make_case(n: int, d: int, c: int, k: int, seed: int, family: str = "random") -> Instance:
    rng = random.Random(seed)
    a = [rng.randrange(c) for _ in range(n * n)]
    t = [rng.randrange(c) for _ in range(n * n)]
    s = [rng.randrange(c) for _ in range(d * d)]
    if family == "close":
        t = a[:]
        for _ in range(max(1, n * n // 10)):
            t[rng.randrange(n * n)] = rng.randrange(c)
    elif family == "reachable":
        instance = Instance(n, d, c, k, a, t, s)
        operations = [(rng.randrange(n - d + 1), rng.randrange(n - d + 1), rng.randrange(4)) for _ in range(rng.randint(1, k))]
        t, _ = simulate(instance, operations)
    elif family == "pattern":
        t = [(row + col) % c for row in range(n) for col in range(n)]
        s = [rng.randrange(c)] * (d * d)
    elif family == "uniform":
        a = [rng.randrange(c)] * (n * n)
        t = a[:]
        for _ in range(max(1, n * n // 8)):
            t[rng.randrange(n * n)] = rng.randrange(c)
    return Instance(n, d, c, k, a, t, s)


def readiness_cases(random_count: int) -> list[tuple[str, Instance]]:
    cases = []
    for n, k in [(3, 1), (30, 180)]:
        for d in (2, 3):
            for c in (2, 6):
                name = f"boundary_n{n}_d{d}_c{c}_k{k}"
                cases.append((name, make_case(n, d, c, k, 891000 + 1000 * n + 10 * d + c)))
    rng = random.Random(941730)
    families = ("random", "close", "reachable", "pattern", "uniform")
    for index in range(random_count):
        n, d, c, k = rng.randint(3, 30), rng.choice((2, 3)), rng.randint(2, 6), rng.randint(1, 180)
        family = families[index % len(families)]
        cases.append((f"random_{index:03d}_{family}", make_case(n, d, c, k, rng.randrange(1 << 30), family)))
    return cases


def run_solver(path: Path, instance: Instance, timeout: float, cwd: str) -> tuple[dict, bytes]:
    """Capture bounded output, killing invalid output floods and timed-out runs."""
    started = time.perf_counter()
    row = {"valid": False, "n": instance.n, "d": instance.d, "c": instance.c, "k": instance.k}
    buffers = {"stdout": bytearray(), "stderr": bytearray()}
    overflow = []
    try:
        process = subprocess.Popen(
            [sys.executable, "-I", "-B", str(path)], cwd=cwd,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
    except OSError as exc:
        row.update(error=f"Could not launch solver: {exc}", runtime_sec=time.perf_counter() - started)
        return row, b""

    def drain(stream, key, limit):
        try:
            while True:
                chunk = stream.read(8192)
                if not chunk:
                    break
                room = limit + 1 - len(buffers[key])
                buffers[key].extend(chunk[:max(0, room)])
                if len(buffers[key]) > limit:
                    overflow.append(key)
                    try:
                        process.kill()
                    except OSError:
                        pass
                    break
        finally:
            stream.close()

    threads = [
        threading.Thread(target=drain, args=(process.stdout, "stdout", 100000), daemon=True),
        threading.Thread(target=drain, args=(process.stderr, "stderr", 8192), daemon=True),
    ]
    for thread in threads:
        thread.start()
    timed_out = False
    try:
        try:
            process.stdin.write(format_instance(instance).encode("ascii"))
            process.stdin.close()
        except (BrokenPipeError, OSError):
            pass
        process.wait(timeout=max(0.001, timeout - (time.perf_counter() - started)))
    except subprocess.TimeoutExpired:
        timed_out = True
        process.kill()
        process.wait()
    finally:
        for thread in threads:
            thread.join(timeout=2)
    output = bytes(buffers["stdout"])
    row.update(runtime_sec=time.perf_counter() - started, returncode=process.returncode,
               output_bytes=len(output), stderr=bytes(buffers["stderr"]).decode("utf-8", errors="replace")[:2048])
    if timed_out:
        row["error"] = f"Exceeded {timeout:g}-second timeout."
    elif overflow:
        row["error"] = f"Exceeded capture limit for {', '.join(overflow)}."
    elif process.returncode:
        row["error"] = f"Solver exited with code {process.returncode}."
    elif row["stderr"]:
        row["error"] = "Solver wrote to stderr; checkpoint requires no debug output."
    else:
        try:
            operations = validate_output(instance, output)
            final_grid, _ = simulate(instance, operations)
            matches = match_count(instance, final_grid)
            row.update(valid=True, operations=len(operations), matches=matches,
                       score=1_000_000 * matches // (instance.n * instance.n))
        except (ValueError, TypeError, IndexError) as exc:
            row["error"] = f"Invalid output: {exc}"
    return row, output


def check_submission(path: Path, random_count: int = 30, timeout: float = 5.0) -> dict:
    path = path.resolve()
    report = {
        "solver": str(path), "python": sys.version, "timeout_sec": timeout,
        "random_cases": random_count, "static": inspect_source(path), "cases": [],
        "transition_differential": {
            "status": "not_run", "reason": "Run solver-specific duplicated transition checks separately against tools.simulate."
        },
    }
    report["solver_sha256"] = report["static"].get("sha256", "")
    if not report["static"]["valid"]:
        report.update(valid=False, passed=False, cases_passed=0, cases_total=0, max_runtime_sec=0.0)
        return report
    cases = readiness_cases(random_count)
    solver_data = path.read_bytes()
    if hashlib.sha256(solver_data).hexdigest() != report["solver_sha256"]:
        report["static"]["errors"].append("Solver changed during its static check; retry readiness.")
        report.update(valid=False, passed=False, cases_passed=0, cases_total=0, max_runtime_sec=0.0)
        return report
    with tempfile.TemporaryDirectory(prefix="stamp-readiness-") as isolated_cwd:
        snapshot = Path(isolated_cwd) / path.name
        snapshot.write_bytes(solver_data)
        repeat_expected = None
        repeat_index = 4  # The first full-size K=180 case exercises the normal search path.
        for index, (name, instance) in enumerate(cases):
            row, output = run_solver(snapshot, instance, timeout, isolated_cwd)
            row["name"] = name
            report["cases"].append(row)
            if index == repeat_index:
                repeat_expected = output
        name, instance = cases[repeat_index]
        repeated, output = run_solver(snapshot, instance, timeout, isolated_cwd)
        report["determinism"] = {
            "case": name, "valid": repeated["valid"] and output == repeat_expected,
            "repeat_run": repeated,
        }
    rows = report["cases"]
    report.update(
        valid=all(row["valid"] for row in rows) and report["determinism"]["valid"],
        cases_passed=sum(row["valid"] for row in rows), cases_total=len(rows),
        max_runtime_sec=max(row["runtime_sec"] for row in rows + [repeated]),
        max_size_runtime_sec=max(row["runtime_sec"] for row in rows if row["n"] == 30),
        total_runtime_sec=sum(row["runtime_sec"] for row in rows + [repeated]),
    )
    report["passed"] = report["valid"]
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("solver", type=Path)
    parser.add_argument("--random", type=int, default=30, metavar="COUNT", help="additional fixed-seed random cases (default: 30)")
    parser.add_argument("--timeout", type=float, default=5.0, help="per-instance wall time limit in seconds")
    parser.add_argument("--output", type=Path, help="write the full machine-readable JSON report")
    args = parser.parse_args()
    if args.random < 0 or args.timeout <= 0:
        parser.error("--random must be nonnegative and --timeout must be positive")
    report = check_submission(args.solver, args.random, args.timeout)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    status = "PASS" if report["valid"] else "FAIL"
    print(f"{status}: {report['cases_passed']}/{report['cases_total']} cases; max {report['max_runtime_sec']:.3f}s; {args.solver}")
    for error in report["static"]["errors"] + report["static"]["review_flags"]:
        print(f"  {error}")
    for row in report["cases"]:
        if not row["valid"]:
            print(f"  {row['name']}: {row['error']}")
    if "determinism" in report and not report["determinism"]["valid"]:
        print("  Determinism check failed: repeated output differed or the repeat run was invalid.")
    print("Transition differential: separate solver-specific verification required.")
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
