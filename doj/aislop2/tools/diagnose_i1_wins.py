"""Replay benchmark wins and record block-beam coverage; diagnostic only."""
import argparse
import hashlib
import importlib.util
import inspect
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.simulate import Instance, parse_instance, simulate
from tools.validate_output import validate_output


def worker(solver, case):
    instance = parse_instance(case.read_text())
    spec = importlib.util.spec_from_file_location('i1_diagnostic', solver)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    original = module.i1_search_block
    traces = []

    def traced(n, d, initial, wanted, depth, width=8, node_budget=160000,
               seed=0, expand=None, reference=()):
        span = n-d+1
        ops = [(aid//4//span, aid//4%span, aid%4) for aid in reference]
        hypothetical = Instance(n, d, 6, 180, initial[:n*n], [0]*(n*n), initial[n*n:])
        grid, stamp = simulate(hypothetical, ops)
        before = sum(a == b for a, b in zip(grid+stamp, wanted))
        started = time.perf_counter()
        result = original(n, d, initial, wanted, depth, width, node_budget, seed, expand, reference)
        caller = inspect.currentframe().f_back.f_locals
        left, right = caller['left'], caller['right']
        parent_length = len(caller['best'])
        traces.append(dict(depth=depth, width=width, expansions=result[2],
                           left=left, right=right, parent_length=parent_length,
                           block_kind='suffix' if right == parent_length else 'internal',
                           runtime_sec=time.perf_counter()-started,
                           reference_score=before, candidate_score=result[1],
                           gain=result[1]-before,
                           scored_stamp_labels=sum(v != 6 for v in wanted[n*n:])))
        return result

    module.i1_search_block = traced
    started = time.perf_counter()
    operations = module.solve(instance.n, instance.d, instance.c, instance.k,
                              instance.a, instance.t, instance.s)
    # Match native print() newline translation, including CRLF on Windows.
    output = (os.linesep.join([str(len(operations))]+[' '.join(map(str, op)) for op in operations])+os.linesep).encode()
    validate_output(instance, output)
    grid, _ = simulate(instance, operations)
    matches = sum(a == b for a, b in zip(grid, instance.t))
    print(json.dumps(dict(matches=matches, score=1000000*matches//instance.n**2,
                          runtime_sec=time.perf_counter()-started,
                          output_sha256=hashlib.sha256(output).hexdigest(), traces=traces)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('solver', type=Path)
    parser.add_argument('--worker', type=Path)
    parser.add_argument('--benchmark', type=Path)
    parser.add_argument('--reference', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.worker:
        worker(args.solver.resolve(), args.worker.resolve())
        return
    benchmark = json.loads(args.benchmark.read_text())
    reference = {r['id']: r for r in json.loads(args.reference.read_text())['results']}
    metadata = {r['id']: r for r in json.loads((ROOT/'cases/manifest.json').read_text())['cases']}
    digest = hashlib.sha256(args.solver.read_bytes()).hexdigest()
    assert digest == benchmark['solver_sha256']
    rows = []
    for row in benchmark['results']:
        if row['score'] <= reference[row['id']]['score']:
            continue
        case = ROOT/metadata[row['id']]['path']
        assert hashlib.sha256(case.read_bytes()).hexdigest() == row['input_sha256']
        process = subprocess.run([sys.executable, '-I', '-B', str(Path(__file__).resolve()),
                                  str(args.solver.resolve()), '--worker', str(case)],
                                 capture_output=True, timeout=5, check=True)
        result = json.loads(process.stdout)
        result['id'] = row['id']
        result['identical_score'] = result['score'] == row['score']
        result['identical_output'] = result['output_sha256'] == row['output_sha256']
        assert result['identical_score'] and result['identical_output'], result
        rows.append(result)
        print(row['id'], 'reproduced', [(t['depth'],t['gain'],t['scored_stamp_labels'])
                                       for t in result['traces'] if t['gain']>0], flush=True)
    report = dict(diagnostic_only=True, solver_sha256=digest, passed=True, results=rows)
    args.output.write_text(json.dumps(report, indent=2)+'\n')


if __name__ == '__main__':
    main()
