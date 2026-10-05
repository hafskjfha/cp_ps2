# Global sequence and objective perturbation research

Parent: immutable `submissions/best_052_252937025.py`. All probes below use the
canonical simulator and output validator, deterministic seeds, and retained
parent score floors. Cached-output experiments are diagnostic; no checkpoint
or submission claim is made here.

## Global sequence mutation (rejected)

Implemented sparse accepted-update propagation for exact forward color states
and backward target wishes. Mutations include single operations, distant swaps,
relocation, reversal, and segment rotation. Inline differential check covered
1,500 accepted random changes, including worse-score mutations; every prefix,
suffix, and score matched independent full reconstruction.

On provisional parent050 dev100, 5,000 proposals at initial temperature0.45
yielded +1,480 points, max incremental0.178s, total3.904s. Increasing to50,000
proposals/temperature0.9 still yielded just+1,480, max1.835s,total42.665s.
This direction was rejected for poor score/runtime return.

## Destruction/reconstruction (rejected)

Remove or randomize2/4/8/16 operations, reconstruct with three exact backward
refinement passes, and walk between basins with temperature0.5. Sixteen trials
on provisional parent050 dev100 yielded+1,372, max0.816s,total12.050s. Root
independently found no gain from its related24-trial/two-pass variant. Rejected.

## Objective perturbation

Instead of changing operation variables directly, change target-cell objective
weights, perform one weighted coordinate sweep, then restore true objective and
perform three unweighted sweeps. Move to repaired basins within one match of
the best, reset every four trials, and retain the highest canonical score.
Existing parent only tries two specific weight configurations once; this probe
explores randomized and spatial configurations repeatedly at the final solution.

Twelve-trial results on provisional050 dev100:

- Random1/2 weights: +30,989,7wins,max0.952s,total14.167s.
- Random0/1 relaxation: +9,180,4wins,max0.981s,total13.632s.

On canonical052 dev100:

- Spatial1/2 weights: +23,687,7wins,max0.805s,total12.119s.
- Random subset of unresolved cells doubled: +18,653,5wins,max0.873s,total11.959s.

After root's beam24 dev100:

- Eight random1/2 trials,three true sweeps: +26,204,7wins,max0.559s,total7.890s.
- Four trials,three true sweeps: +9,563,3wins,max0.290s,total4.226s.
- Eight trials,one true sweep: +5,157,3wins,max0.332s,total4.703s.
- Eight trials,two true sweeps: +6,230,2wins,max0.498s,total7.199s.

The three-sweep variant is clearly stronger in these diagnostics. Full frozen320
diagnostic after canonical beam24 outputs is in progress. Runtime figures are
incremental helper time under shared machine load, not full CLI qualification.

Implementation: `solvers/experiments/million_anneal_fragment.py`, function
`objective_walk`. Diagnostic drivers are `million_anneal_*_probe.py`; they read
cached outputs and are not submission files.

## Frozen result and integration

Full320 after canonical beam24: eight trials, mode0, three true sweeps yields
**+52,045**,12wins/no losses, incremental helper total21.861s,max0.6173s.
Evidence: `results/million_anneal_stable_objective_8_0_320_p3.json` contains
canonical scores and every proposed output. Winning IDs:006,007,018,027,042,
063,070,202,247,266,270,283. Omitting largest-D3 cases (N>=24,K>=120) loses
only case007's+3,333 in this diagnostic. Root owns any actual gating and full
submission runtime qualification.

Additional spatial mode2 experiment: +42,000,13wins,total23.074s,max0.6112s.
Its union with mode0 is+71,666 but the extra runtime is not justified here.
Color-focused mode4 on dev adds17,228; this was not promoted to full320.
Lower-pass ablations were weaker. No further expansion is requested.

Frozen implementation: `million_anneal_objective_frozen.py` keeps only the
selected mode0 behavior with the original public function signature. It is a
helper fragment, not a standalone submission. Integrate it after retained
candidate selection, passing the existing `refine`, `weighted_refine`, and
action geometry. Use trials8/mode0/passes3. Random seed is derived solely from
input colors and K. The returned path is always <=K and no worse than its input.

Thirty fresh random instances passed exact frozen/full-helper operation parity
plus canonical validity and parent-score-floor checks. Applying root's gate
N>=24,D3,K>=120 retains+48,712 with max incremental0.3370s,total17.579s.
Review metadata: `results/million_anneal_review.json`.
