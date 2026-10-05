"""Lightweight exact patch-statistic transport ceilings; diagnostic only."""
import collections
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.simulate import parse_instance, rotation_offsets


def best_matches(reference, masks, all_patterns, maximum):
    planes = [0]*4
    for j, color in enumerate(reference):
        carry = masks[j][color]
        for p in range(4):
            old = planes[p]
            planes[p] = old ^ carry
            carry &= old
            if not carry:
                break
    surviving = all_patterns
    value = 0
    for p in range(3, -1, -1):
        desirable = surviving & (planes[p] if maximum else ~planes[p])
        if desirable:
            surviving = desirable
            if maximum:
                value += 1 << p
        elif not maximum:
            value += 1 << p
    return value


def edge_histogram(values, width):
    counts = collections.Counter()
    for p, color in enumerate(values):
        if p % width < width-1:
            counts[tuple(sorted((color, values[p+1])))] += 1
        if p+width < len(values):
            counts[tuple(sorted((color, values[p+width])))] += 1
    return counts


def analyze(ins):
    n, d, q = ins.n, ins.d, ins.d**2
    target_patterns = set()
    source_patterns = set()
    offsets = [[a*n+b for a, b in rotation_offsets(d, r)] for r in range(4)]
    for x in range(n-d+1):
        for y in range(n-d+1):
            base = x*n+y
            source_patterns.add(tuple(ins.a[base+v] for v in offsets[0]))
            for rotation in offsets:
                target_patterns.add(tuple(ins.t[base+v] for v in rotation))
    target_patterns = sorted(target_patterns)
    masks = [[0]*ins.c for _ in range(q)]
    for rank, pattern in enumerate(target_patterns):
        for j, color in enumerate(pattern):
            masks[j][color] |= 1 << rank
    all_patterns = (1 << len(target_patterns))-1
    initial = sum(a == t for a, t in zip(ins.a, ins.t))
    entry = best_matches(ins.s, masks, all_patterns, True)
    overlap = 0
    for pattern in source_patterns:
        overlap = max(overlap, best_matches(pattern, masks, all_patterns, True))
        if overlap == q:
            break
    diameter = 0
    for pattern in target_patterns:
        diameter = max(diameter, q-best_matches(pattern, masks, all_patterns, False))
        if diameter == q:
            break
    initial_edges = edge_histogram(ins.a, n)+edge_histogram(ins.s, d)
    target_edges = edge_histogram(ins.t, n)
    histogram_deficit = sum(max(0, count-initial_edges[pair]) for pair, count in target_edges.items())
    max_boundary = 2*d*min(2, n-d)
    edge_wrong_lower = max(0, (histogram_deficit-max_boundary*ins.k+3)//4)
    return dict(initial_stamp_best_overlap=entry, initial_patch_max_overlap=overlap,
                target_patch_hamming_diameter=diameter, target_patch_patterns=len(target_patterns),
                source_patch_patterns=len(source_patterns), edge_histogram_deficit=histogram_deficit,
                boundary_edges_per_move=max_boundary,
                bounds=dict(repeat_contact_transport=min(n*n, initial+(q*ins.k+entry+(ins.k-1)*overlap)//2),
                            target_pattern_transport=min(n*n, initial+entry+(ins.k-1)*diameter),
                            edge_histogram=min(n*n, n*n-edge_wrong_lower)))


def main():
    start = time.perf_counter()
    data = json.loads((ROOT/'results/seven_bound_joint.json').read_text())
    rows = []
    changes = []
    for row in data['rows']:
        if not row['headroom']:
            continue
        ins = parse_instance((ROOT/'cases/generated'/f"{row['id']}.in").read_text())
        stats = analyze(ins)
        ceiling = min(row['upper_matches'], *stats['bounds'].values())
        assert ceiling >= row['matches']
        detail = dict(id=row['id'], n=ins.n, d=ins.d, c=ins.c, k=ins.k,
                      old_upper=row['upper_matches'], upper_matches=ceiling, **stats)
        rows.append(detail)
        if ceiling < row['upper_matches']:
            detail['reduction'] = row['upper_score']-1000000*ceiling//(ins.n*ins.n)
            changes.append(detail)
    reduction = sum(row['reduction'] for row in changes)
    report = dict(diagnostic_only=True, baseline_report='results/seven_bound_joint.json',
                  previous_upper_score=data['upper_score'], upper_score=data['upper_score']-reduction,
                  reduction=reduction, changes=changes, rows=rows,
                  elapsed_sec=time.perf_counter()-start)
    (ROOT/'results/seven_bound_transport.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'rows'}, indent=2))


if __name__ == '__main__':
    main()
