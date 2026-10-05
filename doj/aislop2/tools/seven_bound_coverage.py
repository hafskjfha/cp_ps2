"""Integer-checked weighted maximum-coverage upper-bound certificates."""
import collections
import heapq
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.simulate import parse_instance
from tools.seven_bound_audit import summarize


def weighted_cover(ins, ceiling, scale=8):
    wrong = [i for i, (a, t) in enumerate(zip(ins.a, ins.t)) if a != t]
    initial = ins.n**2-len(wrong)
    lookup = {pos: i for i, pos in enumerate(wrong)}
    patches = []
    cover = [[] for _ in wrong]
    for x in range(ins.n-ins.d+1):
        for y in range(ins.n-ins.d+1):
            patch = [lookup[(x+p)*ins.n+y+q] for p in range(ins.d) for q in range(ins.d)
                     if (x+p)*ins.n+y+q in lookup]
            for cell in patch:
                cover[cell].append(len(patches))
            patches.append(patch)
    saved = None
    for threshold in range(1, scale*ins.d**2):
        if initial+ins.k*threshold//scale >= ceiling:
            continue
        weights = [scale]*len(wrong)
        counts = [scale*len(patch) for patch in patches]
        active = [count > threshold for count in counts]
        degrees = [sum(active[j] for j in surrounding) for surrounding in cover]
        heap = [(-deg, i) for i, deg in enumerate(degrees) if deg]
        heapq.heapify(heap)
        removed = 0
        while heap:
            negative, cell = heapq.heappop(heap)
            if not weights[cell] or -negative != degrees[cell]:
                continue
            relevant = [j for j in cover[cell] if active[j]]
            assert relevant
            delta = min(weights[cell], min(counts[j]-threshold for j in relevant))
            weights[cell] -= delta
            removed += delta
            for patchid in cover[cell]:
                counts[patchid] -= delta
                if active[patchid] and counts[patchid] <= threshold:
                    active[patchid] = False
                    for neighbor in patches[patchid]:
                        degrees[neighbor] -= 1
                        if weights[neighbor] and degrees[neighbor]:
                            heapq.heappush(heap, (-degrees[neighbor], neighbor))
            if weights[cell] and degrees[cell]:
                heapq.heappush(heap, (-degrees[cell], cell))
        # The heuristic above only proposes a certificate. These exact integer
        # calculations establish its validity independently of that heuristic.
        actual_max = max(sum(weights[cell] for cell in patch) for patch in patches)
        assert max(counts) == actual_max <= threshold
        removed = sum(scale-w for w in weights)
        upper = initial+(ins.k*actual_max+removed)//scale
        if upper < ceiling:
            ceiling = upper
            saved = dict(scale=scale, weights=list(zip(wrong, weights)),
                         max_patch_weight=actual_max, removed_weight=removed,
                         numerator=ins.k*actual_max+removed, upper_matches=upper)
    return ceiling, saved


def main():
    started = time.perf_counter()
    data = json.loads((ROOT/'results/seven_bound_audit.json').read_text())
    changes = []
    for row in data['rows']:
        if not row['headroom']:
            continue
        ins = parse_instance((ROOT/'cases/generated'/f"{row['id']}.in").read_text())
        upper, cert = weighted_cover(ins, row['upper_matches'])
        if upper < row['upper_matches']:
            changes.append(dict(id=row['id'], old_upper=row['upper_matches'], upper_matches=upper,
                                reduction=row['upper_score']-1000000*upper//ins.n**2,
                                certificate=cert))
            row['upper_matches'] = upper
            row['bound_matches']['weighted_coverage'] = upper
            row['upper_score'] = 1000000*upper//ins.n**2
            row['headroom'] = row['upper_score']-row['score']
            assert row['headroom'] >= 0
    data.update(summarize(data['rows']))
    data['rows'].sort(key=lambda row: -row['headroom'])
    data['coverage_certificates'] = changes
    data['coverage_elapsed_sec'] = time.perf_counter()-started
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
    (ROOT/'results/seven_bound_coverage.json').write_text(json.dumps(data, indent=2)+'\n')
    print('upper', data['upper_score'], 'headroom', data['headroom'], 'optimal', data['proven_optimal'],
          'time', data['coverage_elapsed_sec'])
    print('changes', [(c['id'], c['old_upper'], c['upper_matches'], c['reduction']) for c in changes])


if __name__ == '__main__':
    main()
