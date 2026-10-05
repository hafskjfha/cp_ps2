"""Repeat the slowest cases from two frozen reports using canonical validation."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.benchmark import evaluate_case, summarize


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('solver', type=Path)
    parser.add_argument('--selection', type=Path, required=True)
    parser.add_argument('--reference', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--count', type=int, default=12)
    parser.add_argument('--repeat', type=int, default=3)
    parser.add_argument('--timeout', type=float, default=5)
    args = parser.parse_args()
    if args.count < 1 or args.repeat < 1 or not 0 < args.timeout <= 5:
        parser.error('positive count/repeat and timeout <= 5 required')
    source = args.solver.read_bytes()
    digest = hashlib.sha256(source).hexdigest()
    manifest_data = (ROOT / 'cases/manifest.json').read_bytes()
    manifest_digest = hashlib.sha256(manifest_data).hexdigest()
    selection = json.loads(args.selection.read_text())
    reference = json.loads(args.reference.read_text())
    assert reference['solver_sha256'] == digest
    assert selection['manifest_sha256'] == reference['manifest_sha256'] == manifest_digest
    assert not reference['invalid']
    expected = {row['id']: row for row in reference['results']}
    meta = {row['id']: row for row in json.loads(manifest_data)['cases']}
    selected = sorted(selection['results'], key=lambda row: row['runtime_sec'], reverse=True)
    current = sorted(reference['results'], key=lambda row: row['runtime_sec'], reverse=True)
    ids = list(dict.fromkeys(row['id'] for row in selected[:args.count] + current[:args.count]))
    ids += [selected[0]['id']] * args.repeat
    rows = []
    report = dict(solver=str(args.solver), solver_sha256=digest,
                  manifest_sha256=manifest_digest, timeout_sec=args.timeout, jobs=1,
                  selection=str(args.selection), reference=str(args.reference),
                  selection_rule=f'Union of {args.count} slowest cases from each report, '
                                 f'then {args.repeat} repeats of original slowest',
                  results=rows)
    with tempfile.TemporaryDirectory(prefix='stamp-repeat-') as directory:
        snapshot = Path(directory) / args.solver.name
        snapshot.write_bytes(source)
        for identifier in ids:
            row = evaluate_case(snapshot, meta[identifier], args.timeout)
            row['identical_output'] = row.get('output_sha256') == expected[identifier]['output_sha256']
            row['identical_score'] = row['score'] == expected[identifier]['score']
            rows.append(row)
            print(identifier, row['valid'], round(row['runtime_sec'], 3),
                  'identical=' + str(row['identical_output']), flush=True)
    report.update(summarize(rows))
    report['source_unchanged'] = hashlib.sha256(args.solver.read_bytes()).hexdigest() == digest
    report['passed'] = (not report['invalid'] and report['source_unchanged']
                        and all(row['identical_score'] and row['identical_output'] for row in rows))
    args.output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('PASS' if report['passed'] else 'FAIL', len(rows), 'cases; max', report['max_runtime_sec'])
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
