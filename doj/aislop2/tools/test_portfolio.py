import random
import unittest
from tools.test_solver import load_solver, ROOT
from tools.simulate import Instance, simulate, match_count


class PortfolioTests(unittest.TestCase):
    def test_selects_actual_best_component(self):
        solver = load_solver(ROOT/'solvers/experiments/portfolio.py')
        rng = random.Random(827134)
        for _ in range(24):
            n,d,c,k = rng.randint(3,8),rng.choice((2,3)),rng.randint(2,6),rng.randint(1,30)
            a,t,s = [[rng.randrange(c) for _ in range(count)] for count in (n*n,n*n,d*d)]
            instance = Instance(n,d,c,k,a,t,s)
            scores = []
            for function in (solver.solve_plateau,solver.solve_lookahead,solver.solve):
                ops = function(n,d,c,k,a[:],t,s[:])
                final,_ = simulate(instance,ops)
                scores.append(match_count(instance,final))
            self.assertEqual(scores[-1],max(scores[:-1]))


if __name__ == '__main__':
    unittest.main()
