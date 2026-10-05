"""Exact path parity for bitparallel routing against scalar reference search."""
import json
from pathlib import Path
import random
import sys
import time
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools.simulate import Instance,simulate,parse_instance,match_count
from solvers.experiments.route_sparse_fragment import route_patterns,route_tail
from solvers.experiments import route_bits_fragment as bits
from tools.test_route_review import make_case
bits.route_patterns=route_patterns


class BitRouteTests(unittest.TestCase):
    def test_fresh_complete_path_parity(self):
        rng=random.Random(202609262057)
        for i in range(30):
            n=(3,4,7,12,20,30)[i%6];d=2+(i//6)%2;c=2+i%5
            repeats=((3,),(5,),(6,),(9,),(12,),(3,5,6,9,12))[(i//5+i)%6]
            case=make_case(rng,n,d,c,2*max(repeats)+18,('random','near','stripes','reachable')[i%4])
            before=(case.a[:],case.s[:])
            expected=route_tail(n,d,case.a,case.t,case.s,case.k,repeats,3)
            actual=bits.route_tail_bits(n,d,case.a,case.t,case.s,case.k,repeats,3)
            self.assertEqual(actual,expected,(i,n,d,repeats))
            self.assertEqual((case.a,case.s),before)
            final,_=simulate(case,actual)
            self.assertGreaterEqual(match_count(case,final),match_count(case,case.a))

    def test_short_budget_does_not_expand_empty_power_set(self):
        for k in (0,1,5,6,10,11):
            self.assertEqual(bits.route_tail_bits(3,2,[0]*9,[1]*9,[0]*4,k,(6,),3),[])
        self.assertEqual(bits.route_tail_bits(3,2,[1,0,1,0,1,1,0,1,0],
            [0,1,1,1,0,0,0,1,1],[1,1,0,1],4,(2,),3),[])


def diagnose():
    previous=json.loads((ROOT/'results/route_canceled_variants.json').read_text())['adaptive']
    cached={r['id']:r for r in json.loads((ROOT/'results/temporal_parent39_cache.json').read_text())['results']}
    rows=[]
    for old in previous:
        row=cached[old['id']]
        case=parse_instance((ROOT/'cases/generated'/f"{row['id']}.in").read_text())
        sequence=[]
        for operation in row['operations']:
            if sequence and sequence[-1]==operation:sequence.pop()
            else:sequence.append(operation)
        start=time.perf_counter()
        tail=bits.route_tail_bits(case.n,case.d,row['board'],case.t,row['stamp'],case.k-len(sequence),(3,),min(8,max(3,2500//case.n**2)))
        elapsed=time.perf_counter()-start
        assert tail==[tuple(x) for x in old['operations']],row['id']
        rows.append(dict(id=row['id'],runtime_sec=elapsed))
    report=dict(cases=len(rows),max_runtime_sec=max(x['runtime_sec'] for x in rows),
                total_runtime_sec=sum(x['runtime_sec'] for x in rows),results=rows)
    (ROOT/'results/route_bits_cached_parity.json').write_text(json.dumps(report,indent=2))
    print('cached exactparity',len(rows),'sum',report['total_runtime_sec'],'max',report['max_runtime_sec'],flush=True)


def full_helper():
    from solvers.experiments import route_extensions_fragment as extra
    from tools.test_route_review import old,POWERS
    from tools.validate_output import validate_output
    extra.build,extra.transition=old.build,old.transition
    rng=random.Random(202609260947)
    rows=[]
    for i in range(36):
        n=(3,4,7,13,23,30)[i%6];d=2+(i//6)%2;c=(2,6)[(i//12)%2]
        k=1 if i<12 else 180
        family=('random','near','stripes','reachable')[i%4]
        case=make_case(rng,n,d,c,k,family)
        expected=None
        times=[]
        for solver in (route_tail,bits.route_tail_bits):
            extra.route_tail=solver
            board,stamp=case.a[:],case.s[:]
            start=time.perf_counter()
            operations=extra.route_extra_powers(n,d,board,case.t,stamp,k,POWERS)
            times.append(time.perf_counter()-start)
            answer=(str(len(operations))+'\n'+''.join('%d %d %d\n'%op for op in operations)).encode()
            validate_output(case,answer)
            final,buffer=simulate(case,operations)
            assert (board,stamp)==(final,buffer)
            assert match_count(case,final)>=match_count(case,case.a)
            if expected is None:expected=operations
            else:assert operations==expected,(i,n,d,c)
        rows.append(dict(id=i,n=n,d=d,c=c,k=k,family=family,operations=len(expected),
            scalar_runtime_sec=times[0],bits_runtime_sec=times[1]))
    report=dict(cases=len(rows),powers=POWERS,scalar_max=max(x['scalar_runtime_sec'] for x in rows),
        bits_max=max(x['bits_runtime_sec'] for x in rows),scalar_sum=sum(x['scalar_runtime_sec'] for x in rows),
        bits_sum=sum(x['bits_runtime_sec'] for x in rows),results=rows)
    (ROOT/'results/route_bits_full_power_holdout.json').write_text(json.dumps(report,indent=2))
    print({k:v for k,v in report.items() if k!='results'},flush=True)


if __name__=='__main__':
    if '--diagnose' in sys.argv:diagnose()
    elif '--full-helper' in sys.argv:full_helper()
    else:unittest.main()
