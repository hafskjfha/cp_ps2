"""Runtime-only early completion, accepted solely at the color inventory bound."""
import ast
import importlib.util
import json
from pathlib import Path
import random
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools.simulate import Instance,simulate,match_count
from tools.benchmark import evaluate_case,summarize

PATH=ROOT/'solvers/experiments/runtime_route_early_bound.py'
spec=importlib.util.spec_from_file_location('runtime_early',PATH)
candidate=importlib.util.module_from_spec(spec);spec.loader.exec_module(candidate)


class EarlyRouteTests(unittest.TestCase):
    def test_old_program_is_unchanged_outside_guarded_injection(self):
        old=ast.parse((ROOT/'solvers/experiments/algebra39_cycles.py').read_text())
        new=ast.parse(PATH.read_text())
        new.body=[node for node in new.body if getattr(node,'name',None)!='runtime_early_bound']
        changed=next(node for node in new.body if getattr(node,'name',None)=='solve_without_hot_restart')
        self.assertIsInstance(changed.body[1],ast.If)
        del changed.body[1]
        self.assertEqual(ast.dump(old,include_attributes=False),ast.dump(new,include_attributes=False))

    def test_trials_preserve_inputs_and_only_accept_proven_bound(self):
        rng=random.Random(202609270144)
        for trial in range(20):
            n,d,c,k=5+trial%5,3,2+trial%5,(5,6,12,90)[trial%4]
            grid=[rng.randrange(c) for _ in range(n*n)]
            target=grid[:]
            for p in rng.sample(range(n*n),min(n*n,2+trial%8)):target[p]=rng.randrange(c)
            stamp=[rng.randrange(c) for _ in range(d*d)]
            prefix=[(rng.randrange(n-d+1),rng.randrange(n-d+1),rng.randrange(4)) for _ in range(min(3,k))]
            before=(grid[:],target[:],stamp[:],prefix[:],random.getstate())
            answer=candidate.runtime_early_bound(n,d,k,grid,target,stamp,prefix)
            self.assertEqual((grid,target,stamp,prefix,random.getstate()),before)
            if answer is not None:
                case=Instance(n,d,c,k,grid,target,stamp)
                final,_=simulate(case,answer)
                self.assertEqual(match_count(case,final),candidate.color_bound(grid+stamp,target))


def diagnose():
    previous=json.loads((ROOT/'results/checkpoints/best_049_252862932.benchmark.json').read_text())
    parent={row['id']:row for row in previous['results']}
    manifest=json.loads((ROOT/'cases/manifest.json').read_text())
    selected=[row for row in manifest['cases'] if 5<=row['n']<=9 and row['d']==3]
    selected.sort(key=lambda row:(row['id'] not in ('case_265','case_317'),row['id']))
    rows=[]
    for meta in selected:
        row=evaluate_case(PATH,meta,5)
        row['delta']=row['score']-parent[row['id']]['score']
        rows.append(row)
        print(row['id'],row['matches'],round(row['runtime_sec'],3),row['delta'],row.get('error',''),flush=True)
    result=dict(**summarize(rows),score_delta=sum(row['delta'] for row in rows),results=rows)
    (ROOT/'results/runtime_route_early_small_diagnostic.json').write_text(json.dumps(result,indent=2))
    print({k:v for k,v in result.items() if k!='results'},flush=True)


if __name__=='__main__':
    if '--diagnose' in sys.argv:diagnose()
    else:unittest.main()
