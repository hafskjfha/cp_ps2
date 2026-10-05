"""Bounded diagnostic subset; not a qualifying stable benchmark."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.benchmark import evaluate_case, summarize


def main():
    manifest = json.loads((ROOT/'cases/manifest.json').read_text())
    baseline = json.loads((ROOT/'results/anneal_informed_cached_stable.json').read_text())
    previous = {row['id']: row for row in baseline['results']}
    selected = [meta for meta in manifest['cases']
                if meta['k'] == 3 and meta['d'] == 3]
    rows = []
    for meta in selected:
        row = evaluate_case(ROOT/'solvers/experiments/exact_three_d2.py', meta, 5)
        row['baseline_score'] = previous[row['id']]['score']
        row['delta'] = row['score'] - row['baseline_score']
        rows.append(row)
        print(json.dumps(row), flush=True)
    report = dict(diagnostic_only=True, **summarize(rows), results=rows)
    (ROOT/'results/exact_three_d3_diagnostic.json').write_text(json.dumps(report, indent=2))
    print(json.dumps({k: v for k, v in report.items() if k != 'results'}), flush=True)


if __name__ == '__main__':
    main()
