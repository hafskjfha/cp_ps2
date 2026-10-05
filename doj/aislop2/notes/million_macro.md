# Early macro construction investigation

Parent checkpoint052 stable score252937025. Hypothesis: replacing weak suffixes of the incumbent with substantial-budget sparse permutation routing can improve exact final matches. Probe four prefix cut points and an independent initial-state macro constructor, retain the parent whenever the candidate does not win. Existing simulator remains canonical. All initial timings under concurrent research load are diagnostic.

## Results (diagnostic only)

- Prefix routing, five fractions `(0,.25,.5,.75,.9)` with three-power routing for30 rounds followed by `(6,9,5,12,3,6,9)` powers: cached parent050 development +53995, max0.362s.
- Distant conjugate macros `C(AB)^3C` compile sparse local/stamp permutations, substitute remote patch values and score every remote action through bit masks. Seven development wins, +57111 vs050, total34.667s/max4.119s incremental; rejected for runtime and limited gain. Accepted macros have an exact delta assertion and every returned development output passed canonical simulation.
- Refining two candidate prefix/macro trajectories: development +44094 vs050; no merit over the cheaper standalone prefix stage.
- Exact score-neutral operation deletion followed by routing: stable320 cached052 +0. Rejected; it removed some operations but did not make another profitable routing edit possible.
- Five-fraction prefix routing: stable320 cached052 +96212,12wins; incremental total12.868s,max0.529s.
- Same prefix stage applied after root longbeam24: +104785 additional,14wins; combined parent052 gain998813 before other agents' complementary edits. Incremental total12.903s,max0.545s. `results/million_macro_after_longbeam.json` contains exact outputs.

## Frozen integration fragment

`solvers/experiments/million_macro_prefix.py` provides `macro_prefix`, intended to integrate with existing parent globals. Call with `cuts=(0,.25,.5,.75,.9), mixed=True`. This is a fragment, not a standalone submission and not a promoted checkpoint. Parent retains the score whenever no candidate wins.

A safe gain upper bound now skips an uncompetitive prefix: initial prefix matches plus remaining operation budget times2 for D3 or1 for D2. Across all supported powers3,5,6,9,12, the number of affected grid cells per complete macro divided by operation cost is at most those bounds. No sequence of these macros can exceed that bound. Every one of320 cached longbeam-parent operation sequences remained byte-for-byte equivalent as operation tuples. Incremental total9.416s,max0.480s in this measurement; shared machine timings are provisional. `results/million_macro_fast_equivalence.json` records parity.

Verification:60 random configurations covering N3..30,D2/D3,C2..6,K1..180 passed canonical simulator, strict output validator and retained-score floor;15 deterministic repeats passed. Evidence `results/million_macro_prefix_verification.json`.

## Independent longbeam review

Reviewed root `million_longbeam.py` and parent State/clone logic.100 randomized configurations,1200 dynamic states,6075 returned choices passed exact canonical gain and transition checks. Tested shuffled action orders, first-choice global maximum, clone isolation, board/stamp/match count, per-patch counts and child best-action gain against exhaustive scalar enumeration. No correctness issue found. Choice tier cutoff is tested after sampling the current tier, so it can include actions more than one below the best gain; this is heuristic behavior, not invalidity. Evidence `results/million_macro_longbeam_review.json`.
