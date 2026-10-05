"""Differential and parent-state diagnostics for sparse six-step routing."""
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
from solvers.experiments.route_sparse_fragment import route_patterns,route_tail


class RouteTests(unittest.TestCase):
    def test_permutations_match_canonical_simulator(self):
        rng=random.Random(291828)
        for n,d in ((3,2),(4,3),(7,2),(8,3)):
            state=[rng.randrange(6) for _ in range(n*n+d*d)]
            case=Instance(n,d,6,180,state[:n*n],state[:n*n],state[n*n:])
            for dx,dy,r,s,backward,count,mapping in route_patterns(n,d,(3,6)):
                x,y=0,max(0,-dy)
                if x+dx>n-d or y+dy>n-d or y>n-d:continue
                left,right=(x,y,r),(x+dx,y+dy,s)
                word=([right,left] if backward else [left,right])*count
                final,_=simulate(case,word)
                expected=state[:n*n]
                base=x*n+y
                for p,q,buffer in mapping:expected[base+p]=state[q if buffer else base+q]
                self.assertEqual(final,expected)

    def test_appending_is_legal_and_monotone(self):
        rng=random.Random(732098)
        for _ in range(12):
            n,d=rng.choice(((3,2),(4,3),(5,2),(6,3)))
            a,t,s=[[rng.randrange(3) for _ in range(size)] for size in (n*n,n*n,d*d)]
            case=Instance(n,d,3,18,a,t,s)
            word=route_tail(n,d,a,t,s,18,(3,6))
            final,_=simulate(case,word)
            self.assertGreaterEqual(match_count(case,final),match_count(case,a))


def diagnose():
    spec=importlib.util.spec_from_file_location('parent',ROOT/'submissions/best_039_251862073.py')
    parent=importlib.util.module_from_spec(spec);spec.loader.exec_module(parent)
    report=json.loads((ROOT/'results/checkpoints/best_039_251862073.benchmark.json').read_text())
    records=[]
    cached=ROOT/'results/route_parent39_states.json'
    if cached.exists():
        records=json.loads(cached.read_text())
    else:
        for row in report['results']:
            if row['k']-row['operations']<6:continue
            case=parse_instance((ROOT/'cases/generated'/f"{row['id']}.in").read_text())
            bound=parent.color_bound(case.a+case.s,case.t)
            if row['matches']>=bound:continue
            start=time.perf_counter()
            ops=parent.solve(case.n,case.d,case.c,case.k,case.a[:],case.t,case.s[:])
            board,stamp=simulate(case,ops)
            assert match_count(case,board)==row['matches']
            records.append(dict(row=row,board=board,stamp=stamp,operations=ops,parent_runtime=time.perf_counter()-start))
            print('cached',row['id'],flush=True)
        cached.write_text(json.dumps(records))
    results=[]
    for record in records:
        row=record['row']
        case=parse_instance((ROOT/'cases/generated'/f"{row['id']}.in").read_text())
        if case.n>20:continue
        start=time.perf_counter()
        tail=route_tail(case.n,case.d,record['board'],case.t,record['stamp'],case.k-len(record['operations']),(3,6))
        elapsed=time.perf_counter()-start
        final,_=simulate(case,record['operations']+tail)
        gain=match_count(case,final)-row['matches']
        result=dict(id=row['id'],n=case.n,d=case.d,gain=gain,operations=len(tail),runtime=elapsed)
        results.append(result);print(result,flush=True)
    (ROOT/'results/route_sparse_diagnostic.json').write_text(json.dumps(results,indent=2))


def variants():
    records=json.loads((ROOT/'results/route_parent39_states.json').read_text())
    all_results={}
    for name,repeats,rounds in [('six_once',(3,),1),('six_three',(3,),3),
                                 ('six_many',(3,),16),('twelve_many',(3,6),16)]:
        results=[]
        for record in records:
            row=record['row']
            case=parse_instance((ROOT/'cases/generated'/f"{row['id']}.in").read_text())
            start=time.perf_counter()
            tail=route_tail(case.n,case.d,record['board'],case.t,record['stamp'],case.k-len(record['operations']),repeats,rounds)
            elapsed=time.perf_counter()-start
            final,_=simulate(case,record['operations']+tail)
            gain=match_count(case,final)-row['matches']
            delta=1000000*match_count(case,final)//(case.n*case.n)-row['score']
            result=dict(id=row['id'],n=case.n,d=case.d,gain=gain,delta=delta,operations=tail,runtime=elapsed)
            results.append(result)
        all_results[name]=results
        print(name,'delta',sum(x['delta'] for x in results),'wins',sum(x['gain']>0 for x in results),
              'sum',round(sum(x['runtime'] for x in results),3),'max',round(max(x['runtime'] for x in results),3),flush=True)
    (ROOT/'results/route_sparse_variants.json').write_text(json.dumps(all_results,indent=2))


def canceled_variants():
    from collections import Counter
    records=json.loads((ROOT/'results/temporal_parent39_cache.json').read_text())['results']
    selected=[]
    for row in records:
        case=parse_instance((ROOT/'cases/generated'/f"{row['id']}.in").read_text())
        counts,needed=Counter(case.a+case.s),Counter(case.t)
        if row['matches']>=sum(min(counts[v],needed[v]) for v in needed):continue
        sequence=[]
        for operation in row['operations']:
            if sequence and sequence[-1]==operation:sequence.pop()
            else:sequence.append(operation)
        if case.k-len(sequence)<6:continue
        board,stamp=simulate(case,sequence)
        assert board==row['board'] and stamp==row['stamp']
        selected.append((row,case,sequence))
    report={}
    for name,rounds in [('three',3),('five',5),('eight',8),('adaptive',-1)]:
        rows=[]
        for row,case,sequence in selected:
            count=rounds if rounds>0 else min(8,max(3,2500//(case.n*case.n)))
            start=time.perf_counter()
            tail=route_tail(case.n,case.d,row['board'],case.t,row['stamp'],case.k-len(sequence),(3,),count)
            elapsed=time.perf_counter()-start
            final,_=simulate(case,sequence+tail)
            matches=match_count(case,final)
            rows.append(dict(id=row['id'],n=case.n,d=case.d,gain=matches-row['matches'],
                             delta=1000000*matches//(case.n*case.n)-row['score'],
                             canceled=len(row['operations'])-len(sequence),operations=tail,runtime=elapsed))
        report[name]=rows
        print('canceled',name,'delta',sum(x['delta'] for x in rows),'wins',sum(x['gain']>0 for x in rows),
              'sum',round(sum(x['runtime'] for x in rows),3),'max',round(max(x['runtime'] for x in rows),3),flush=True)
    (ROOT/'results/route_canceled_variants.json').write_text(json.dumps(report,indent=2))


if __name__=='__main__':
    if '--diagnose' in sys.argv:diagnose()
    elif '--canceled' in sys.argv:canceled_variants()
    elif '--variants' in sys.argv:variants()
    else:unittest.main()
