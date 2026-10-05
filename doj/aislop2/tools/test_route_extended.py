"""Symbolic macro extensions measured only against cached complete sequences."""
import json
from pathlib import Path
import random
import sys
import time
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools.simulate import Instance,parse_instance,simulate,match_count
from solvers.experiments.route_extended_fragment import route_patterns_extended,route_tail_extended


class ExtendedTests(unittest.TestCase):
    def test_extended_permutations(self):
        rng=random.Random(739311)
        for n,d in ((3,2),(4,3),(6,2),(8,3)):
            state=[rng.randrange(6) for _ in range(n*n+d*d)]
            case=Instance(n,d,6,180,state[:n*n],state[:n*n],state[n*n:])
            for dx,dy,r,s,backward,count,mapping in route_patterns_extended(n,d,(5,6,9,12)):
                x,y=0,max(0,-dy)
                if x+dx>n-d or y+dy>n-d or y>n-d:continue
                a,b=(x,y,r),(x+dx,y+dy,s)
                final,_=simulate(case,([b,a] if backward else [a,b])*count)
                expected=state[:n*n];base=x*n+y
                for p,q,buffer in mapping:expected[base+p]=state[q if buffer else base+q]
                self.assertEqual(final,expected)


def diagnose():
    from collections import Counter
    parent=json.loads((ROOT/'results/algebra27_t5_r8_diagnostic.json').read_text())
    eligible=[]
    for row in parent['results']:
        case=parse_instance((ROOT/'cases/generated'/f"{row['id']}.in").read_text())
        available,needed=Counter(case.a+case.s),Counter(case.t)
        if case.k-len(row['operations'])<2:continue
        if row['matches']>=sum(min(available[v],needed[v]) for v in needed):continue
        board,stamp=simulate(case,row['operations'])
        eligible.append((row,case,board,stamp))
    report={}
    for name,powers in [('same',()),('five',(5,)),('six',(6,)),('nine',(9,)),('twelve',(12,))]:
        rows=[]
        for row,case,board,stamp in eligible:
            start=time.perf_counter()
            tail=route_tail_extended(case.n,case.d,board,case.t,stamp,case.k-len(row['operations']),powers,1)
            elapsed=time.perf_counter()-start
            final,_=simulate(case,row['operations']+tail)
            matches=match_count(case,final)
            delta=1000000*matches//(case.n*case.n)-row['score']
            rows.append(dict(id=row['id'],n=case.n,d=case.d,delta=delta,gain=matches-row['matches'],operations=tail,runtime=elapsed))
        report[name]=rows
        print(name,'delta',sum(x['delta'] for x in rows),'wins',sum(x['gain']>0 for x in rows),
              'sum',round(sum(x['runtime'] for x in rows),3),'max',round(max(x['runtime'] for x in rows),3),flush=True)
    (ROOT/'results/route_extended_parent27_diagnostic.json').write_text(json.dumps(report,indent=2))


def sequential():
    from collections import Counter
    parent=json.loads((ROOT/'results/algebra27_t5_r8_diagnostic.json').read_text())
    states=[]
    for row in parent['results']:
        case=parse_instance((ROOT/'cases/generated'/f"{row['id']}.in").read_text())
        available,needed=Counter(case.a+case.s),Counter(case.t)
        bound=sum(min(available[v],needed[v]) for v in needed)
        if case.k-len(row['operations'])<10 or row['matches']>=bound:continue
        board,stamp=simulate(case,row['operations'])
        states.append(dict(row=row,case=case,bound=bound,board=board,stamp=stamp,
                           operations=row['operations'][:],matches=row['matches'],runtime=0))
    report={};previous=0
    for name,power in [('six_once',6),('six_twice',6),('six_thrice',6),('nine',9),('five',5),('twelve',12)]:
        rows=[]
        for state in states:
            row,case=state['row'],state['case'];start=time.perf_counter()
            left=case.k-len(state['operations'])
            if left>=2*power and state['matches']<state['bound']:
                tail=route_tail_extended(case.n,case.d,state['board'],case.t,state['stamp'],left,(power,),1)
                state['operations']+=tail
                state['board'],state['stamp']=simulate(case,state['operations'])
                state['matches']=match_count(case,state['board'])
            state['runtime']+=time.perf_counter()-start
            delta=1000000*state['matches']//(case.n*case.n)-row['score']
            rows.append(dict(id=row['id'],n=case.n,d=case.d,delta=delta,gain=state['matches']-row['matches'],
                             operations=state['operations'][:],runtime=state['runtime']))
        report[name]=rows
        delta=sum(x['delta'] for x in rows)
        print(name,'total',parent['total_score']+delta,'delta',delta,'stage gain',delta-previous,
              'sum',round(sum(x['runtime'] for x in rows),3),'max',round(max(x['runtime'] for x in rows),3),flush=True)
        previous=delta
    (ROOT/'results/route_sequential_parent27_diagnostic.json').write_text(json.dumps(report,indent=2))


if __name__=='__main__':
    if '--diagnose' in sys.argv:diagnose()
    elif '--sequential' in sys.argv:sequential()
    else:unittest.main()
