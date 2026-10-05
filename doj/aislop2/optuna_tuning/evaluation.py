"""Canonical local evaluation for tuning; never modifies the main best results.

Trials use immutable source snapshots. Local checkpoints require the entire
stable suite, submission readiness, and an identical second stable run.
"""

from __future__ import annotations

import ast
from contextlib import contextmanager
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import tempfile
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
SOLVER_PATH = Path(__file__).with_name("sa_solver.py")
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.benchmark import breakdown, evaluate_case, summarize
from tools.check_submission import check_submission
from tools.simulate import parse_instance
from optuna_tuning.sa_solver import normalize_params


def load_cases(manifest: Path, suite: str, limit: int | None = None) -> list[dict]:
    """Check the whole frozen manifest before selecting or truncating a suite."""
    if limit is not None and (type(limit) is not int or limit <= 0):
        raise ValueError("Case limit must be a positive integer.")
    document = json.loads(Path(manifest).read_text(encoding="utf-8"))
    if not isinstance(document.get("cases"), list):
        raise ValueError("Manifest must contain a cases list.")
    seen_ids, seen_paths = set(), set()
    selected = []
    for meta in document["cases"]:
        required = ("id", "path", "sha256", "family", "n", "d", "c", "k", "suites")
        if not isinstance(meta, dict) or any(key not in meta for key in required):
            raise ValueError("Manifest case is missing required metadata.")
        path = (ROOT / meta["path"]).resolve()
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != meta["sha256"]:
            raise ValueError("Frozen testcase hash mismatch: " + str(path))
        if meta["id"] in seen_ids or path in seen_paths:
            raise ValueError("Duplicate testcase id or path in manifest: " + str(meta["id"]))
        seen_ids.add(meta["id"])
        seen_paths.add(path)
        instance = parse_instance(data.decode("ascii"))
        if any(meta[key] != getattr(instance, key) for key in ("n", "d", "c", "k")):
            raise ValueError("Testcase metadata disagrees with input: " + str(path))
        if not isinstance(meta["suites"], list):
            raise ValueError("Testcase suites metadata must be a list.")
        if suite in meta["suites"]:
            selected.append(dict(meta))
    expected = document.get("suite_counts", {}).get(suite)
    if expected is not None and expected != len(selected):
        raise ValueError("Manifest suite count does not match its cases.")
    if not selected:
        raise ValueError("Selected suite is empty: " + suite)
    return selected if limit is None else selected[:limit]


def export_source(params: dict, seed: int = 0, *, template_source: bytes | None = None) -> bytes:
    """Bake parameters into the self-contained solver without string substitution."""
    params = normalize_params(params)
    if type(seed) is not int or not 0 <= seed < 2**63:
        raise ValueError("Solver seed must be an integer in [0, 2**63).")
    template = SOLVER_PATH.read_bytes() if template_source is None else template_source
    tree = ast.parse(template, filename=str(SOLVER_PATH))
    replacements = {"DEFAULT_PARAMS": params, "DEFAULT_SEED": seed}
    counts = {name: 0 for name in replacements}
    for node in tree.body:
        name = None
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            name = node.target.id
        if name in replacements:
            counts[name] += 1
            node.value = ast.parse(repr(replacements[name]), mode="eval").body
    if any(count != 1 for count in counts.values()):
        raise ValueError("Solver must define DEFAULT_PARAMS and DEFAULT_SEED exactly once at top level.")
    ast.fix_missing_locations(tree)
    source = (ast.unparse(tree) + "\n").encode("utf-8")
    compile(source, "exported_solver.py", "exec")
    if len(source) > 100_000:
        raise ValueError("Exported solver exceeds the official 100,000-byte source limit.")
    return source


def evaluate_source(source: bytes, cases: list[dict], timeout: float = 4.5,
                    on_case=None) -> dict:
    """Evaluate a snapshot sequentially, permitting Optuna pruning in on_case."""
    if not isinstance(source, bytes) or not source:
        raise ValueError("Solver source must be nonempty bytes.")
    if not cases:
        raise ValueError("Cannot evaluate an empty case list.")
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("Timeout must be finite and positive.")
    started = time.perf_counter()
    rows = []
    with tempfile.TemporaryDirectory(prefix="stamp-optuna-") as directory:
        snapshot = Path(directory) / "solver.py"
        snapshot.write_bytes(source)
        for index, meta in enumerate(cases):
            row = evaluate_case(snapshot, meta, timeout)
            if row.get("stderr"):
                row.update(valid=False, score=0, error="Solver wrote debug output to stderr.")
            rows.append(row)
            if on_case is not None:
                on_case(row, index)
    fingerprints = [(row["id"], row["input_sha256"], row.get("output_sha256"), row["score"])
                    for row in rows]
    return dict(
        **summarize(rows), results=rows, breakdown=breakdown(rows),
        solver_sha256=hashlib.sha256(source).hexdigest(), python=sys.version,
        timeout_sec=timeout, jobs=1, wall_runtime_sec=time.perf_counter() - started,
        result_sha256=hashlib.sha256(json.dumps(fingerprints, separators=(",", ":")).encode()).hexdigest(),
    )


def _write_json(path: Path, document: dict) -> None:
    path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


@contextmanager
def _qualification_lock(directory: Path):
    """Advisory OS lock is released on process exit; keep its file in place."""
    lock = directory / ".qualification.lock"
    with lock.open("a+b") as stream:
        stream.seek(0, 2)
        if stream.tell() == 0:
            stream.write(b"0")
            stream.flush()
        stream.seek(0)
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise ValueError("Qualification is already running: " + str(directory)) from exc
        try:
            yield
        finally:
            stream.seek(0)
            if os.name == "nt":
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def qualify(source: bytes, manifest: Path, output_dir: Path, description: str = "Optuna candidate",
            *, timeout: float = 4.5, on_progress=None, readiness_random_count: int = 30) -> dict:
    """Promote only strict stable improvements inside this tuning run's directory.

    The caller should qualify an iterations=0 baseline first. A full stable run
    from the supplied manifest is always required; limits used during tuning
    cannot weaken this gate. Custom manifests define their own stable suite.
    Reproduction compares every output digest and score, not just the total.
    For a nonimproving candidate, passed means stable outputs are valid;
    submission readiness is required only for a promoted checkpoint.
    """
    if not isinstance(source, bytes) or not source:
        raise ValueError("Solver source must be nonempty bytes.")
    if len(source) > 100_000:
        raise ValueError("Solver exceeds the official 100,000-byte source limit.")
    if not 0 < timeout <= 5.0 or not math.isfinite(timeout):
        raise ValueError("Checkpoint timeout must be positive and at most the 5-second contest limit.")
    if type(readiness_random_count) is not int or readiness_random_count < 0:
        raise ValueError("Readiness random count must be a nonnegative integer.")
    manifest = Path(manifest).resolve()
    manifest_digest = hashlib.sha256(manifest.read_bytes()).hexdigest()
    cases = load_cases(manifest, "stable")
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    with _qualification_lock(output_dir):
        best_path = output_dir / "best.json"
        previous = json.loads(best_path.read_text(encoding="utf-8")) if best_path.exists() else None
        if previous:
            if previous["manifest_sha256"] != manifest_digest:
                raise ValueError("Cannot compare checkpoints from a changed manifest; choose a new output directory.")
            previous_source = Path(previous["checkpoint"]).read_bytes()
            if hashlib.sha256(previous_source).hexdigest() != previous["solver_sha256"]:
                raise ValueError("Previous immutable checkpoint has changed.")
        digest = hashlib.sha256(source).hexdigest()
        report_dir = output_dir / "qualifications" / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
                                                       + "_" + digest[:12] + "_" + uuid.uuid4().hex[:8])
        report_dir.mkdir(parents=True, exist_ok=False)
        candidate = report_dir / "candidate.py"
        candidate.write_bytes(source)
        benchmark = evaluate_source(source, cases, timeout, on_progress)
        benchmark.update(manifest_sha256=manifest_digest, suite="stable", solver=str(candidate))
        _write_json(report_dir / "stable.json", benchmark)
        result = dict(passed=False, promoted=False, reason="", report_dir=str(report_dir),
                      benchmark=benchmark, solver_sha256=digest, manifest_sha256=manifest_digest)

        def finish(reason, passed=False):
            result.update(reason=reason, passed=passed)
            _write_json(report_dir / "summary.json", result)
            return result

        if benchmark["invalid"]:
            return finish("Invalid or timed-out outputs on the stable suite.")
        if previous and benchmark["total_score"] <= previous["total_score"]:
            return finish("Stable score did not strictly improve.", passed=True)
        readiness = check_submission(candidate, random_count=readiness_random_count, timeout=timeout)
        result["readiness"] = readiness
        _write_json(report_dir / "readiness.json", readiness)
        if not readiness["passed"]:
            return finish("Submission readiness failed.")
        repeated = evaluate_source(source, cases, timeout, on_progress)
        repeated.update(manifest_sha256=manifest_digest, suite="stable", solver=str(candidate))
        result["reproduction"] = repeated
        _write_json(report_dir / "stable_repeat.json", repeated)
        if repeated["invalid"] or repeated["result_sha256"] != benchmark["result_sha256"]:
            return finish("Repeated stable run did not reproduce every output and score.")
        checkpoints = output_dir / "checkpoints"
        checkpoints.mkdir(exist_ok=True)
        existing_ids = [int(path.name.split("_")[1]) for path in checkpoints.glob("best_*_*.py")
                        if path.name.split("_")[1].isdigit()]
        checkpoint_id = max(existing_ids, default=-1) + 1
        suffix = "initial" if previous is None else str(benchmark["total_score"])
        checkpoint = checkpoints / f"best_{checkpoint_id:03d}_{suffix}.py"
        with checkpoint.open("xb") as stream:
            stream.write(source)
        best = dict(id=checkpoint_id, total_score=benchmark["total_score"], avg_score=benchmark["avg_score"],
                    runtime_sec=benchmark["runtime_sec"], max_runtime_sec=benchmark["max_runtime_sec"],
                    description=description, checkpoint=str(checkpoint), file=str(checkpoint),
                    solver_sha256=digest, manifest_sha256=manifest_digest,
                    report_dir=str(report_dir), python=sys.version, timeout_sec=timeout)
        history = output_dir / "history.csv"
        fields = ["id", "total_score", "avg_score", "runtime_sec", "max_runtime_sec", "description",
                  "file", "solver_sha256", "manifest_sha256", "report_dir"]
        needs_header = not history.exists() or not history.stat().st_size
        with history.open("a", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
            if needs_header:
                writer.writeheader()
            writer.writerow(best)
        temporary_best = output_dir / (".best-" + uuid.uuid4().hex + ".json")
        _write_json(temporary_best, best)
        temporary_best.replace(best_path)
        result.update(promoted=True, checkpoint=str(checkpoint), best=best)
        return finish("Saved initial checkpoint." if previous is None else "Saved strict stable score improvement.",
                      passed=True)
