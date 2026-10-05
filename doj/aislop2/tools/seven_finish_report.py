"""Write the campaign report from verified immutable checkpoint evidence."""
import csv
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def read(path):return json.loads((ROOT/path).read_text(encoding='utf8'))

def summarize_bound(parent,transport,baseline,benchmark):
    """Merge the latest tightening and verify all 320 official-score ceilings."""
    starting={row['id']:row for row in baseline['results']}
    selected={row['id']:row for row in benchmark['results']}
    rows={row['id']:dict(row) for row in parent['rows']}
    assert len(rows)==len(parent['rows'])==320
    assert set(rows)==set(starting)==set(selected)
    assert parent['baseline_sha256']==baseline['solver_sha256']
    assert parent['manifest_sha256']==baseline['manifest_sha256']
    assert parent['score']==baseline['total_score']
    assert transport['previous_upper_score']==parent['upper_score']
    assert sum(row['upper_score'] for row in rows.values())==parent['upper_score']
    expected={key for key,row in rows.items() if row['headroom']>0}
    seen=set()
    for update in transport['rows']:
        key=update['id']
        assert key not in seen
        seen.add(key)
        row=rows[key]
        assert update['old_upper']==row['upper_matches']
        assert update['upper_matches']==min(row['upper_matches'],*update['bounds'].values())
        assert type(update['upper_matches']) is int
        row['upper_matches']=update['upper_matches']
        row['upper_score']=1000000*row['upper_matches']//starting[key]['total_cells']
    assert seen==expected
    for key,row in rows.items():
        cells=starting[key]['total_cells']
        assert cells==selected[key]['total_cells']==row['n']**2
        assert 0<=starting[key]['matches']<=row['upper_matches']<=cells
        assert 0<=selected[key]['matches']<=row['upper_matches']
        assert row['upper_score']==1000000*row['upper_matches']//cells
    upper=sum(row['upper_score'] for row in rows.values())
    assert upper==transport['upper_score']
    assert parent['upper_score']-upper==transport['reduction']
    return dict(upper_score=upper,headroom=upper-baseline['total_score'],
                selected_headroom=upper-benchmark['total_score'],
                baseline_proven_optimal=sum(row['upper_matches']==starting[key]['matches']
                                            for key,row in rows.items()),
                selected_proven_optimal=sum(row['upper_matches']==selected[key]['matches']
                                            for key,row in rows.items()))

best=read('results/best.json')
benchmark=read(best['benchmark'])
readiness=read(best['readiness'])
stress=read(best['stress'])
periodic=read(best['periodic'])
reproduction=read(best['reproduction'])
baseline=read('results/checkpoints/runtime_053_254103898.benchmark.json')
bound_path='results/seven_bound_transport.json'
bound_transport=read(bound_path)
bound=summarize_bound(read(bound_transport['baseline_report']),bound_transport,baseline,benchmark)
manifest=read('cases/manifest.json')
history=list(csv.DictReader((ROOT/'results/history.csv').open(encoding='utf8',newline='')))
source=(ROOT/best['file']).read_bytes()
digest=hashlib.sha256(source).hexdigest()
assert source==(ROOT/'solvers/current.py').read_bytes()
assert digest==best['solver_sha256']
assert len(source)<=100000
assert len(benchmark['results'])==320 and benchmark['invalid']==0
assert readiness['passed']and stress['passed']and periodic['valid']and reproduction['passed']
for evidence in (benchmark,readiness,stress,periodic,reproduction):
    assert evidence['solver_sha256']==digest
    assert evidence['max_runtime_sec']<=5
assert hashlib.sha256((ROOT/'cases/manifest.json').read_bytes()).hexdigest()==baseline['manifest_sha256']==benchmark['manifest_sha256']
for meta in manifest['cases']:
    assert hashlib.sha256((ROOT/meta['path']).read_bytes()).hexdigest()==meta['sha256']
for row in history:
    assert hashlib.sha256((ROOT/row['file']).read_bytes()).hexdigest()==row['solver_sha256']
assert all(int(b['total_score'])>int(a['total_score'])for a,b in zip(history,history[1:]))
old={r['id']:r for r in baseline['results']}
delta=[r['score']-old[r['id']]['score']for r in benchmark['results']]
total=benchmark['total_score'];start=baseline['total_score'];target=start+7000000
assert bound['headroom']>0
required_headroom_percent=100*(target-start)/bound['headroom']
worst=max(x['max_runtime_sec']for x in (benchmark,readiness,stress,periodic,reproduction))
summary=dict(baseline_score=start,target_score=target,total_score=total,gain=total-start,
             shortfall=max(0,target-total),target_achieved=total>=target,
             wins=sum(d>0 for d in delta),ties=sum(d==0 for d in delta),losses=sum(d<0 for d in delta),
             selected_file=best['file'],source_bytes=len(source),solver_sha256=digest,
             worst_verified_runtime_sec=worst,immutable_checkpoints_verified=len(history),
             frozen_inputs_verified=320,upper_score=bound['upper_score'],
             bound_report=bound_path,baseline_headroom=bound['headroom'],
             selected_headroom=bound['selected_headroom'],
             baseline_proven_optimal=bound['baseline_proven_optimal'],
             selected_proven_optimal=bound['selected_proven_optimal'],
             required_headroom_percent=required_headroom_percent)
(ROOT/'results/seven_final_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf8')
complementary_status = (
    'A complementary forward constructor was tested separately. It rewards keeping remaining mismatches adjacent, runs before refinement on a disjoint input domain, and skips the later plain beam. **It is not included in selected checkpoint 054.**'
    if int(best['id']) == 54 else
    'The selected solver also uses a forward constructor that rewards keeping remaining mismatches adjacent. It runs before refinement on a disjoint input domain and skips the later plain beam. The final benchmark includes any regressions caused by this replacement.'
)
runtime_status=''
if best.get('kind')=='verified_runtime_variant' and int(best['id'])==55:
    strict=read('results/checkpoints/best_055_254652429.benchmark.json')
    strict_rows={row['id']:row for row in strict['results']}
    assert len(strict_rows)==320
    assert all(row['score']==strict_rows[row['id']]['score'] and
               row['output_sha256']==strict_rows[row['id']]['output_sha256']
               for row in benchmark['results'])
    probe=read('results/seven_construct_fast_boundary_probe.json')
    assert probe['all_outputs_identical']
    helper={kind:[row['runtime_sec'] for row in probe['helper'] if row['variant']==kind]
            for kind in ('parent','bytearray')}
    assert all(row['exact_operations'] for row in probe['helper'])
    helper_mean={kind:sum(times)/len(times) for kind,times in helper.items()}
    helper_reduction=100*(1-helper_mean['bytearray']/helper_mean['parent'])
    runtime_status=(f"The selected runtime variant preserves all 320 scores and stdout hashes from immutable checkpoint 055. "
                    f"Its private cluster states use bytearrays and update only the score planes consumed by the beam. "
                    f"Recorded paired helper timings show a {helper_reduction:.1f}% reduction in mean cluster-search runtime. "
                    f"The full stable run measured {benchmark['runtime_sec']:.3f} seconds versus {strict['runtime_sec']:.3f} seconds "
                    f"for checkpoint 055, with a selected stable maximum of {benchmark['max_runtime_sec']:.3f} seconds. "
                    f"Expanded validation for the selected bytes is reported below. "
                    f"A further stamp-plane cache did not materially improve whole-program runtime and was rejected; "
                    f"see [the cache measurements](seven_construct_cache.md).")
lines=[
'# Seven-million-point campaign result', '',
f"Selected submission: [`{Path(best['file']).name}`](../{best['file']}).",
'',
f"The requested gain of 7,000,000 points was {'achieved' if total>=target else 'not achieved'}. The verified gain is **{total-start:,}**, reaching **{total:,}** on the unchanged 320-case benchmark. Remaining shortfall: **{max(0,target-total):,}**.",
'',
'| Measurement | Stable score |','|---|---:|',
f"| Initial greedy checkpoint 000 | {int(history[0]['total_score']):,} |",
f'| Campaign starting solver, runtime 053 | {start:,} |',
f'| Requested threshold | {target:,} |',
f'| Selected checkpoint {best["id"]:03d} | {total:,} |','',
f"Compared with the campaign start, {summary['wins']} cases improved, {summary['ties']} tied, and {summary['losses']} regressed. These are local results from 320 cases. The unseen official 40-case score has not been measured.",
'',
'## New immutable checkpoints','',
'| ID | Score | Change from preceding best | File |','|---|---:|---:|---|',
]
for i,row in enumerate(history):
    if int(row['id'])>=54:
        lines.append(f"| {row['id']} | {int(row['total_score']):,} | +{int(row['total_score'])-int(history[i-1]['total_score']):,} | [{Path(row['file']).name}](../{row['file']}) |")
lines += ['',f"All {len(history)} checkpoints are preserved, and their hashes were checked. See [history.csv](../results/history.csv) for the complete score progression and the [previous report](million_report.md) for checkpoints 000–053.",'',
'## Search results','',
'The selected solver searches backward from the target while leaving the final stamp unconstrained, then reverses the operation sequence. For targets with few distinct patches, this replaces an early constructor and feeds its result into existing refinement. Exact bit-parallel gains, static pickup masks, and bytearray state copies keep the search cost manageable.',
'',
complementary_status,
'',
runtime_status,
'',
'On the 100-case development suite, distant-pair repair gained 2,222 points, Gibbs coordinate annealing gained 13,822, and coarse-color continuation gained 7,778. Their gains did not justify the added runtime; Gibbs added up to 2.315 seconds. Disjoint-patch assignment produced no development wins.',
'',
'A later experiment alternated global assignments across two shifted patch tilings. Allowing independently chosen rotations for each transfer improved its raw constructions, but neither variant beat checkpoint 055 on any of the 13 eligible development cases. The free-rotation variant took up to 1.617 seconds and passed 40 additional canonical checks. It was rejected; see [layered-assignment research](seven_sequence_layered.md).',
'',
'Strict and neutral long-window reconstruction replaced windows of 12, 24, or 32 operations using beam width 24 and three or six rounds. On 36 eligible development cases it produced no new search gain over the best-known paths and checkpoint 055. An apparent 13,471-point improvement only recovered regressions relative to older checkpoint 053 paths.',
'',
'Cached stable diagnostics found gains of 106,577 for mixed forward/backward construction, 336,679 for a wider standalone backward beam, and 321,463 for a clustered beam. These diagnostic gains overlap and cannot be added together. The mixed constructor was rejected for excessive integration cost.',
'',
'Details: [campaign log](seven_campaign.md), [constructor research](seven_construct.md), [sequence research](seven_sequence.md), [backward review](seven_fastback_review.md), [integration review](seven_combined_review.md).',
'',
'## Validation','',
'The benchmark remains frozen at seed 20260925: 20 smoke cases, 100 development cases, and 320 stable cases across eight families. All 320 input hashes were rechecked. Evaluation uses the canonical simulator, strict output validator, exact integer scorer, reproducible generator, benchmark runner, and immutable checkpoints.',
'',
'| Check on selected bytes | Result | Maximum seconds |','|---|---|---:|',
f"| Stable benchmark | 320/320 valid | {benchmark['max_runtime_sec']:.3f} |",
f"| Random/boundary readiness | {readiness['cases_passed']}/{readiness['cases_total']} plus repeat | {readiness['max_runtime_sec']:.3f} |",
f"| Maximum-size holdouts | {stress['cases_passed']}/{stress['cases_total']} valid | {stress['max_runtime_sec']:.3f} |",
f"| Added periodic holdouts | {periodic['cases_passed']}/{periodic['cases_total']} valid | {periodic['max_runtime_sec']:.3f} |",
f"| Changed-output reproduction | {reproduction['cases']} exact scores and output hashes | {reproduction['max_runtime_sec']:.3f} |",
'',
f"The stable run took {benchmark['runtime_sec']:.3f} seconds in total, averaging {benchmark['avg_runtime_sec']:.3f} seconds per case. The worst verified runtime was {worst:.3f} seconds against the 5-second limit. This leaves limited margin on this machine; hidden inputs or different hardware may take longer.",
'',
f"The selected file is {len(source):,} bytes, reads stdin, and emits only the required operations. It uses no local files or third-party dependencies. Its standard-library LZMA wrapper decodes exactly to the inspected readable Python source. `solvers/current.py` is an identical copy. SHA256: `{digest}`.",
'',
'## Limit of the result','',
f"Color conservation, exact short-prefix searches, whole-board rotation orbits, independently checked integer coverage certificates, and a stamp-transport bound that accounts for repeated grid contacts give a stable-score upper bound of **{bound['upper_score']:,}**. This allowed at most **{bound['headroom']:,}** additional points at the campaign start; {bound['baseline_proven_optimal']} baseline cases were already provably optimal. A 7-million-point gain required about {required_headroom_percent:.2f}% of that remaining room. The selected solver meets these ceilings on {bound['selected_proven_optimal']} cases, leaving at most **{bound['selected_headroom']:,}** further points. This upper bound does not establish whether the requested threshold is attainable. The evaluated methods {'reached' if total>=target else 'did not reach'} it.",
'',
'Proofs and per-case evidence: [bound audit](seven_bound.md), [latest transport bound JSON](../results/seven_bound_transport.json), and its [full 320-case parent bound JSON](../results/seven_bound_joint.json).','',
]
(ROOT/'notes/seven_report.md').write_text('\n'.join(lines),encoding='utf8')
print(json.dumps(summary,indent=2))
