"""Canonical oracles for exact temporal insertion and deletion deltas."""
import importlib.util
from pathlib import Path
import random
import unittest
from tools.simulate import Instance, simulate, match_count

ROOT = Path(__file__).resolve().parents[1]


def load():
    spec = importlib.util.spec_from_file_location('temporal', ROOT/'solvers/experiments/temporal_insert.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TemporalTests(unittest.TestCase):
    def test_cancellation_preserves_grid_and_stamp(self):
        solver=load()
        rng=random.Random(251068)
        for d in (2,3):
            for _ in range(20):
                n,c,k=d+2,6,180
                a,t,s=[[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,d*d)]
                case=Instance(n,d,c,k,a,t,s)
                seq=[(rng.randrange(n-d+1),rng.randrange(n-d+1),rng.randrange(4)) for _ in range(15)]
                for __ in range(12):
                    aid=rng.choice(seq)
                    pos=rng.randrange(len(seq)+1)
                    seq[pos:pos]=[aid,aid]
                compact=solver.cancel_inverse_pairs(seq)
                self.assertEqual(simulate(case,seq),simulate(case,compact))
                self.assertLess(len(compact),len(seq))

    def test_all_insertion_boundaries_match_exhaustive_oracle(self):
        solver = load()
        rng = random.Random(531179)
        for d in (2, 3):
            for _ in range(12):
                n, c, k = d+1, rng.randrange(2, 7), 5
                a, t, s = [[rng.randrange(c) for _ in range(size)] for size in (n*n, n*n, d*d)]
                case = Instance(n,d,c,k,a,t,s)
                indices, _, ops, _, _ = solver.build(n,d,t)
                actions = list(zip(indices,ops))
                seq = [rng.randrange(len(ops)) for _ in range(3)]
                base = match_count(case,simulate(case,[ops[i] for i in seq])[0])
                gain, pos, aid = solver.best_insertion(n,d,a+s,t,actions,seq,17)
                oracle = max(match_count(case,simulate(case,[ops[i] for i in seq[:p]+[j]+seq[p:]])[0])-base
                             for p in range(4) for j in range(len(ops)))
                self.assertEqual(gain,max(0,oracle))
                if gain:
                    child=seq[:pos]+[aid]+seq[pos:]
                    self.assertEqual(match_count(case,simulate(case,[ops[i] for i in child])[0])-base,gain)
                self.assertEqual(len(seq),3)

    def test_deletion_deltas_match_canonical(self):
        solver = load()
        rng=random.Random(62959)
        for d in (2,3):
            for _ in range(16):
                n,c,k=d+2,6,7
                a,t,s=[[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,d*d)]
                case=Instance(n,d,c,k,a,t,s)
                indices,_,ops,_,_=solver.build(n,d,t)
                actions=list(zip(indices,ops))
                seq=[rng.randrange(len(ops)) for _ in range(k)]
                base=match_count(case,simulate(case,[ops[i] for i in seq])[0])
                deltas=solver.deletion_deltas(n,d,a+s,t,actions,seq)
                for pos,gain in enumerate(deltas):
                    actual=match_count(case,simulate(case,[ops[i] for i in seq[:pos]+seq[pos+1:]])[0])-base
                    self.assertEqual(gain,actual)


if __name__=='__main__':
    unittest.main()
