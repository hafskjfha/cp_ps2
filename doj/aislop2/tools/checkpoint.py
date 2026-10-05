"""Promote only verified strict improvements; never overwrite a checkpoint."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OFFICIAL_TIMEOUT = 5.0


def require_runtime(evidence, label):
    for field in ('timeout_sec', 'max_runtime_sec'):
        value = evidence.get(field)
        if not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= OFFICIAL_TIMEOUT:
            raise ValueError(f'{label} {field} must be at most the official 5-second limit')
    if evidence['timeout_sec'] <= 0:
        raise ValueError(f'{label} timeout must be positive')


def validate_benchmark(benchmark):
    """Check the actual case rows, not only a report's aggregate counters."""
    if benchmark['suite'] != 'stable' or benchmark['cases'] != 320 or benchmark['invalid']:
        raise ValueError('full valid 320-case stable benchmark required')
    require_runtime(benchmark, 'benchmark')
    results = benchmark.get('results', [])
    if len(results) != 320 or any(not row.get('valid') for row in results):
        raise ValueError('all 320 stable case results must be present and valid')
    identifiers = [row['id'] for row in results]
    if len(set(identifiers)) != 320:
        raise ValueError('stable case IDs must be unique')
    for row in results:
        if not isinstance(row.get('input_sha256'), str) or not row['input_sha256']:
            raise ValueError('every stable result must record its input hash')
        if type(row['score']) is not int or not 0 <= row['score'] <= 1000000:
            raise ValueError('case score is outside the official range')
        if row['total_cells'] <= 0 or not 0 <= row['matches'] <= row['total_cells']:
            raise ValueError('case match count is invalid')
        if row['score'] != 1000000 * row['matches'] // row['total_cells']:
            raise ValueError('case score differs from the official formula')
        runtime = row['runtime_sec']
        if not math.isfinite(runtime) or not 0 <= runtime <= OFFICIAL_TIMEOUT:
            raise ValueError('case runtime exceeds the official 5-second limit')
    total = sum(row['score'] for row in results)
    if benchmark['total_score'] != total or not math.isclose(benchmark['avg_score'], total / 320, abs_tol=1e-9):
        raise ValueError('benchmark total/average differs from its case results')
    if benchmark['max_runtime_sec'] + 1e-9 < max(row['runtime_sec'] for row in results):
        raise ValueError('benchmark maximum runtime understates its case results')
    return sorted((row['id'], row['input_sha256']) for row in results)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('solver', type=Path)
    parser.add_argument('benchmark', type=Path)
    parser.add_argument('readiness', type=Path)
    parser.add_argument('--description', required=True)
    args = parser.parse_args()
    data = args.solver.read_bytes()
    if len(data)>100000:
        parser.error('submitted source exceeds the official 100,000-byte limit')
    digest = hashlib.sha256(data).hexdigest()
    benchmark = json.loads(args.benchmark.read_text())
    readiness = json.loads(args.readiness.read_text())
    try:
        if benchmark['solver_sha256'] != digest:
            raise ValueError('benchmark does not describe current solver bytes')
        case_signature = validate_benchmark(benchmark)
        if not readiness.get('passed') or readiness.get('solver_sha256') != digest:
            raise ValueError('passing readiness report for current solver bytes required')
        require_runtime(readiness, 'readiness')
    except (KeyError, TypeError, ValueError) as exc:
        parser.error(str(exc))
    directory = ROOT / 'submissions'
    directory.mkdir(exist_ok=True)
    history = ROOT / 'results/history.csv'
    if history.exists():
        with history.open(newline='', encoding='utf-8') as stream:
            rows = list(csv.DictReader(stream))
    else:
        rows = []
    if rows and benchmark['manifest_sha256'] != rows[-1]['manifest_sha256']:
        parser.error('stable benchmark manifest changed')
    if rows and benchmark['total_score'] <= int(rows[-1]['total_score']):
        parser.error('not a strict improvement')
    if rows:
        try:
            previous = json.loads((ROOT / rows[-1]['benchmark']).read_text(encoding='utf-8'))
            if previous['solver_sha256'] != rows[-1]['solver_sha256'] or previous['manifest_sha256'] != rows[-1]['manifest_sha256']:
                raise ValueError('previous checkpoint benchmark evidence was overwritten')
            if validate_benchmark(previous) != case_signature:
                raise ValueError('stable benchmark case IDs or input hashes changed')
        except (OSError, KeyError, TypeError, ValueError) as exc:
            parser.error(str(exc))
    index = len(rows)
    filename = 'best_000_initial.py' if not rows else 'best_%03d_%d.py' % (index, benchmark['total_score'])
    destination = directory / filename
    evidence_directory = ROOT / 'results/checkpoints'
    benchmark_copy = evidence_directory / (destination.stem + '.benchmark.json')
    readiness_copy = evidence_directory / (destination.stem + '.readiness.json')
    if any(path.exists() for path in (destination, benchmark_copy, readiness_copy)):
        parser.error('checkpoint or immutable evidence path already exists')
    evidence_directory.mkdir(parents=True, exist_ok=True)
    for path, evidence in ((benchmark_copy, benchmark), (readiness_copy, readiness)):
        with path.open('x', encoding='utf-8') as stream:
            json.dump(evidence, stream, indent=2)
            stream.write('\n')
    with destination.open('xb') as stream:
        stream.write(data)
    record = dict(id=index, total_score=benchmark['total_score'], avg_score=benchmark['avg_score'],
                  runtime_sec=benchmark['runtime_sec'], max_runtime_sec=benchmark['max_runtime_sec'],
                  description=args.description, file='submissions/'+filename, solver_sha256=digest,
                  manifest_sha256=benchmark['manifest_sha256'], benchmark=benchmark_copy.relative_to(ROOT).as_posix(),
                  readiness=readiness_copy.relative_to(ROOT).as_posix())
    with history.open('a', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(record))
        if not rows:
            writer.writeheader()
        writer.writerow(record)
    (ROOT/'results/best.json').write_text(json.dumps(record, indent=2)+'\n')
    print(destination)


if __name__ == '__main__':
    main()
