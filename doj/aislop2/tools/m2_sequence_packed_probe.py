"""Exact whole-constructor parity and timing of the private packed beam."""
import argparse,json,runpy,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools.simulate import parse_instance,simulate,match_count
from tools.validate_output import validate_output

p=argparse.ArgumentParser()
p.add_argument('--cases',default='041,117,201,261')
p.add_argument('--width',type=int,default=128)
p.add_argument('--five',action='store_true')
p.add_argument('--output',default='results/m2_sequence_packed_constructor.json')
args=p.parse_args()
source=(ROOT/'solvers/experiments/m2_construct_pipeline_fragment.py').read_text().split('_m2_constructor_previous_retained')[0]
source=source.replace('64',str(args.width))
rows=[]
for case in args.cases.split(','):
    cid='case_'+case.zfill(3)
    data=(ROOT/'cases/generated'/(cid+'.in')).read_text()
    inst=parse_instance(data)
    row=dict(id=cid,n=inst.n,d=inst.d,c=inst.c,k=inst.k,width=args.width)
    outputs=[]
    for packed in (False,True):
        module=runpy.run_path(str(ROOT/'solvers/experiments/m2_sequence_runtime_final.py'))
        candidate_source=source
        if packed:
            suffix='packed5_cluster' if args.five else 'packed_cluster'
            exec((ROOT/('solvers/experiments/m2_sequence_'+suffix+'.py')).read_text(),module)
            candidate_source=source.replace('ClusterState','Packed5ClusterState' if args.five else 'PackedClusterState').replace('clone_cluster_state','clone_packed5_cluster_state' if args.five else 'clone_packed_cluster_state').replace('million_choices','packed5_cluster_choices' if args.five else 'packed_cluster_choices')
        exec(candidate_source,module)
        start=time.perf_counter();cpu_start=time.process_time()
        operations=module['m2_quotient_construct'](inst.n,inst.d,inst.c,inst.k,inst.a[:],inst.t,inst.s[:])
        elapsed=time.perf_counter()-start;cpu=time.process_time()-cpu_start
        output=str(len(operations))+'\n'+'\n'.join(' '.join(map(str,a)) for a in operations)+'\n'
        validate_output(inst,output.encode())
        matches=match_count(inst,simulate(inst,operations)[0])
        outputs.append(operations)
        row['packed' if packed else 'original']=dict(matches=matches,runtime_sec=elapsed,cpu_sec=cpu)
    assert outputs[0]==outputs[1],cid
    rows.append(row);print(row,flush=True)
(ROOT/args.output).write_text(json.dumps(dict(config=vars(args),rows=rows),indent=2))
