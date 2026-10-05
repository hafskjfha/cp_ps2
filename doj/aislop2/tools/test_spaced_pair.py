import random
import unittest
from tools.test_solver import ROOT,load_solver
from tools.simulate import Instance,simulate,match_count


class SpacedPairTests(unittest.TestCase):
    def test_exact_completion_and_delta(self):
        solver=load_solver(ROOT/'solvers/experiments/spaced_hybrid.py')
        rng=random.Random(1632997)
        for _ in range(70):
            n,d,c,k=rng.randint(3,6),rng.choice((2,3)),rng.randint(2,6),rng.randint(4,15)
            a,t,s=[[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,d*d)]
            indices,_,ops,_,_=solver.build(n,d,t)
            actions=list(zip(indices,ops))
            sequence=[rng.randrange(-1,len(actions)) for _ in range(k)]
            state=solver.SequenceState(a+s,t,actions,sequence,n*n)
            i=rng.randrange(k-2);j=rng.randrange(i+2,k)
            fixed=rng.randrange(-1,len(actions));side=rng.randrange(2)
            replacements=solver.complete_spaced_pair(state,i,j,fixed,side,n*n,d*d)
            case=Instance(n,d,c,k,a,t,s)
            def evaluate(seq):
                final,_=simulate(case,[ops[x] for x in seq if x>=0])
                return match_count(case,final)
            actual=evaluate(sequence[:i]+replacements+sequence[j+1:])
            best=-1
            for other in range(-1,len(actions)):
                trial=sequence[:]
                trial[i],trial[j]=(other,fixed) if side else (fixed,other)
                best=max(best,evaluate(trial))
            self.assertEqual(actual,best)
            delta=state.delta(i,replacements)
            self.assertEqual(delta,actual-state.score)
            state.accept(i,replacements,delta)
            rebuilt=solver.SequenceState(a+s,t,actions,state.sequence,n*n)
            self.assertEqual(state.prefix,rebuilt.prefix)
            self.assertEqual(state.wishes,rebuilt.wishes)
            self.assertEqual(state.score,actual)


if __name__=='__main__':
    unittest.main()
