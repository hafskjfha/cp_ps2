"""Guard, state restoration, score-floor tests and cached macro-power stages."""
import argparse
import importlib.util
import json
from pathlib import Path
import random
import sys
import time
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools.simulate import Instance,parse_instance,simulate,match_count
from solvers.experiments import route_extensions_fragment as extra
from solvers.experiments.route_sparse_fragment import route_tail

spec=importlib.util.spec_from_file_location('route_parent',ROOT/'submissions/best_027_251280679.py')
parent=importlib.util.module_from_spec(spec);spec.loader.exec_module(parent)
extra.build,extra.transition,extra.route_tail=parent.build,parent.transition,route_tail


class ExtraTests(unittest.TestCase):
    def test_budget_guard_and_exact_state_and_score_floor(self):
        rng=random.Random(933309)
        for k in (0,1,5,6,9,10,11,12,17,18,23,24,37):
            n,d,c=5,3,3
            a,t,s=[[rng.randrange(c) for _ in range(size)] for size in (n*n,n*n,d*d)]
            board,stamp=a[:],s[:]
            word=extra.route_extra_powers(n,d,board,t,stamp,k,(6,9,5,12))
            case=Instance(n,d,c,k,a,t,s)
            final,buffer=simulate(case,word)
            self.assertEqual((board,stamp),(final,buffer))
            self.assertGreaterEqual(match_count(case,final),match_count(case,a))
            self.assertLessEqual(len(word),k)
            if k<10:self.assertEqual(word,[])


def diagnose(path,powers,output):
    from collections import Counter
    report=json.loads(path.read_text());states=[]
    for row in report['results']:
        case=parse_instance((ROOT/'cases/generated'/f"{row['id']}.in").read_text())
        available,needed=Counter(case.a+case.s),Counter(case.t)
        bound=sum(min(available[v],needed[v]) for v in needed)
        if case.k-len(row['operations'])<2*min(powers) or row['matches']>=bound:continue
        board,stamp=simulate(case,row['operations'])
        states.append(dict(row=row,case=case,bound=bound,board=board,stamp=stamp,
                           operations=row['operations'][:],matches=row['matches'],runtime=0))
    result={};previous=0
    for stage,power in enumerate(powers):
        rows=[]
        for state in states:
            row,case=state['row'],state['case'];start=time.perf_counter()
            if state['matches']<state['bound']:
                tail=extra.route_extra_powers(case.n,case.d,state['board'],case.t,state['stamp'],case.k-len(state['operations']),(power,))
                state['operations']+=tail
                state['matches']=match_count(case,state['board'])
            state['runtime']+=time.perf_counter()-start
            final,stamp=simulate(case,state['operations'])
            assert (final,stamp)==(state['board'],state['stamp'])
            delta=1000000*state['matches']//(case.n*case.n)-row['score']
            rows.append(dict(id=row['id'],n=case.n,d=case.d,delta=delta,gain=state['matches']-row['matches'],
                             matches=state['matches'],operations=state['operations'][:],runtime=state['runtime']))
        delta=sum(x['delta'] for x in rows)
        result[f'{stage}_{power}']=dict(parent=str(path),parent_score=report['total_score'],
            total_score=report['total_score']+delta,delta=delta,stage_delta=delta-previous,
            max_runtime_sec=max((x['runtime'] for x in rows),default=0),results=rows)
        print(stage,power,'total',report['total_score']+delta,'delta',delta,'stage gain',delta-previous,
              'sum',round(sum(x['runtime'] for x in rows),3),'max',round(max(x['runtime'] for x in rows),3),flush=True)
        previous=delta
    output.write_text(json.dumps(result,indent=2))


if __name__=='__main__':
    if '--diagnose' not in sys.argv:unittest.main()
    else:
        parser=argparse.ArgumentParser()
        parser.add_argument('--diagnose',type=Path)
        parser.add_argument('--powers',type=int,nargs='+',default=[6,9,5,12])
        parser.add_argument('--output',type=Path,default=ROOT/'results/route_extensions_standard.json')
        args=parser.parse_args();diagnose(args.diagnose,args.powers,args.output)
