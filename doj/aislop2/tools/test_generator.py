"""Determinism, range, and frozen-file safety checks for benchmark generation."""

import hashlib
import json
from pathlib import Path
import tempfile
import unittest

try:
    from . import generate_cases as generator
except ImportError:
    import generate_cases as generator


class GeneratorTests(unittest.TestCase):
    def test_ranges_coverage_and_determinism(self):
        configs = generator.configurations()
        self.assertEqual(len(configs), 320)
        self.assertEqual(configs, generator.configurations())
        self.assertEqual(len({item["seed"] for item in configs}), 320)
        self.assertEqual({item["family"] for item in configs[:20]}, set(generator.FAMILIES))
        for name, expected in (("n", set(range(3, 31))), ("d", {2, 3}),
                               ("c", set(range(2, 7)))):
            self.assertEqual({item[name] for item in configs}, expected)
        self.assertEqual(min(item["k"] for item in configs), 1)
        self.assertEqual(max(item["k"] for item in configs), 180)
        for config in configs:
            case = generator.make_case(config)
            self.assertEqual(generator.serialize_case(case),
                             generator.serialize_case(generator.make_case(config)))
            n, d, c, k = (case[key] for key in ("n", "d", "c", "k"))
            self.assertTrue(3 <= n <= 30 and d in (2, 3) and d <= n)
            self.assertTrue(2 <= c <= 6 and 1 <= k <= 180)
            for key, size in (("a", n), ("t", n), ("s", d)):
                self.assertEqual(len(case[key]), size)
                for row in case[key]:
                    self.assertEqual(len(row), size)
                    self.assertTrue(all(type(value) is int and 0 <= value < c for value in row))
            self.assertEqual(len(generator.serialize_case(case).split()), 4 + 2 * n * n + d * d)
            if case["witness"] is not None:
                self.assertTrue(1 <= len(case["witness"]) <= k)
                self.assertTrue(all(0 <= x <= n-d and 0 <= y <= n-d and 0 <= r <= 3
                                    for x, y, r in case["witness"]))

    def test_manifest_freeze_and_suite_counts(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "cases"
            first = generator.write_outputs(output)
            self.assertEqual(first["written_files"], 321)
            before = {path: (path.read_bytes(), path.stat().st_mtime_ns)
                      for path in output.rglob("*") if path.is_file()}
            self.assertEqual(generator.write_outputs(output)["written_files"], 0)
            self.assertEqual(before, {path: (path.read_bytes(), path.stat().st_mtime_ns)
                                     for path in before})
            manifest = json.loads((output / "manifest.json").read_text())
            self.assertEqual(manifest["version"], 1)
            for suite, count in generator.SUITE_COUNTS.items():
                self.assertEqual(sum(suite in case["suites"] for case in manifest["cases"]), count)
            for case in manifest["cases"]:
                content = Path(case["path"]).read_bytes()
                self.assertEqual(hashlib.sha256(content).hexdigest(), case["sha256"])
            damaged = output / "generated" / "case_000.in"
            damaged.write_bytes(b"intentionally changed\n")
            with self.assertRaises(FileExistsError):
                generator.write_outputs(output)
            self.assertEqual(damaged.read_bytes(), b"intentionally changed\n")
            self.assertEqual(generator.write_outputs(output, overwrite=True)["written_files"], 1)

    def test_reachable_against_canonical_simulator(self):
        try:
            try:
                from .simulate import Instance, simulate
            except ImportError:
                from simulate import Instance, simulate
        except ImportError:
            self.skipTest("canonical simulator is not available yet")
        for config in generator.configurations():
            if config["family"] != "reachable":
                continue
            case = generator.make_case(config)
            arrays = {key: [value for row in case[key] for value in row]
                      for key in ("a", "t", "s")}
            instance = Instance(case["n"], case["d"], case["c"], case["k"],
                                arrays["a"], arrays["t"], arrays["s"])
            grid, _ = simulate(instance, case["witness"])
            self.assertEqual(grid, arrays["t"])


if __name__ == "__main__":
    unittest.main()
