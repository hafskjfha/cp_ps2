"""Additional exact shallow-prefix ceilings; no solver or benchmark changes."""
import collections
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.simulate import parse_instance, match_count
from tools.seven_bound_audit import TwoMoveOracle, summarize


def exact_prefix(ins, depth):
    oracle = TwoMoveOracle(ins)
    grid = ins.a[:]
    action_cells = [tuple(positions[i] for i in rotation) for positions in oracle.positions
                    for rotation in oracle.rotations]
    best = oracle.initial_best()
    visited = 0
    inventory = sum(min((ins.a+ins.s).count(c), ins.t.count(c)) for c in range(ins.c))
    area = ins.d**2
    target = ins.t
    def search(stamp, errors, current, left):
        nonlocal best, visited
        visited += 1
        best = max(best, current)
        if best >= inventory or current+left*area <= best:
            return
        if left == 1:
            best = max(best, current+oracle.max_next_gain(errors, stamp))
            return
        for cells in action_cells:
            outgoing = tuple(grid[pos] for pos in cells)
            next_errors = errors[:]
            delta = 0
            for i, pos in enumerate(cells):
                change = int(stamp[i] == target[pos])-int(grid[pos] == target[pos])
                delta += change
                grid[pos] = stamp[i]
                if change > 0:
                    oracle.subtract(next_errors, oracle.cover[pos])
                elif change < 0:
                    oracle.add(next_errors, oracle.cover[pos])
            search(outgoing, next_errors, current+delta, left-1)
            for pos, old in zip(cells, outgoing):
                grid[pos] = old
            if best >= inventory:
                break
    search(ins.s, oracle.error_planes, match_count(ins, grid), depth)
    assert grid == ins.a
    return best, visited


def main():
    started = time.perf_counter()
    data = json.loads((ROOT/'results/seven_bound_coverage.json').read_text())
    changes = []
    calculations = []
    for row in data['rows']:
        if not row['headroom'] or row['k'] < 3:
            continue
        actions = 4*(row['n']-row['d']+1)**2
        depth = min(row['k'], 4 if actions <= 36 else 3)
        if actions**(depth-1) > 100000:
            continue
        if row['upper_matches'] <= row['initial_matches']+(row['k']-depth)*row['d']**2:
            continue
        ins = parse_instance((ROOT/'cases/generated'/f"{row['id']}.in").read_text())
        before = time.perf_counter()
        optimum, visited = exact_prefix(ins, depth)
        upper = min(row['upper_matches'], optimum+(row['k']-depth)*row['d']**2)
        calculation = dict(id=row['id'], depth=depth, optimum=optimum, visited=visited,
                           runtime_sec=time.perf_counter()-before, old_upper=row['upper_matches'],
                           upper_matches=upper)
        calculations.append(calculation)
        print(calculation, flush=True)
        if upper < row['upper_matches']:
            calculation['reduction'] = row['upper_score']-1000000*upper//ins.n**2
            changes.append(calculation)
            row['upper_matches'] = upper
            row['bound_matches'][f'exact_{depth}_prefix'] = upper
            row['upper_score'] = 1000000*upper//ins.n**2
            row['headroom'] = row['upper_score']-row['score']
            assert row['headroom'] >= 0
    data.update(summarize(data['rows']))
    data['rows'].sort(key=lambda row: -row['headroom'])
    data['shallow_calculations'] = calculations
    data['shallow_elapsed_sec'] = time.perf_counter()-started
    # Group summaries are rederived below, including all prior tightenings.
    for field, buckets in data['breakdown'].items():
        for key in buckets:
            if field in ('family', 'd', 'c'):
                group = [r for r in data['rows'] if str(r[field]) == key]
            elif field == 'spare_budget':
                group = [r for r in data['rows'] if ('yes' if r['spare_operations'] else 'no') == key]
            elif field == 'n_bucket':
                group = [r for r in data['rows'] if ('3-9' if r['n'] < 10 else '10-19' if r['n'] < 20 else '20-30') == key]
            else:
                group = [r for r in data['rows'] if ('1-3' if r['k'] <= 3 else '4-10' if r['k'] <= 10 else '11-60' if r['k'] <= 60 else '61-180') == key]
            buckets[key] = summarize(group)
    (ROOT/'results/seven_bound_final.json').write_text(json.dumps(data, indent=2)+'\n')
    print('FINAL', {k: data[k] for k in ('upper_score', 'headroom', 'proven_optimal', 'shallow_elapsed_sec')})


if __name__ == '__main__':
    main()
