import random
import unittest
from tools.test_solver import load_solver, ROOT
from tools.simulate import Instance, simulate


class PackedTests(unittest.TestCase):
    def test_one_hot_encoding_matches_three_bit_search(self):
        hot = load_solver(ROOT/'solvers/experiments/plateau_hot12.py')
        packed = load_solver(ROOT/'solvers/experiments/plateau12.py')
        rng = random.Random(71137)
        for _ in range(45):
            n,d,c,k = rng.randint(3,8),rng.choice((2,3)),rng.randint(2,6),rng.randint(1,30)
            a,t,s = [[rng.randrange(c) for _ in range(count)] for count in (n*n,n*n,d*d)]
            indices,codes,ops,coverage,patches = hot.build(n,d,t)
            code = sum(1 << (6*j+v) for j,v in enumerate(s))
            for index,positions in enumerate(indices):
                self.assertEqual((code & codes[index]).bit_count(),sum(s[j]==t[p] for j,p in enumerate(positions)))
            self.assertEqual(hot.solve(n,d,c,k,a,t,s),packed.solve(n,d,c,k,a,t,s))

    def test_packed_deltas_transitions_and_baseline(self):
        solver = load_solver(ROOT/'solvers/experiments/plateau.py')
        greedy = load_solver(ROOT/'solvers/greedy.py')
        solver.RUNS = 1
        rng = random.Random(832773)
        for _ in range(50):
            n,d,c,k = rng.randint(3,8),rng.choice((2,3)),rng.randint(2,6),rng.randint(1,20)
            a,t,s = [[rng.randrange(c) for _ in range(count)] for count in (n*n,n*n,d*d)]
            instance = Instance(n,d,c,180,a,t,s)
            indices,codes,ops,coverage,patches = solver.build(n,d,t)
            mask = sum(1<<(3*j) for j in range(d*d))
            stampcode = sum(v<<(3*j) for j,v in enumerate(s))
            for i in rng.sample(range(len(ops)), min(20,len(ops))):
                g,st = a[:],s[:]
                solver.transition(g,st,indices[i])
                self.assertEqual((g,st),simulate(instance,[ops[i]]))
                diff = codes[i] ^ stampcode
                matches = d*d-((diff | diff>>1 | diff>>2)&mask).bit_count()
                self.assertEqual(matches,sum(g[p]==t[p] for p in patches[i>>2]))
            self.assertEqual(solver.solve(n,d,c,k,a[:],t,s[:]),greedy.solve(n,d,c,k,a[:],t,s[:]))


if __name__ == '__main__':
    unittest.main()
