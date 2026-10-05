"""Differential proof and measured speed for fused temporal boundaries."""
import importlib.util
import json
from pathlib import Path
import random
import sys
import time
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


old=load('temporal_old','solvers/experiments/runtime_route_early_bound.py')
new=load('temporal_fast','solvers/experiments/runtime_temporal_fast.py')


class BoundaryTests(unittest.TestCase):
    def test_arbitrary_states_all_fields_and_best(self):
        rng=random.Random(202609270782)
        for trial in range(35):
            n=(3,5,9,17,30)[trial%5];d=2+(trial//5)%2;c=2+trial%5
            initial=[rng.randrange(c) for _ in range(n*n+d*d)]
            target=[rng.randrange(c) for _ in range(n*n)]
            indices,_,ops,_,_=old.build(n,d,target);actions=list(zip(indices,ops))
            order=list(range(len(actions)));rng.shuffle(order)
            left=old.RefineState(n,d,initial,target,actions,order)
            right=new.RefineState(n,d,initial,target,actions,order)
            for step in range(30):
                action=rng.randrange(len(actions))
                if step%4==0:
                    wishes=bool(rng.randrange(2))
                    left.apply(action,wishes);right.apply(action,wishes)
                else:
                    left.apply(action);left.apply(action,wishes=True)
                    new.temporal_boundary(right,action)
                self.assertEqual(left.__dict__,right.__dict__)
                self.assertEqual(left.best(),right.best())
                ranks=[0]*len(actions)
                for rank,aid in enumerate(order):ranks[aid]=rank
                expected=left.best()
                for minimum in (0,1,3,8,18):
                    actual=new.temporal_best(right,ranks,minimum)
                    if expected[1]>minimum:self.assertEqual(actual,expected)
                    else:self.assertLessEqual(actual[1],minimum)

    def test_insertion_deletion_and_complete_temporal_paths(self):
        rng=random.Random(202609270793)
        for trial in range(24):
            n=(3,6,12,30)[trial%4];d=2+(trial//4)%2;c=2+trial%5;k=8+trial%12
            initial=[rng.randrange(c) for _ in range(n*n+d*d)]
            target=[rng.randrange(c) for _ in range(n*n)]
            indices,_,ops,_,_=old.build(n,d,target);actions=list(zip(indices,ops))
            sequence=[rng.randrange(len(actions)) for _ in range(k-4)]
            args=(n,d,initial,target,actions,sequence)
            self.assertEqual(old.best_insertion(*args,seed=trial),new.best_insertion(*args,seed=trial))
            self.assertEqual(old.deletion_deltas(*args),new.deletion_deltas(*args))
            args=(n,d,k,initial,target,actions,sequence)
            self.assertEqual(old.temporal_repair(*args,rounds=2,removals=2),new.temporal_repair(*args,rounds=2,removals=2))


def measure():
    rng=random.Random(202609270794)
    rows=[]
    for n,d in ((30,2),(30,3)):
        initial=[rng.randrange(6) for _ in range(n*n+d*d)]
        target=[rng.randrange(6) for _ in range(n*n)]
        indices,_,ops,_,_=old.build(n,d,target);actions=list(zip(indices,ops))
        sequence=[rng.randrange(len(actions)) for _ in range(175)]
        outputs=[];times=[]
        for module in (old,new):
            start=time.perf_counter()
            result=module.temporal_repair(n,d,180,initial,target,actions,sequence,rounds=5,removals=5)
            times.append(time.perf_counter()-start);outputs.append(result)
        assert outputs[0]==outputs[1]
        row=dict(n=n,d=d,old_sec=times[0],new_sec=times[1],speedup=times[0]/times[1],operations=len(outputs[0]))
        rows.append(row);print(row,flush=True)
    (ROOT/'results/runtime_temporal_micro.json').write_text(json.dumps(rows,indent=2))


if __name__=='__main__':
    if '--measure' in sys.argv:measure()
    else:unittest.main()
