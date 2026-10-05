"""Independent canonical review of temporal edits and submission packaging.

Run directly to also save results/temporal_review.json. No benchmark is run.
"""
import ast
import base64
import hashlib
import importlib.util
import json
import lzma
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import time
import tokenize
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from tools.check_submission import inspect_source
from tools.compact_submission import compact_source, decode_literal_wrapper, pack_source
from tools.simulate import Instance, format_instance, match_count, simulate
from tools.validate_output import validate_output


SOURCE = ROOT / "solvers/experiments/algebra27_t3_r3_source.py"
PACKED = ROOT / "solvers/experiments/algebra27_t3_r3.py"
MEASUREMENTS = {}


def load_solver():
    spec = importlib.util.spec_from_file_location("temporal_review_candidate", SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CanonicalTemporalReview(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.solver = load_solver()

    def fixture(self, rng, n, d, c, budget, length):
        grid = [rng.randrange(c) for _ in range(n * n)]
        target = [rng.randrange(c) for _ in range(n * n)]
        stamp = [rng.randrange(c) for _ in range(d * d)]
        case = Instance(n, d, c, budget, grid, target, stamp)
        indices, _, operations, _, _ = self.solver.build(n, d, target)
        actions = list(zip(indices, operations))
        sequence = [rng.randrange(len(actions)) for _ in range(length)]
        return case, actions, sequence

    @staticmethod
    def score(case, actions, sequence):
        return match_count(case, simulate(case, [actions[aid][1] for aid in sequence])[0])

    def insertion_oracle(self, case, actions, sequence):
        base = self.score(case, actions, sequence)
        options = [(self.score(case, actions, sequence[:pos] + [aid] + sequence[pos:]) - base, pos, aid)
                   for pos in range(len(sequence) + 1) for aid in range(len(actions))]
        return max(0, max(item[0] for item in options))

    def test_every_boundary_insertion_matches_canonical_global_optimum(self):
        rng = random.Random(280971)
        cases = oracle_candidates = 0
        for d in (2, 3):
            for length in range(7):
                for variant in range(5):
                    n = max(3, d) + variant % 3
                    case, actions, sequence = self.fixture(rng, n, d, 2 + variant, length + 1, length)
                    initial = case.a + case.s
                    original = (initial[:], case.t[:], sequence[:])
                    gain, pos, aid = self.solver.best_insertion(n, d, initial, case.t, actions, sequence, 379 + variant)
                    oracle = self.insertion_oracle(case, actions, sequence)
                    self.assertEqual(gain, oracle)
                    if gain:
                        self.assertGreaterEqual(pos, 0)
                        self.assertLessEqual(pos, len(sequence))
                        self.assertEqual(self.score(case, actions, sequence[:pos] + [aid] + sequence[pos:])
                                         - self.score(case, actions, sequence), gain)
                    else:
                        self.assertEqual((pos, aid), (-1, -1))
                    self.assertEqual((initial, case.t, sequence), original)
                    cases += 1
                    oracle_candidates += len(actions) * (length + 1)
        MEASUREMENTS["insertion"] = dict(cases=cases, exhaustive_candidate_sequences=oracle_candidates)

    def test_deletion_and_reinsertion_gain_match_full_simulation(self):
        rng = random.Random(480651)
        checked = 0
        for d in (2, 3):
            for index in range(24):
                n, length = max(3, d) + index % 2, 1 + index % 7
                case, actions, sequence = self.fixture(rng, n, d, 2 + index % 5, length, length)
                initial = case.a + case.s
                base = self.score(case, actions, sequence)
                deltas = self.solver.deletion_deltas(n, d, initial, case.t, actions, sequence)
                self.assertEqual(len(deltas), length)
                for remove in range(length):
                    child = sequence[:remove] + sequence[remove + 1:]
                    removed = self.score(case, actions, child)
                    self.assertEqual(deltas[remove], removed - base)
                    gain, pos, aid = self.solver.best_insertion(n, d, initial, case.t, actions, child, 805 + remove)
                    oracle = self.insertion_oracle(case, actions, child)
                    self.assertEqual(gain, oracle)
                    repaired = child[:pos] + [aid] + child[pos:] if aid >= 0 else child
                    self.assertEqual(self.score(case, actions, repaired) - base, deltas[remove] + gain)
                    checked += 1
        MEASUREMENTS["deletion_reinsertion"] = dict(cases=48, checked_removals=checked)

    def test_repair_never_loses_score_or_exceeds_budget_each_round(self):
        rng = random.Random(512553)
        cases = calls = 0
        for d in (2, 3):
            for index in range(18):
                n, k = max(3, d) + index % 3, 1 + index % 9
                length = rng.randrange(k + 1)
                case, actions, sequence = self.fixture(rng, n, d, 2 + index % 5, k, length)
                base = self.score(case, actions, sequence)
                initial = case.a + case.s
                for removals in (0, 1, 3, len(sequence) + 1):
                    previous = base
                    for rounds in (0, 1, 2, 3, 5):
                        answer = self.solver.temporal_repair(n, d, k, initial, case.t, actions, sequence, rounds, removals)
                        self.assertLessEqual(len(answer), k)
                        current = self.score(case, actions, answer)
                        self.assertGreaterEqual(current, previous)
                        self.assertLessEqual(current, self.solver.color_bound(initial, case.t))
                        self.assertEqual(initial, case.a + case.s)
                        previous = current
                        calls += 1
                cases += 1
        # Large endpoints verify valid indexing/budget without an exhaustive oracle.
        for d in (2, 3):
            case, actions, sequence = self.fixture(rng, 30, d, 6, 180, 180)
            answer = self.solver.temporal_repair(30, d, 180, case.a + case.s, case.t, actions, sequence, 1, 2)
            self.assertLessEqual(len(answer), 180)
            self.assertGreaterEqual(self.score(case, actions, answer), self.score(case, actions, sequence))
            cases += 1
            calls += 1
        MEASUREMENTS["iterated_repair"] = dict(cases=cases, calls=calls, includes_maximum_n_and_k=True)

    def test_cancellation_preserves_full_stamp_state(self):
        rng = random.Random(193571)
        for index in range(48):
            d = 2 + index % 2
            case, actions, sequence = self.fixture(rng, max(3, d) + index % 4, d, 2 + index % 5, 180, 20)
            for _ in range(25):
                aid = rng.randrange(len(actions))
                position = rng.randrange(len(sequence) + 1)
                sequence[position:position] = [aid, aid]
            compact = self.solver.cancel_inverse_pairs(sequence)
            self.assertEqual(simulate(case, [actions[i][1] for i in sequence]),
                             simulate(case, [actions[i][1] for i in compact]))
            self.assertEqual(compact, self.solver.cancel_inverse_pairs(compact))
            self.assertLessEqual(len(compact), 20)
        MEASUREMENTS["cancellation"] = dict(cases=48, pairs_injected=1200)


class PackagingReview(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="temporal-pack-review-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)

    def inspect(self, source, encoding="utf8"):
        path = self.root / "solver.py"
        path.write_bytes(source.encode(encoding))
        return inspect_source(path)

    def test_current_candidate_exactly_maps_to_source(self):
        with tokenize.open(PACKED) as stream:
            decoded = decode_literal_wrapper(stream.read())
        expected = compact_source(SOURCE.read_text(encoding="utf8"))
        self.assertEqual(decoded, expected)
        report = inspect_source(PACKED)
        self.assertTrue(report["valid"], report)
        self.assertEqual(set(report["imports"]), {"math", "random", "sys"})
        self.assertLessEqual(report["source_bytes"], 100000)
        MEASUREMENTS["artifact_mapping"] = report

    def test_exact_source_byte_boundary(self):
        packed = pack_source("input()\nprint(0)\n")
        padded = packed + "#" + "x" * (100000 - len(packed.encode()) - 1)
        self.assertEqual(len(padded.encode()), 100000)
        self.assertTrue(self.inspect(padded)["valid"])
        rejected = self.inspect(padded + "x")
        self.assertFalse(rejected["valid"])
        self.assertTrue(any("100,000" in message for message in rejected["errors"]))

    def test_malformed_and_nested_packed_sources_are_rejected(self):
        good = "import sys\nsys.stdin.read()\nprint(0)\n"
        packed = pack_source(good)
        examples = [packed + "print('extra')\n", packed.replace("exec(", "eval(", 1),
                    packed.replace("import base64,lzma", "import base64,lzma,os"),
                    "import base64,lzma\nexec(lzma.decompress(base64.b85decode(input())))\n",
                    pack_source("input()\nopen('local.dat')\nprint(0)"),
                    pack_source("import local_helper\ninput()\nprint(0)"),
                    pack_source(packed),
                    pack_source("input()\nexec('print(0)')\n"),
                    pack_source("print(0)\n"),
                    pack_source("this is invalid python!\n"),
                    pack_source("x" * 1_000_001)]
        raw = lzma.compress(good.encode())
        for compressed in (raw[:-1], raw + b"trailing", raw + raw, b"invalid-compressed-stream"):
            examples.append("import base64,lzma\nexec(lzma.decompress(base64.b85decode(" + repr(base64.b85encode(compressed)) + ")))\n")
        for example in examples:
            with self.subTest(wrapper=example[:75]):
                self.assertFalse(self.inspect(example)["valid"])
        latin1 = pack_source(good, "latin1")
        self.assertTrue(self.inspect(latin1, "latin1")["valid"])
        self.assertFalse(self.inspect(latin1.replace(".encode('latin1')", ".encode('utf8')"), "latin1")["valid"])
        MEASUREMENTS["malformed_wrappers"] = dict(rejected=len(examples) + 1, valid_latin1_control=True)

    def test_deep_decoded_expression_returns_invalid_report(self):
        # Regression discovered during independent review: ast.parse used to
        # raise uncaught RecursionError rather than producing an invalid report.
        decoded = "input()\nprint(" + "+".join(["1"] * 3000) + ")\n"
        self.assertFalse(self.inspect(pack_source(decoded))["valid"])

    def test_builder_reproduces_reviewed_artifact_from_immutable_inputs(self):
        fixture_root = self.root / "fixture"
        (fixture_root / "submissions").mkdir(parents=True)
        (fixture_root / "solvers/experiments").mkdir(parents=True)
        parent = next((ROOT / "submissions").glob("best_027_*.py"))
        (fixture_root / "submissions" / parent.name).write_bytes(parent.read_bytes())
        artifact_tree = ast.parse(SOURCE.read_text())
        route_names = {"route_patterns", "route_tail"}
        temporal_names = {"cancel_inverse_pairs", "best_insertion", "deletion_deltas", "temporal_repair"}
        for name, selected in (("route_sparse_fragment.py", route_names), ("temporal_fragment.py", temporal_names)):
            # Experiment fragments evolve after a checkpoint. Snapshot the actual
            # reviewed artifact's definitions rather than assuming today's mutable
            # fragments are the historical versions used to produce checkpoint040.
            fragment = "\n\n".join(ast.unparse(node) for node in artifact_tree.body
                                    if isinstance(node, ast.FunctionDef) and node.name in selected) + "\n"
            (fixture_root / "solvers/experiments" / name).write_text(fragment, encoding="utf8")
        # The real builder is executed, changing only its ROOT for isolation.
        tree = ast.parse((ROOT / "tools/build_routing_candidate.py").read_text())
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == "ROOT" for target in node.targets):
                node.value = ast.Call(func=ast.Name(id="Path", ctx=ast.Load()), args=[ast.Constant(str(fixture_root))], keywords=[])
        ast.fix_missing_locations(tree)
        builder = self.root / "isolated_builder.py"
        builder.write_text("import sys\nsys.path.insert(0," + repr(str(ROOT)) + ")\n" + ast.unparse(tree), encoding="utf8")
        process = subprocess.run([sys.executable, "-I", "-B", str(builder), "--parent", "27", "--rounds", "3",
                                  "--temporal", "3", "--removals", "3", "--repeat", "3", "--name", "replica"],
                                 capture_output=True, timeout=15, check=True)
        self.assertFalse(process.stderr)
        replica_source = fixture_root / "solvers/experiments/replica_source.py"
        class IgnoreDocumentation(ast.NodeTransformer):
            def visit_Expr(self, node):
                return None if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str) else node
        self.assertEqual(ast.dump(IgnoreDocumentation().visit(ast.parse(replica_source.read_text()))),
                         ast.dump(IgnoreDocumentation().visit(artifact_tree)))
        replica = fixture_root / "solvers/experiments/replica.py"
        with tokenize.open(replica) as stream:
            rebuilt = decode_literal_wrapper(stream.read())
        with tokenize.open(PACKED) as stream:
            expected = decode_literal_wrapper(stream.read())
        self.assertEqual(rebuilt, expected)
        MEASUREMENTS["builder"] = dict(source_ast_reproduced=True, decoded_reproduced=True,
                                       fragments_snapshotted_from_reviewed_source=True,
                                       exact_packed_bytes_equal=replica.read_bytes() == PACKED.read_bytes(),
                                       rebuilt_bytes=replica.stat().st_size)

    def test_packed_solver_isolated_execution_matches_source(self):
        rng = random.Random(162077)
        copied = self.root / "standalone.py"
        copied.write_bytes(PACKED.read_bytes())
        rows = []
        for n, d, c, k in ((3, 2, 2, 1), (3, 3, 6, 180), (4, 3, 4, 9), (5, 2, 6, 18)):
            values = [[rng.randrange(c) for _ in range(size)] for size in (n * n, n * n, d * d)]
            case = Instance(n, d, c, k, *values)
            input_data = format_instance(case).encode()
            outputs = []
            for path in (SOURCE, copied):
                process = subprocess.run([sys.executable, "-I", "-B", str(path)], input=input_data,
                                         capture_output=True, cwd=self.root, timeout=5, check=True)
                self.assertFalse(process.stderr)
                validate_output(case, process.stdout)
                outputs.append(process.stdout)
            self.assertEqual(outputs[0], outputs[1])
            rows.append(dict(n=n, d=d, c=c, k=k, output_sha256=hashlib.sha256(outputs[0]).hexdigest()))
        MEASUREMENTS["isolated_execution"] = rows


if __name__ == "__main__":
    started = time.perf_counter()
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    report = dict(passed=result.wasSuccessful(), tests_run=result.testsRun,
                  runtime_sec=time.perf_counter() - started,
                  failures=[dict(test=str(test), traceback=trace) for test, trace in result.failures + result.errors],
                  measurements=MEASUREMENTS)
    (ROOT / "results/temporal_review.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf8")
    raise SystemExit(not result.wasSuccessful())
