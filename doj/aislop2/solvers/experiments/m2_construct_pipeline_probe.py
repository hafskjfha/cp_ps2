"""Full solver diagnostic with a stronger constructor replacing old stages."""
import argparse
import json
import sys
import time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from solvers.experiments.m2_construct_probe import load
from tools.simulate import parse_instance,simulate,match_count
from tools.validate_output import validate_output


def domain(m,n,d,c,k,grid,target,stamp):
    if n<10 or k<12:return False
    if 100*sum(a==b for a,b in zip(grid,target))>=70*m.color_bound(grid+stamp,target):return False
    patterns=set()
    for x in range(n-d+1):
        for y in range(n-d+1):
            patterns.add(tuple(target[(x+i)*n+y+j]for i in range(d)for j in range(d)))
            if len(patterns)>4*c:return True
    return False


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--width',type=int,default=64);ap.add_argument('--mode',type=int,default=0)
    ap.add_argument('--compact-width',type=int,default=0)
    ap.add_argument('--compact-long-width',type=int,default=256)
    ap.add_argument('--runtime-final',action='store_true')
    ap.add_argument('--tag',default='')
    ap.add_argument('--stamp-cache',action='store_true')
    ap.add_argument('--packed',action='store_true')
    ap.add_argument('--medium-budget',type=int,default=0)
    ap.add_argument('--retain64',action='store_true')
    ap.add_argument('--suite',default='dev');ap.add_argument('--ids',default='');args=ap.parse_args()
    m=load('base','solvers/experiments/m2_sequence_runtime_final.py'if args.runtime_final else 'solvers/experiments/seven_construct_fast_bytearray_readable.py')
    if args.stamp_cache:exec((ROOT/'solvers/experiments/m2_construct_stampcache_fragment.py').read_text(),m.__dict__)
    if args.packed:
        exec((ROOT/'solvers/experiments/m2_sequence_packed_cluster.py').read_text(),m.__dict__)
        m.M2BeamState=m.PackedClusterState;m.M2BeamClone=m.clone_packed_cluster_state;m.M2BeamChoices=m.packed_cluster_choices
    exp=load('constructor','solvers/experiments/m2_construct_forward.py')
    oldret=m.solve_retained_iterated;oldbeam=m.million_beam
    def replacement(n,d,c,k,grid,target,stamp):
        if not domain(m,n,d,c,k,grid,target,stamp):return oldret(n,d,c,k,grid,target,stamp)
        beam_width=min(args.width,64)if n>=24 and k>=120 else args.width
        if args.compact_width and d==3 and n<=16 and 20<=k<=80:
            beam_width=min(args.compact_width,args.compact_long_width)if k>48 else args.compact_width
        if args.medium_budget and 17<=n<=23:
            allowance=args.medium_budget//(n*n*k)
            beam_width=max(64,min(512,1<<max(0,allowance.bit_length()-1)))
        diversity_mode={3:7,4:8,5:9,6:10}.get(args.mode,1)
        result=exp.construct(m,n,d,c,k,grid,target,stamp,width=beam_width,branch=6,mode=diversity_mode)
        if args.retain64 and beam_width!=64:
            baseline=exp.construct(m,n,d,c,k,grid,target,stamp,width=64,branch=6,mode=1)
            indices,_,_,_,_=m.build(n,d,target);side=n-d+1
            def baseline_score(out):
                board=grid+stamp
                for x,y,r in out:m._st(board,n*n,indices[(x*side+y)*4+r])
                return sum(a==b for a,b in zip(board,target))
            if baseline_score(baseline)>=baseline_score(result):result=baseline
        if args.mode==2:
            extra=exp.construct(m,n,d,c,k,grid,target,stamp,width=beam_width,branch=6,mode=1,seed=1)
            indices,_,_,_,_=m.build(n,d,target);side=n-d+1
            def score(out):
                board=grid+stamp
                for x,y,r in out:m._st(board,n*n,indices[(x*side+y)*4+r])
                return sum(a==b for a,b in zip(board,target))
            if score(extra)>score(result):result=extra
        if args.mode in (1,2,3,4,5,6):
            result=m.cluster_improve(n,d,c,k,grid,target,stamp,result,width=16)
        return result
    def beam(n,d,c,k,grid,target,stamp,reference,**kwargs):
        if domain(m,n,d,c,k,grid,target,stamp):return reference
        return oldbeam(n,d,c,k,grid,target,stamp,reference,**kwargs)
    m.solve_retained_iterated=replacement;m.million_beam=beam
    floors={r['id']:r for r in json.loads((ROOT/'results/checkpoints/runtime_055_254652429.benchmark.json').read_text())['results']}
    report=dict(settings=vars(args),diagnostic_only=True,cases=[])
    suffix='_compact%d'%args.compact_width if args.compact_width else ''
    if args.compact_long_width!=256:suffix+='_long%d'%args.compact_long_width
    if args.runtime_final:suffix+='_fast'
    if args.tag:suffix+='_'+args.tag
    if args.stamp_cache:suffix+='_cache'
    if args.packed:suffix+='_packed'
    if args.medium_budget:suffix+='_medium%d'%args.medium_budget
    if args.retain64:suffix+='_ret64'
    dest=ROOT/('results/m2_construct_pipeline_%s_w%d_m%d%s.json'%(args.suite,args.width,args.mode,suffix))
    selected={r['id']:r for r in json.loads((ROOT/'results/m2_construct_pipeline_stable_w64_m1.json').read_text())['cases']}
    for meta in json.loads((ROOT/'cases/manifest.json').read_text())['cases']:
        if args.suite not in meta['suites']:continue
        if args.ids and meta['id']not in args.ids.split(','):continue
        ins=parse_instance((ROOT/meta['path']).read_text());floor=floors[meta['id']]
        if not domain(m,ins.n,ins.d,ins.c,ins.k,ins.a,ins.t,ins.s):continue
        if args.compact_width or args.medium_budget:
            compact=args.compact_width and ins.d==3 and ins.n<=16 and 20<=ins.k<=80
            medium=args.medium_budget and 17<=ins.n<=23
            if not(compact or medium):continue
        start=time.perf_counter();out=m.solve(ins.n,ins.d,ins.c,ins.k,ins.a,ins.t,ins.s);elapsed=time.perf_counter()-start
        encoded=(str(len(out))+'\n'+'\n'.join(' '.join(map(str,op))for op in out)+'\n').encode()
        validate_output(ins,encoded);matches=match_count(ins,simulate(ins,out)[0]);delta=1000000*matches//ins.n**2-floor['score']
        selected_matches=selected[meta['id']]['matches']
        report['cases'].append(dict(id=meta['id'],n=ins.n,d=ins.d,k=ins.k,parent=floor['matches'],selected_parent=selected_matches,matches=matches,delta=delta,gain_over_selected=1000000*matches//ins.n**2-1000000*selected_matches//ins.n**2,runtime_sec=elapsed,operations=out))
        report.update(total_delta=sum(r['delta']for r in report['cases']),gain_over_selected=sum(r['gain_over_selected']for r in report['cases']),wins=sum(r['delta']>0 for r in report['cases']),losses=sum(r['delta']<0 for r in report['cases']),runtime_sec=sum(r['runtime_sec']for r in report['cases']),max_runtime_sec=max(r['runtime_sec']for r in report['cases']))
        dest.write_text(json.dumps(report));print(meta['id'],matches-floor['matches'],delta,round(elapsed,3),flush=True)
    print({k:v for k,v in report.items()if k!='cases'},flush=True)
if __name__=='__main__':main()
