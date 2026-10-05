# Frozen benchmark ceiling audit

This is a diagnostic mathematical ceiling, not a measured solver improvement.
The baseline is `submissions/runtime_053_254103898.py`, measured at **254,103,898**
on the unchanged 320-case manifest. The requested increase is 7,000,000, giving a
target of **261,103,898**.

The final certified upper bound is **262,366,265**, leaving at most
**8,262,367** additional points. **178 of 320 cases are already provably optimal**
under at least one bound below. The requested gain would consume at least
**84.72%** of this relaxed headroom. These bounds do not prove the requested
increase impossible, and they do not show that the ceiling is attainable.

## Artifacts and reproduction

Run these commands in order from the repository root:

```text
python tools/seven_bound_audit.py
python tools/seven_bound_coverage.py
python tools/seven_bound_shallow.py
```

The final per-case bounds, group summaries, weighted-coverage certificates, and
shallow-search statistics are in `results/seven_bound_final.json`. The initial
and intermediate reports are `results/seven_bound_audit.json` and
`results/seven_bound_coverage.json`.

The scripts read the canonical simulator, the frozen inputs, and the recorded
baseline benchmark. They change only their diagnostic JSON files. The audit
checks input hashes, manifest hash, solver hash, and recorded score consistency.
Its bit-sliced exact two-move oracle was differentially checked against **39,360
canonical two-move sequences across 18 fixed-seed random instances**, with both
stamp sizes and N from 3 through 6. No new dedicated unit-test files were added.

The final stages took about 11 seconds total on this run. Reported bound quality
does not depend on solver runtime or on time limits.

## Proofs

Let B=N², q=D², I be the initial number of matches, and W be the set of initially
wrong grid positions.

1. **Color inventory.** Every operation is a permutation of the B+q colors in
   grid plus stamp. For color c, at most min(count(A+S,c), count(T,c)) target cells
   can match. Sum that quantity over colors to bound the final match count.

2. **Touched cells.** Only touched cells can change. Each operation touches q
   positions, so final matches are at most min(B, I+Kq).

3. **Unweighted patch coverage.** Count initially wrong cells in every legal
   placement, ignoring rotation. Any sequence visits at most K distinct
   placements. The number of initially wrong cells in their union is no larger
   than the sum of the K largest such patch counts. Hence final matches are at
   most I plus that sum, capped at B. Overlap is double-counted only in the
   direction that weakens the ceiling.

4. **Exact-prefix bound.** If E_h is the maximum match count after at most h
   operations, then any sequence of at most K>=h operations ends with at most
   E_h+(K-h)q matches: each remaining operation can add at most q. The audit
   exhaustively computes E_1, computes E_2 when it can tighten the bound, and
   computes selected E_3/E_4 when the exhaustive state count is modest.
   Sequences ending before h are also bounded because E_h includes them.

5. **Whole-board rotation orbit.** When N=D, a move exchanges the entire board
   and stamp, with inverse rotations. After an even number of moves the grid
   is a rotation of the original A; after an odd number it is a rotation of
   the original S. Every rotation of S is reachable in one move; every rotation
   of A is reachable in two. Thus K=1 is exact by one-step enumeration, and
   K>=2 is exact by checking these eight possible grid orientations. A mere
   inventory ceiling would be much looser on these cases.

6. **Weighted coverage certificate.** Give each initially wrong cell i an
   integer weight w_i in [0,Q], with Q=8. Let H be the maximum sum of weights in
   any legal patch. If a final newly corrected subset F lies in the union of
   at most K visited patches, then

   ```text
   Q |F| = sum_F w_i + sum_F (Q-w_i)
         <= K H + sum_W (Q-w_i).
   ```

   Therefore final matches are at most
   `I + floor((K*H + sum_W(Q-w_i))/Q)`.
   A deterministic greedy procedure proposes weights. Their validity does not
   rely on the procedure being optimal: the stored integer weights, the maximum
   over every patch, and the final numerator are recomputed exactly. Every
   accepted certificate is saved in the report. There are no floating-point
   feasibility assumptions.

Taking the minimum of independently valid match ceilings remains a valid
ceiling. Each match ceiling is converted using the official per-case integer
floor; those per-case score ceilings are then summed.

## Remaining ceiling by case family

| Family | Remaining score ceiling |
| --- | ---: |
| Stripes | 2,610,413 |
| Repeated stamp | 1,752,071 |
| Random | 1,276,865 |
| Checkerboard | 1,152,052 |
| Reachable | 824,350 |
| Near target | 350,255 |
| Local adversarial | 217,644 |
| Nearly uniform | 78,717 |

Other useful partitions:

| Partition | Remaining score ceiling |
| --- | ---: |
| D=2 | 2,203,561 |
| D=3 | 6,058,806 |
| N=3..9 | 699,526 |
| N=10..19 | 3,005,050 |
| N=20..30 | 4,557,791 |
| K=1..3 | 49,988 |
| K=4..10 | 1,042,144 |
| K=11..60 | 2,825,245 |
| K=61..180 | 4,344,990 |
| Baseline already uses K operations | 7,242,584 |
| Baseline has spare operations | 1,019,783 |

The spare-operation split concerns whole-instance headroom on those baseline
cases. It establishes that a method which only changes cases with spare budget
cannot add more than 1,019,783 points. It does not bound sequence replacement on
cases that originally used all K operations.

## Practical search implications

The largest remaining individual ceilings include:

| Case | N/D/C/K | Current matches | Certified match ceiling | Score headroom |
| --- | --- | ---: | ---: | ---: |
| 154 | 21/3/5/45 | 249 | 402 | 346,939 |
| 007 | 30/3/6/180 | 598 | 879 | 312,222 |
| 058 | 18/2/6/73 | 225 | 312 | 268,518 |
| 283 | 27/3/3/93 | 549 | 727 | 244,170 |
| 063 | 27/2/5/145 | 528 | 687 | 218,107 |
| 142 | 21/3/6/112 | 321 | 417 | 217,687 |
| 001 | 30/3/6/180 | 687 | 880 | 214,444 |
| 117 | 13/3/5/30 | 121 | 157 | 213,018 |

These are opportunities under a relaxation, not promises of achievable gain.
The large-D, many-color stripe/repeated-stamp cases justify testing stronger
sequence construction and replacement, because they dominate remaining
headroom and generally have exhausted the move budget. Local suffix repairs
alone cannot meet the requested increase. Perfecting all N<=9 cases would add
at most 699,526 points, and perfecting all K<=3 cases at most 49,988.

The top 20 remaining cases account for at most 4,087,444 points. Therefore even
an ideal solution on those cases alone cannot produce a 7,000,000 increase;
improvements must be broad. Case IDs above are diagnostic references only and
must not be used for solver-specific branches or benchmark hardcoding.

Further useful bound work would require a substantially tighter relaxation of
operation sequencing and stamp transport. The present bounds intentionally
ignore many of those restrictions, so the true remaining attainable gain may
be appreciably smaller.

## Follow-up: joint inventory and coverage relaxation

A bounded second audit tried an additional necessary condition. Let U be the
union of visited patches. All colors outside U stay unchanged, and the colors
inside U plus the stamp are conserved. For any color potentials lambda_c in
[0,1], the net increase in matches is therefore at most

```text
sum_c lambda_c count(S,c)
  + sum_(i in U intersect W) (1-lambda_target(i)+lambda_initial(i)).
```

Proof: the inventory bound restricted to U is
`I + |U intersect W| - sum_c max(count(T_U,c)-count(A_U,c)-count(S,c),0)`.
Replace each maximum by its lower bound lambda_c times its argument. Initially
correct cells contribute zero to each color-count difference. The resulting
cell weights lie in [0,2] and can be bounded using the same weighted coverage
certificate as before. This couples color inventory and patch coverage instead
of taking only their independent minimum.

`tools/seven_bound_joint.py` tested every nontrivial binary color-potential
assignment, at most 62 per case, on 85 potentially useful cases. When
`K >= ceil(N/D)^2`, the coverage relaxation can visit the whole board, so this
joint relaxation cannot beat the existing global inventory bound and is skipped.
Greedy integer certificates were proposed for all thresholds, with denominator-8
refinement for an improving potential. The run took about 11 seconds.

The only extra tightening was case_038, from 469 to 468 matching cells,
reducing the score ceiling by **2,066**. Its stored integer certificate was
independently recomputed and verified. The newest result is therefore
**262,364,199**, with **8,260,301** remaining headroom, in
`results/seven_bound_joint.json`. The preceding final report is retained intact.

This follow-up does **not** establish that a 7,000,000 increase is impossible.
The remaining margin above that target is 1,260,301. All K=4..10 cases together
have only 1,042,144 relaxed headroom, so even eliminating their entire remaining
ceiling by exhaustive search could not close that margin by itself. A useful
new proof would have to constrain longer operation sequences and coupled stamp
transport. The simple color-potential approach above did not supply such a
constraint; no additional claim of impossibility is supported.

## Follow-up: stamp transport, repeated contacts, and adjacency

A further lightweight static audit found a **60,662** reduction, leaving an
upper score of **262,303,537**. This is still **1,199,639** above the requested
target score of 261,103,898. The computation took about 0.73 seconds and is
recorded in `results/seven_bound_transport.json`; the reproducible tool is
`tools/seven_bound_transport.py`. It leaves prior reports intact.

The useful new bound explicitly prices the repeated contacts needed to change
the stamp beyond the initial grid's patch patterns. Let q=D². Let e be the
maximum overlap between the initial stamp and any rotated target patch. Let m
be the maximum overlap between any initial A patch and any rotated target
patch. Both statistics are computed exactly. Target patterns include all four
rotations, so an additional rotation of the source patch does not change m.

For a sequence of L moves, let R count grid contacts after a cell's first
contact. There are qL-R distinct touched cells, hence its net match increase G
is at most qL-R. Also let B count correct deposits, including deposits later
overwritten. G<=B. The first stamp makes at most e correct deposits. Every
later stamp is the preceding operation's picked-up grid patch. Compared with
that patch's original A colors, only cells previously contacted can differ;
each such cell can raise its overlap with the destination target by at most
one. Thus

```text
G <= qL-R,
G <= B <= e+(L-1)m+R.
2G <= qL+e+(L-1)m.
```

The final expression increases with L, so for L<=K the certified ceiling is
`I + floor((qK+e+(K-1)m)/2)`. This improves case_023 from 402 to 393 matches
(13,314 points), case_247 from 425 to 402 (27,348 points), and case_294 from
197 to 189 (20,000 points).

Two additional valid bounds were measured but did not tighten the aggregate:

- **Target-pattern transport.** Write P_t for the reference-oriented target
  colors under operation t, and c_t for the colors it picks up. Exact score
  telescoping gives
  `G = matches(S,P_1) + sum_{t<L}(matches(c_t,P_(t+1))-matches(c_t,P_t))
  - matches(c_L,P_L)`.
  If H is the maximum Hamming distance between two rotated target patches,
  then G<=e+(K-1)H. Most useful cases have H=q, making this too weak.
- **Unordered neighboring-color histograms.** Count each unordered color pair
  on grid and stamp adjacency edges. A swap preserves all internal patch/stamp
  edges up to rotation; only at most `2D*min(2,N-D)` exterior edges change.
  Let F be the sum of positive target-grid histogram deficits against the
  initial grid-plus-stamp histogram. K moves change at most bK edges. E wrong
  final cells change at most 4E target-grid edges, so `F<=bK+4E` and
  `E>=max(0,ceil((F-bK)/4))`. This incorporates all color-pair categories rather
  than only a monochromatic edge total, but still gives no extra reduction.

Independent checks compared the patch-overlap and Hamming statistics with
scalar enumeration of every patch pair on 20 small instances. All three bounds
also held on 480 canonically simulated fixed-seed random sequences.

These results remain insufficient to prove the requested gain impossible.
The transport relaxation is weak whenever an initial patch can perfectly match
some target patch, and the adjacency relaxation permits much more structural
change than the relevant operation budgets require. No stronger inexpensive
certificate has been established in this audit.
