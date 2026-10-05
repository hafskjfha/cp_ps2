import argparse,json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from solvers.experiments.m2_construct_probe import load
from tools.simulate import parse_instance,simulate,match_count
from tools.validate_output import validate_output

def main():
    p=argparse.ArgumentParser();p.add_argument('--width',type=int,default=512);p.add_argument('--future',type=int,default=3)
    p.add_argument('--suite',default='dev');p.add_argument('--limit',type=int,default=100)
    p.add_argument('--ids',default='');a=p.parse_args()
    m=load('base','solvers/experiments/m2_sequence_runtime_final.py');exec((ROOT/'solvers/experiments/m2_sequence_packed_cluster.py').read_text(),m.__dict__)
    exp=load('small','solvers/experiments/m2_construct_small_beam.py')
    floor={r['id']:r for r in json.loads((ROOT/'results/checkpoints/best_056_255006286.benchmark.json').read_text())['results']}
    report=dict(settings=vars(a),cases=[],diagnostic_only=True)
    dest=ROOT/('results/m2_construct_small_w%d_f%d_%s.json'%(a.width,a.future,a.suite))
    for meta in json.loads((ROOT/'cases/manifest.json').read_text())['cases']:
        if a.suite not in meta['suites']:continue
        if a.ids and meta['id']not in a.ids.split(','):continue
        ins=parse_instance((ROOT/meta['path']).read_text());old=floor[meta['id']]
        if not(4<=ins.n<=9 and 3<=ins.k<=12):continue
        if old['matches']==m.color_bound(ins.a+ins.s,ins.t):continue
        start=time.perf_counter();out,nodes=exp.construct(m,ins.n,ins.d,ins.c,ins.k,ins.a,ins.t,ins.s,a.width,a.future)
        runtime=time.perf_counter()-start
        encoded=(str(len(out))+'\n'+'\n'.join(' '.join(map(str,op))for op in out)+'\n').encode();validate_output(ins,encoded)
        matches=match_count(ins,simulate(ins,out)[0]);delta=1000000*max(matches,old['matches'])//ins.n**2-old['score']
        report['cases'].append(dict(id=meta['id'],n=ins.n,d=ins.d,c=ins.c,k=ins.k,parent=old['matches'],matches=matches,delta=delta,raw_delta=matches-old['matches'],runtime_sec=runtime,expansions=nodes,operations=out))
        report.update(total_delta=sum(r['delta']for r in report['cases']),wins=sum(r['delta']>0 for r in report['cases']),runtime_sec=sum(r['runtime_sec']for r in report['cases']),max_runtime_sec=max(r['runtime_sec']for r in report['cases']))
        dest.write_text(json.dumps(report));print(meta['id'],matches,old['matches'],delta,round(runtime,3),nodes,flush=True)
        if len(report['cases'])>=a.limit:break
    print({k:v for k,v in report.items()if k!='cases'},flush=True)
if __name__=='__main__':main()
