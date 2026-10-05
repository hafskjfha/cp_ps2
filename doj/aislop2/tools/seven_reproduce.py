"""Repeat changed benchmark outputs through canonical evaluation."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import tempfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools.benchmark import evaluate_case

p=argparse.ArgumentParser()
p.add_argument('solver',type=Path)
p.add_argument('benchmark',type=Path)
p.add_argument('--baseline',type=Path,default=ROOT/'results/checkpoints/runtime_053_254103898.benchmark.json')
p.add_argument('--output',type=Path,required=True)
args=p.parse_args()
data=args.solver.read_bytes();digest=hashlib.sha256(data).hexdigest()
bench=json.loads(args.benchmark.read_text())
assert digest==bench['solver_sha256']
old={r['id']:r for r in json.loads(args.baseline.read_text())['results']}
new={r['id']:r for r in bench['results']}
metadata=json.loads((ROOT/'cases/manifest.json').read_text())['cases']
rows=[]
with tempfile.TemporaryDirectory(prefix='stamp-reproduce-')as directory:
    snapshot=Path(directory)/args.solver.name;snapshot.write_bytes(data)
    for meta in metadata:
        expected=new[meta['id']]
        if expected['score']==old[meta['id']]['score']:continue
        row=evaluate_case(snapshot,meta,5)
        row['reproduced']=row['valid']and row['score']==expected['score']and row['output_sha256']==expected['output_sha256']
        rows.append(row)
        print(meta['id'],row['reproduced'],round(row['runtime_sec'],3),flush=True)
report=dict(solver_sha256=digest,passed=all(r['reproduced']for r in rows),cases=len(rows),max_runtime_sec=max((r['runtime_sec']for r in rows),default=0),results=rows)
args.output.write_text(json.dumps(report,indent=2)+'\n')
print('PASS'if report['passed']else'FAIL','reproduced',len(rows),'changed cases',flush=True)
raise SystemExit(0 if report['passed']else 1)
