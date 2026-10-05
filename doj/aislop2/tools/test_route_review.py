"""Fresh, independent semantic and runtime review of frozen routing helpers."""
import importlib.util
import json
from pathlib import Path
import random
import sys
import time
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools.simulate import Instance,simulate,match_count
from tools.validate_output import validate_output
from solvers.experiments.route_sparse_fragment import route_patterns,route_tail
from solvers.experiments import route_extensions_fragment as extra

spec=importlib.util.spec_from_file_location('route_unpruned',ROOT/'solvers/experiments/route_39_six_three.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
extra.build,extra.transition,extra.route_tail=old.build,old.transition,route_tail
POWERS=(6,6,9,5,12,3,6,9,12)


def make_case(rng,n,d,c,k,family):
    stamp=[rng.randrange(c) for _ in range(d*d)]
    target=[rng.randrange(c) for _ in range(n*n)]
    if family=='random':grid=[rng.randrange(c) for _ in target]
    elif family=='near':
        grid=target[:]
        for p in rng.sample(range(n*n),min(n*n,max(1,n*n//15))):grid[p]=(grid[p]+rng.randrange(1,c))%c
    elif family=='stripes':
        target=[(p//n+p%n//2)%c for p in range(n*n)]
        grid=target[:]
        for p in rng.sample(range(n*n),min(n*n,max(2,n*n//8))):grid[p]=rng.randrange(c)
    else:
        grid=[rng.randrange(c) for _ in target]
        origin=Instance(n,d,c,180,grid,target,stamp)
        word=[(rng.randrange(n-d+1),rng.randrange(n-d+1),rng.randrange(4)) for _ in range(12)]
        target,_=simulate(origin,word)
    return Instance(n,d,c,k,grid,target,stamp)


class RouteReview(unittest.TestCase):
    def test_unique_label_permutations_all_powers(self):
        checked=0
        for n,d in ((3,2),(3,3),(4,3),(9,2),(16,3),(30,2),(30,3)):
            # Distinct labels make every incorrect source index observable.
            state=list(range(n*n+d*d))
            case=Instance(n,d,6,180,state[:n*n],state[:n*n],state[n*n:])
            for dx,dy,r,s,backward,count,mapping in route_patterns(n,d,(3,5,6,9,12)):
                x,y=0,max(0,-dy)
                if x+dx>n-d or y+dy>n-d or y>n-d:continue
                left,right=(x,y,r),(x+dx,y+dy,s)
                word=([right,left] if backward else [left,right])*count
                final,_=simulate(case,word)
                expected=state[:n*n];base=x*n+y
                for p,q,buffer in mapping:expected[base+p]=state[q if buffer else base+q]
                self.assertEqual(final,expected)
                checked+=1
        self.assertGreater(checked,5000)
        print('unique-label permutation checks',checked,flush=True)

    def test_pruning_exactly_matches_unpruned_on_fresh_cases(self):
        rng=random.Random(202609260173)
        checked=0
        choices=((3,),(5,),(6,),(9,),(12,),(3,5,6,9,12))
        rows=[]
        for i in range(24):
            n=(3,5,8,12,20,30)[i%6];d=2+(i//6)%2;c=(2,6)[i%2]
            repeats=choices[(i//4+i)%len(choices)]
            k=2*max(repeats)+12
            case=make_case(rng,n,d,c,k,('random','near','stripes','reachable')[i%4])
            before=(case.a[:],case.s[:]);start=time.perf_counter()
            expected=old.route_tail(n,d,case.a,case.t,case.s,k,repeats,2)
            actual=route_tail(n,d,case.a,case.t,case.s,k,repeats,2)
            elapsed=time.perf_counter()-start
            self.assertEqual(actual,expected,(n,d,repeats))
            self.assertEqual((case.a,case.s),before)
            final,_=simulate(case,actual)
            self.assertGreaterEqual(match_count(case,final),match_count(case,case.a))
            rows.append(dict(n=n,d=d,c=c,powers=repeats,operations=len(actual),runtime_sec=elapsed))
            checked+=1
        (ROOT/'results/route_review_pruning.json').write_text(json.dumps(rows,indent=2))
        print('fresh pruning comparisons',checked,flush=True)

    def test_full_power_schedule_fresh_holdout(self):
        rng=random.Random(202609260947)
        rows=[]
        for i in range(36):
            n=(3,4,7,13,23,30)[i%6];d=2+(i//6)%2;c=(2,6)[(i//12)%2]
            k=1 if i<12 else 180
            family=('random','near','stripes','reachable')[i%4]
            case=make_case(rng,n,d,c,k,family)
            board,stamp=case.a[:],case.s[:]
            start=time.perf_counter()
            operations=extra.route_extra_powers(n,d,board,case.t,stamp,k,POWERS)
            elapsed=time.perf_counter()-start
            answer=(str(len(operations))+'\n'+''.join('%d %d %d\n'%op for op in operations)).encode()
            validated=validate_output(case,answer)
            final,buffer=simulate(case,validated)
            self.assertEqual((board,stamp),(final,buffer))
            initial_matches=match_count(case,case.a);matches=match_count(case,final)
            self.assertGreaterEqual(matches,initial_matches)
            rows.append(dict(id=i,n=n,d=d,c=c,k=k,family=family,initial_matches=initial_matches,
                matches=matches,gain=matches-initial_matches,operations=len(operations),
                output_bytes=len(answer),runtime_sec=elapsed))
        report=dict(seed=202609260947,cases=len(rows),powers=POWERS,
            max_runtime_sec=max(row['runtime_sec'] for row in rows),
            total_runtime_sec=sum(row['runtime_sec'] for row in rows),results=rows)
        (ROOT/'results/route_review_holdout.json').write_text(json.dumps(report,indent=2))
        print('fresh full-power helper holdout',len(rows),'max',report['max_runtime_sec'],flush=True)


if __name__=='__main__':unittest.main()
