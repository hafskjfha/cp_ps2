"""Proof-based diagnostic ceilings for the unchanged 320-case benchmark.

This is not a submission or improvement claim. Only diagnostic reports change.
"""
import collections
import hashlib
import json
from pathlib import Path
import random
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.simulate import Instance, match_count, parse_instance, rotation_offsets, simulate


class TwoMoveOracle:
    """Exhaustive two-move optimum, with bit-sliced parallel second moves."""
    def __init__(self, ins):
        self.ins = ins
        n, d, c = ins.n, ins.d, ins.c
        self.width = width = n - d + 1
        self.count = width * width
        self.all = (1 << self.count) - 1
        self.target_masks = [[0] * c for _ in range(d*d)]
        self.cover = [0] * (n*n)
        self.positions = []
        self.rotations = [[p*d+q for p, q in rotation_offsets(d, r)] for r in range(4)]
        self.error_planes = [0] * 5
        for x in range(width):
            for y in range(width):
                bit = 1 << (x*width+y)
                positions = [(x+p)*n+y+q for p in range(d) for q in range(d)]
                self.positions.append(positions)
                wrong = sum(ins.a[pos] != ins.t[pos] for pos in positions)
                for j in range(5):
                    if wrong & (1 << j):
                        self.error_planes[j] |= bit
                for j, pos in enumerate(positions):
                    self.target_masks[j][ins.t[pos]] |= bit
                    self.cover[pos] |= bit

    @staticmethod
    def add(planes, mask):
        for j in range(5):
            old = planes[j]
            planes[j] = old ^ mask
            mask &= old
            if not mask:
                return
        assert not mask

    @staticmethod
    def subtract(planes, mask):
        for j in range(5):
            old = planes[j]
            planes[j] = old ^ mask
            mask &= ~old
            if not mask:
                return
        assert not mask

    def max_next_gain(self, error_planes, stamp):
        best = -self.ins.d**2
        for rotation in self.rotations:
            planes = error_planes[:]
            for j, natural in enumerate(rotation):
                self.add(planes, self.target_masks[natural][stamp[j]])
            available = self.all
            value = 0
            for j in range(4, -1, -1):
                candidates = available & planes[j]
                if candidates:
                    value += 1 << j
                    available = candidates
            best = max(best, value-self.ins.d**2)
        return best

    def initial_best(self):
        initial = match_count(self.ins, self.ins.a)
        return max(initial, initial+self.max_next_gain(self.error_planes, self.ins.s))

    def best(self):
        ins = self.ins
        initial = match_count(ins, ins.a)
        best = self.initial_best()
        for positions in self.positions:
            for rotation in self.rotations:
                errors = self.error_planes[:]
                delta = 0
                stamp = []
                for j, natural in enumerate(rotation):
                    pos = positions[natural]
                    old, new, target = ins.a[pos], ins.s[j], ins.t[pos]
                    stamp.append(old)
                    change = int(new == target) - int(old == target)
                    delta += change
                    if change > 0:
                        self.subtract(errors, self.cover[pos])
                    elif change < 0:
                        self.add(errors, self.cover[pos])
                best = max(best, initial+delta+self.max_next_gain(errors, stamp))
        return best


def verify():
    rng = random.Random(76113081)
    checked = 0
    for n, d in [(3, 2), (3, 3), (4, 2), (4, 3), (5, 3), (6, 2)]:
        for _ in range(3):
            c = rng.randint(2, 6)
            ins = Instance(n, d, c, 2, *[[rng.randrange(c) for _ in range(size)]
                                        for size in (n*n, n*n, d*d)])
            moves = [(x, y, r) for x in range(n-d+1) for y in range(n-d+1) for r in range(4)]
            brute = match_count(ins, ins.a)
            brute_one = brute
            for op in moves:
                grid, _ = simulate(ins, [op])
                brute_one = max(brute_one, match_count(ins, grid))
                for op2 in moves:
                    grid, _ = simulate(ins, [op, op2])
                    brute = max(brute, match_count(ins, grid))
                    checked += 1
            oracle = TwoMoveOracle(ins)
            assert oracle.initial_best() == brute_one
            assert oracle.best() == max(brute, brute_one)
    return dict(random_cases=18, canonical_two_move_sequences=checked)


def summarize(rows):
    return dict(cases=len(rows), score=sum(r['score'] for r in rows),
                upper_score=sum(r['upper_score'] for r in rows),
                headroom=sum(r['headroom'] for r in rows),
                proven_optimal=sum(r['headroom'] == 0 for r in rows))


def main():
    started = time.perf_counter()
    verification = verify()
    manifest_bytes = (ROOT/'cases/manifest.json').read_bytes()
    manifest = json.loads(manifest_bytes)
    best = json.loads((ROOT/'results/best.json').read_text())
    benchmark = json.loads((ROOT/best['benchmark']).read_text())
    assert best['total_score'] == benchmark['total_score'] == 254103898
    assert hashlib.sha256(manifest_bytes).hexdigest() == benchmark['manifest_sha256']
    assert hashlib.sha256((ROOT/best['file']).read_bytes()).hexdigest() == benchmark['solver_sha256']
    measured = {r['id']: r for r in benchmark['results']}
    rows = []
    for meta in manifest['cases']:
        if 'stable' not in meta['suites']:
            continue
        case_bytes = (ROOT/meta['path']).read_bytes()
        assert hashlib.sha256(case_bytes).hexdigest() == meta['sha256']
        ins = parse_instance(case_bytes.decode('ascii'))
        oracle = TwoMoveOracle(ins)
        initial = match_count(ins, ins.a)
        pool = collections.Counter(ins.a+ins.s)
        target = collections.Counter(ins.t)
        inventory = sum(min(pool[c], target[c]) for c in target)
        first = oracle.initial_best()
        occupancy = sorted((sum(ins.a[p] != ins.t[p] for p in positions)
                            for positions in oracle.positions), reverse=True)
        bounds = dict(inventory=inventory, touched_cells=min(ins.n**2, initial+ins.k*ins.d**2),
                      union_coverage=min(ins.n**2, initial+sum(occupancy[:ins.k])),
                      one_move_prefix=min(ins.n**2, first+(ins.k-1)*ins.d**2))
        second = None
        if ins.n == ins.d:
            exact = first
            if ins.k >= 2:
                for r in range(4):
                    grid, _ = simulate(ins, [(0, 0, 0), (0, 0, r)])
                    exact = max(exact, match_count(ins, grid))
            bounds['whole_board_exact'] = exact
        elif ins.k >= 2 and min(bounds.values()) > initial+(ins.k-2)*ins.d**2:
            second = oracle.best()
            bounds['two_move_prefix'] = min(ins.n**2, second+(ins.k-2)*ins.d**2)
        upper = min(bounds.values())
        obs = measured[meta['id']]
        assert obs['valid'] and obs['matches'] <= upper, (meta['id'], obs['matches'], upper)
        row = {key: meta[key] for key in ('id', 'family', 'n', 'd', 'c', 'k')}
        row.update(initial_matches=initial, matches=obs['matches'], score=obs['score'],
                   operations=obs['operations'], spare_operations=ins.k-obs['operations'],
                   upper_matches=upper, upper_score=1000000*upper//ins.n**2,
                   bound_matches=bounds, one_move_optimum=first, two_move_optimum=second,
                   runtime_sec=obs['runtime_sec'])
        row['headroom'] = row['upper_score']-row['score']
        row['unmatched_recoverable_ceiling'] = upper-obs['matches']
        rows.append(row)
    groups = {}
    for key in ('family', 'd', 'c', 'n_bucket', 'k_bucket', 'spare_budget'):
        buckets = collections.defaultdict(list)
        for row in rows:
            if key == 'n_bucket':
                bucket = '3-9' if row['n'] < 10 else '10-19' if row['n'] < 20 else '20-30'
            elif key == 'k_bucket':
                bucket = '1-3' if row['k'] <= 3 else '4-10' if row['k'] <= 10 else '11-60' if row['k'] <= 60 else '61-180'
            elif key == 'spare_budget':
                bucket = 'yes' if row['spare_operations'] > 0 else 'no'
            else:
                bucket = str(row[key])
            buckets[bucket].append(row)
        groups[key] = {k: summarize(v) for k, v in sorted(buckets.items())}
    result = dict(diagnostic_only=True, proofs='notes/seven_bound.md',
                  baseline=best['file'], baseline_sha256=benchmark['solver_sha256'],
                  manifest_sha256=benchmark['manifest_sha256'], verification=verification,
                  target_score=261103898, **summarize(rows), breakdown=groups,
                  elapsed_sec=time.perf_counter()-started,
                  rows=sorted(rows, key=lambda row: -row['headroom']))
    (ROOT/'results/seven_bound_audit.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({key: value for key, value in result.items() if key != 'rows'}, indent=2))
    print('TOP REMAINING:')
    for row in result['rows'][:35]:
        print(row['id'], row['family'], 'N/D/C/K', row['n'], row['d'], row['c'], row['k'],
              'matches', row['matches'], '/', row['upper_matches'], 'gap', row['headroom'])


if __name__ == '__main__':
    main()
