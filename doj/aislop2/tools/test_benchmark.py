"""Subprocess evaluator behavior, including timeout and invalid output."""
import tempfile
import unittest
from pathlib import Path

from tools.benchmark import evaluate_case, summarize


class BenchmarkTests(unittest.TestCase):
    def test_process_validation_and_score(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            case = root / 'input.in'
            case.write_text('3 2 2 1\n' + '0 ' * 22 + '\n')
            solver = root / 'solver.py'
            meta = dict(id='sample', path=str(case), n=3, d=2, c=2, k=1, family='test')
            solver.write_text('print(0)\n')
            result = evaluate_case(solver, meta, 2, root)
            self.assertTrue(result['valid'])
            self.assertEqual(result['score'], 1000000)
            self.assertEqual(result['matches'], 9)
            solver.write_text('print("0 1")\n')
            result = evaluate_case(solver, meta, 2, root)
            self.assertFalse(result['valid'])
            self.assertEqual(result['score'], 0)
            solver.write_text('import time\ntime.sleep(1)\n')
            result = evaluate_case(solver, meta, 0.05, root)
            self.assertFalse(result['valid'])
            self.assertIn('timeout', result['error'])


if __name__ == '__main__':
    unittest.main()
