"""Small-board diagnostic only; full stable validation is required for promotion."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools.benchmark import evaluate_case,summarize

solver=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'solvers/experiments/packed_late_weighted.py'
parent=json.loads((ROOT/'results/wildcard_suffix_fast_stable.json').read_text())
previous={r['id']:r for r in parent['results']}
manifest=json.loads((ROOT/'cases/manifest.json').read_text())
wide=len(sys.argv)>2 and sys.argv[2]=='partial9'
partial=len(sys.argv)>2 and sys.argv[2] in ('partial','partial9')
selected=[m for m in manifest['cases'] if
          (5<=m['n']<=9 if wide else m['n'] in (5,6) if partial else m['n']==4) and m['d']==3
          and (1<=m['n']**2-previous[m['id']]['matches']<=(8 if wide else 4) if partial
               else previous[m['id']]['matches']<16)
          and previous[m['id']]['operations']<m['k']]
rows=[]
for meta in selected:
    row=evaluate_case(solver,meta,5)
    row['delta']=row['score']-previous[row['id']]['score']
    rows.append(row)
    print(json.dumps(row),flush=True)
report=dict(diagnostic_only=True,**summarize(rows),results=rows)
(ROOT/f'results/{solver.stem}_diagnostic.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='results'}),flush=True)
