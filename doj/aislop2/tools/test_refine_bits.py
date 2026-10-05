"""Exact scalar/bitset backward-refinement parity."""
import random
import unittest
from tools.test_solver import load_solver, ROOT


class RefinementBitsTests(unittest.TestCase):
    def test_exact_refinement_parity(self):
        slow = load_solver(ROOT/'submissions/best_010_246874186.py')
        fast = load_solver(ROOT/'solvers/experiments/refine_bits.py')
        rng = random.Random(762811)
        for _ in range(100):
            n,d,c,k = rng.randint(3,12),rng.choice((2,3)),rng.randint(2,6),rng.randint(1,40)
            initial,target = [[rng.randrange(c) for _ in range(size)] for size in (n*n+d*d,n*n)]
            indices,_,ops,_,_ = slow.build(n,d,target)
            actions = list(zip(indices,ops))
            sequence = [rng.randrange(len(actions)) for _ in range(rng.randrange(k+1))]
            self.assertEqual(slow.refine(n,d,k,initial,target,actions,sequence[:],passes=3),
                             fast.refine(n,d,k,initial,target,actions,sequence[:],passes=3))


if __name__ == '__main__':
    unittest.main()
