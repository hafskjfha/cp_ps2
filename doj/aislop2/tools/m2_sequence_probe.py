"""Cached, canonical diagnostic for the m2 sequence neighborhood."""
import argparse,json,runpy,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools.simulate import parse_instance,simulate,match_count
from tools.validate_output import validate_output

p=argparse.ArgumentParser()
p.add_argument('--cache',default='results/m2_parent_cache.json')
p.add_argument('--mode',default='relocate')
p.add_argument('--limit',type=int,default=100)
p.add_argument('--rounds',type=int,default=2)
p.add_argument('--blocks',default='1,2,3')
p.add_argument('--passes',type=int,default=1)
p.add_argument('--output',default='results/m2_sequence_relocate_dev.json')
p.add_argument('--module',default='solvers/experiments/m2_sequence_runtime_final.py')
args=p.parse_args()
module=runpy.run_path(str(ROOT/args.module))
probe=runpy.run_path(str(ROOT/('solvers/experiments/m2_sequence_'+args.mode+'.py')))[args.mode+'_refine']
data=json.loads((ROOT/args.cache).read_text());rows=[]
source=data.get('results',data.get('cases'))
for row in source[:args.limit]:
    inst=parse_instance((ROOT/'cases/generated'/(row['id']+'.in')).read_text())
    indices,_,ops,_,_=module['build'](inst.n,inst.d,inst.t)
    side=inst.n-inst.d+1
    sequence=[(x*side+y)*4+r for x,y,r in row['operations']]
    start=time.perf_counter()
    candidate=probe(inst.n,inst.d,inst.c,inst.k,inst.a+inst.s,inst.t,indices,sequence,module,rounds=args.rounds,blocks=tuple(map(int,args.blocks.split(','))),passes=args.passes)
    elapsed=time.perf_counter()-start
    operations=[ops[a] for a in candidate]
    output=str(len(operations))+'\n'+'\n'.join(' '.join(map(str,a)) for a in operations)+'\n'
    validate_output(inst,output.encode())
    matches=match_count(inst,simulate(inst,operations)[0]);score=1000000*matches//inst.n**2
    parent=1000000*row['matches']//inst.n**2
    assert score>=parent,(row['id'],score,parent)
    rows.append(dict(id=row['id'],delta=score-parent,matches=matches,parent=row['matches'],score=score,runtime_sec=elapsed,operations=operations))
    if score>parent or elapsed>1:print(row['id'],score-parent,round(elapsed,3),flush=True)
    module['_REFINE_GOALS'].clear()
summary=dict(config=vars(args),cases=len(rows),total_delta=sum(r['delta'] for r in rows),wins=sum(r['delta']>0 for r in rows),max_runtime_sec=max(r['runtime_sec'] for r in rows),total_runtime_sec=sum(r['runtime_sec'] for r in rows),results=rows)
(ROOT/args.output).write_text(json.dumps(summary))
print({k:v for k,v in summary.items() if k!='results'},flush=True)
