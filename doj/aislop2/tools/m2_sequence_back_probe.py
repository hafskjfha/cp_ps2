"""Whole backward-constructor parity for the packed FastBack kernel."""
import argparse,ast,json,runpy,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools.simulate import parse_instance,simulate,match_count
from tools.validate_output import validate_output

p=argparse.ArgumentParser()
p.add_argument('--cases',default='007,137,186,270')
p.add_argument('--width',type=int,default=128)
p.add_argument('--output',default='results/m2_sequence_packed_back_constructor.json')
args=p.parse_args()
base=ROOT/'solvers/experiments/m2_sequence_runtime_final.py'
lines=base.read_text().splitlines();tree=ast.parse('\n'.join(lines))
node=next(node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name=='seven_backward_construct')
source='\n'.join(lines[node.lineno-1:node.end_lineno])
rows=[]
for case in args.cases.split(','):
    cid='case_'+case.zfill(3)
    inst=parse_instance((ROOT/'cases/generated'/(cid+'.in')).read_text())
    row=dict(id=cid,n=inst.n,d=inst.d,c=inst.c,k=inst.k,width=args.width)
    outputs=[]
    for packed in (False,True):
        module=runpy.run_path(str(base))
        candidate_source=source
        if packed:
            exec((ROOT/'solvers/experiments/m2_sequence_packed_back.py').read_text(),module)
            candidate_source=source.replace('FastBack(', 'PackedFastBack(')
        exec(candidate_source,module)
        start=time.perf_counter();cpu_start=time.process_time()
        operations=module['seven_backward_construct'](inst.n,inst.d,inst.c,inst.k,inst.a[:],inst.t,inst.s[:],width=args.width)
        elapsed=time.perf_counter()-start;cpu=time.process_time()-cpu_start
        output=str(len(operations))+'\n'+'\n'.join(' '.join(map(str,a)) for a in operations)+'\n'
        validate_output(inst,output.encode())
        matches=match_count(inst,simulate(inst,operations)[0])
        outputs.append(operations)
        row['packed' if packed else 'original']=dict(matches=matches,runtime_sec=elapsed,cpu_sec=cpu)
    assert outputs[0]==outputs[1],cid
    rows.append(row);print(row,flush=True)
(ROOT/args.output).write_text(json.dumps(dict(config=vars(args),rows=rows),indent=2))
