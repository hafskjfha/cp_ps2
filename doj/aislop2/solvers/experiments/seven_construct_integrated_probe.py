"""Whole-pipeline integration probe. Diagnostic imports are intentional."""
import argparse
import importlib.util
import json
import sys
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from tools.simulate import parse_instance,simulate,match_count
from tools.validate_output import validate_output

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--limit',type=int,default=100)
    parser.add_argument('--mode',choices=['early','late','pool'],default='early')
    parser.add_argument('--width',type=int,default=16)
    parser.add_argument('--fast',action='store_true')
    parser.add_argument('--ids',default='')
    parser.add_argument('--domain',choices=['broad','d3','complement'],default='broad')
    args=parser.parse_args()
    m=load('base','solvers/experiments/million_safe_readable.py')
    cluster=load('cluster','solvers/experiments/seven_construct_cluster_fast.py' if args.fast else 'solvers/experiments/seven_construct_cluster_frozen.py')
    original_construct=m.construct_all;original_beam=m.million_beam;original_pool=m.construct_pool
    def eligible(n,d,c,k,grid,target,stamp):
        if n<=16 or k<=10:return False
        if args.domain!='broad' and d!=3:return False
        if args.domain=='complement':
            patterns={tuple(target[(x+i)*n+y+j]for i in range(d)for j in range(d))
                      for x in range(n-d+1)for y in range(n-d+1)}
            if n>=10 and k>=12 and len(patterns)<=4*c and 100*sum(a==b for a,b in zip(grid,target))<88*m.color_bound(grid+stamp,target):return False
        return True
    def construct(*a):
        reference=original_construct(*a)
        return cluster.improve(m,*a,reference,width=args.width) if eligible(*a) else reference
    def late(*a,**kw):
        if eligible(*a[:7]):
            return cluster.improve(m,*a[:8],width=args.width) if args.mode=='late' else a[7]
        return original_beam(*a,**kw)
    def pool(*a):
        rows=original_pool(*a)
        if eligible(*a):
            candidate=cluster.improve(m,*a,rows[0][1],width=args.width)
            n,d,c,k,grid,target,stamp=a
            positions,_,_,_,_=m.build(n,d,target);side=n-d+1
            final=grid+stamp
            for x,y,r in candidate:m._st(final,n*n,positions[(x*side+y)*4+r])
            rows.append((sum(x==y for x,y in zip(final,target)),candidate))
            rows.sort(key=lambda row:row[0],reverse=True)
        return rows
    if args.mode=='early':m.construct_all=construct
    elif args.mode=='pool':m.construct_pool=pool
    m.million_beam=late
    parent={r['id']:r for r in json.loads((ROOT/'results/seven_parent_cache.json').read_text())['results']}
    rows=[]
    for meta in json.loads((ROOT/'cases/manifest.json').read_text())['cases']:
        if 'dev' not in meta['suites']:continue
        if args.ids and meta['id'] not in args.ids.split(','):continue
        ins=parse_instance((ROOT/meta['path']).read_text())
        if not eligible(ins.n,ins.d,ins.c,ins.k,ins.a,ins.t,ins.s):continue
        start=time.perf_counter()
        operations=m.solve(ins.n,ins.d,ins.c,ins.k,ins.a,ins.t,ins.s)
        elapsed=time.perf_counter()-start
        output=str(len(operations))+'\n'+'\n'.join(' '.join(map(str,x)) for x in operations)+'\n'
        validate_output(ins,output.encode())
        matches=match_count(ins,simulate(ins,operations)[0])
        baseline=parent[meta['id']]
        delta=1000000*matches//(ins.n*ins.n)-baseline['score']
        row=dict(id=meta['id'],matches=matches,parent=baseline['matches'],delta=delta,
                 runtime_sec=elapsed,parent_runtime_sec=baseline['runtime_sec'],operations=operations)
        rows.append(row)
        print(meta['id'],delta,round(elapsed,3),flush=True)
        if len(rows)>=args.limit:break
    result=dict(mode=args.mode,width=args.width,cases=rows,total_delta=sum(r['delta'] for r in rows),
                wins=sum(r['delta']>0 for r in rows),losses=sum(r['delta']<0 for r in rows),
                runtime_sec=sum(r['runtime_sec'] for r in rows),max_runtime_sec=max(r['runtime_sec'] for r in rows))
    out=ROOT/('results/seven_construct_integrated_%s_w%d_n%d%s%s%s.json'%(args.mode,args.width,args.limit,'_fast' if args.fast else '',('_'+args.ids.replace(',','-')) if args.ids else '',('_'+args.domain) if args.domain!='broad' else ''))
    out.write_text(json.dumps(result));print({k:v for k,v in result.items() if k!='cases'},flush=True)

if __name__=='__main__':main()
