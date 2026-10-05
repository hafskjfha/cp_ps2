"""Joint color-inventory and visited-patch coverage certificates.

All certificates are checked with integer arithmetic; greedy optimization only
selects which valid certificate to try.
"""
import heapq
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.simulate import parse_instance
from tools.seven_bound_audit import summarize


def joint_certificate(ins, ceiling, scale=1, selected=None):
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
    potentials = selected if selected is not None else range(1, (1 << ins.c)-1)
    for color_mask in potentials:
        potential = [(color_mask >> c) & 1 for c in range(ins.c)]
        constant = sum(potential[c] for c in ins.s)
        if initial+constant >= ceiling:
            continue
        base = [scale*(1-potential[ins.t[pos]]+potential[ins.a[pos]]) for pos in wrong]
        starting_counts = [sum(base[cell] for cell in patch) for patch in patches]
        simple = initial+constant+min(sum(base), sum(sorted(starting_counts, reverse=True)[:ins.k]))//scale
        if simple < ceiling:
            ceiling = simple
            saved = dict(color_mask=color_mask, scale=scale, weights=list(zip(wrong, base)),
                         max_patch_weight=max(starting_counts), removed_weight=0,
                         constant=constant, upper_matches=simple, kind='top_k')
        for threshold in range(0, max(starting_counts)+1):
            if initial+constant+ins.k*threshold//scale >= ceiling:
                continue
            weights = base[:]
            counts = starting_counts[:]
            active = [count > threshold for count in counts]
            degrees = [sum(active[j] for j in surrounding) for surrounding in cover]
            heap = [(-deg, i) for i, deg in enumerate(degrees) if deg and weights[i]]
            heapq.heapify(heap)
            while heap:
                negative, cell = heapq.heappop(heap)
                if not weights[cell] or -negative != degrees[cell]:
                    continue
                relevant = [j for j in cover[cell] if active[j]]
                assert relevant
                delta = min(weights[cell], min(counts[j]-threshold for j in relevant))
                weights[cell] -= delta
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
            maximum = max(sum(weights[cell] for cell in patch) for patch in patches)
            assert max(counts) == maximum <= threshold
            removed = sum(b-w for b, w in zip(base, weights))
            upper = initial+constant+(ins.k*maximum+removed)//scale
            if upper < ceiling:
                ceiling = upper
                saved = dict(color_mask=color_mask, scale=scale, weights=list(zip(wrong, weights)),
                             max_patch_weight=maximum, removed_weight=removed,
                             constant=constant, upper_matches=upper, kind='weighted')
    return ceiling, saved


def main():
    started = time.perf_counter()
    data = json.loads((ROOT/'results/seven_bound_final.json').read_text())
    changes = []
    searched = 0
    for row in data['rows']:
        if not row['headroom'] or row['k'] >= ((row['n']+row['d']-1)//row['d'])**2:
            continue
        ins = parse_instance((ROOT/'cases/generated'/f"{row['id']}.in").read_text())
        upper, cert = joint_certificate(ins, row['upper_matches'])
        searched += 1
        if upper < row['upper_matches']:
            extra_upper, extra_cert = joint_certificate(ins, upper, 8, [cert['color_mask']])
            if extra_upper < upper:
                upper, cert = extra_upper, extra_cert
            change = dict(id=row['id'], old_upper=row['upper_matches'], upper_matches=upper,
                          reduction=row['upper_score']-1000000*upper//ins.n**2, certificate=cert)
            print({k: v for k, v in change.items() if k != 'certificate'}, flush=True)
            changes.append(change)
            row['upper_matches'] = upper
            row['bound_matches']['joint_inventory_coverage'] = upper
            row['upper_score'] = 1000000*upper//ins.n**2
            row['headroom'] = row['upper_score']-row['score']
            assert row['headroom'] >= 0
    data.update(summarize(data['rows']))
    data['rows'].sort(key=lambda row: -row['headroom'])
    data['joint_certificates'] = changes
    data['joint_elapsed_sec'] = time.perf_counter()-started
    # Recalculate group summaries consistently with the other bound stages.
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
    (ROOT/'results/seven_bound_joint.json').write_text(json.dumps(data, indent=2)+'\n')
    print('upper', data['upper_score'], 'headroom', data['headroom'], 'optimal', data['proven_optimal'],
          'searched', searched, 'time', data['joint_elapsed_sec'], flush=True)


if __name__ == '__main__':
    main()
