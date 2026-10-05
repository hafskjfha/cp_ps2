"""Run the normal smoke/stable/readiness gates and save a strict improvement."""
import argparse
import csv
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser()
p.add_argument('name')
p.add_argument('--description',required=True)
p.add_argument('--jobs',type=int,default=2)
args=p.parse_args()
source=ROOT/'solvers/experiments'/f'{args.name}.py'
if source.stat().st_size>100000:raise SystemExit('Source is oversized')
def run(arguments):
    subprocess.run([sys.executable,*arguments],cwd=ROOT,check=True)

with (ROOT/'notes/experiments.md').open('a',encoding='utf8') as f:
    f.write(f'\n\n### Qualification: {args.name}\nHypothesis: {args.description}. '
            f'Packed source {source.stat().st_size} bytes; fixed benchmark unchanged.\n')
reports={key:ROOT/'results'/f'{args.name}_{key}.json' for key in ('smoke','stable','readiness')}
run(['tools/benchmark.py',str(source),'--suite','smoke','--jobs','1','--output',str(reports['smoke'])])
run(['tools/benchmark.py',str(source),'--suite','stable','--jobs',str(args.jobs),'--output',str(reports['stable'])])
benchmark=json.loads(reports['stable'].read_text())
history=list(csv.DictReader((ROOT/'results/history.csv').open(newline='',encoding='utf8')))
delta=benchmark['total_score']-int(history[-1]['total_score'])
if delta<=0:
    with (ROOT/'notes/experiments.md').open('a',encoding='utf8') as f:
        f.write(f"Rejected: stable {benchmark['total_score']}, delta {delta:+}, max {benchmark['max_runtime_sec']:.3f}s.\n")
    raise SystemExit('No strict improvement; not promoted')
run(['tools/check_submission.py',str(source),'--random','12','--timeout','5','--output',str(reports['readiness'])])
run(['tools/checkpoint.py',str(source),str(reports['stable']),str(reports['readiness']),'--description',args.description])
shutil.copyfile(source,ROOT/'solvers/current.py')
best=json.loads((ROOT/'results/best.json').read_text())
with (ROOT/'notes/experiments.md').open('a',encoding='utf8') as f:
    f.write(f"Saved checkpoint {best['id']:03d}: stable {benchmark['total_score']}, delta {delta:+}, "
            f"all320 valid, max {benchmark['max_runtime_sec']:.3f}s, readiness20 valid; {best['file']}.\n")
print('QUALIFIED',best['id'],benchmark['total_score'],flush=True)
