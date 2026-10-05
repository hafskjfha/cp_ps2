# Seven-million-point campaign

Request: improve the current frozen320 score by at least 7,000,000.
Starting solver: `submissions/runtime_053_254103898.py`, score254103898.
Target:261103898. Keep all320 input hashes, five-second runtime, standard-library
Python and100000-byte source/output limits. Existing evaluation infrastructure
and checkpoints are reused. The user authorizes autonomous measured experiments.
No new dedicated test programs are required; canonical simulator checks run
inline or in diagnostic evaluation drivers.

Independent work: forward construction with spatial objective potentials;
global/distant sequence optimization; rigorous theoretical score ceilings;
backward and mixed forward/backward construction.

Root hypothesis: construct from the final target with an unconstrained stamp.
Represent unconstrained labels by6, which matches no physical color. Swapping
target labels backwards preserves the exact number of final grid matches.
The same bit-parallel RefineState scorer supports every backwards move. A beam
keeps multiple full label states, and reversing its path yields legal output.
Mixed construction can swap either the actual initial colors or the final
labels, returning forward_path+reverse(backward_path).

Canonical verification:11227 candidate gain/clone checks on100 random
configurations,2000 reverse-path canonical simulations passed.
Development probes (candidate floor against current053; diagnostic only):

| Probe | Retained gain | Added total seconds | Maximum seconds |
|---|---:|---:|---:|
| Backward width12,future3 |96255|13.094|1.119|
| Backward width48,future3 |170867|40.763|4.278|
| Mixed width24,future3 |153511|40.500|4.033|

These are unqualified candidate gains, not submission claims. The larger probes
cannot simply be appended to the parent within5s. Explore early integration,
cheaper state updates and stronger candidate refinement before qualification.
`results/seven_parent_cache.json` is a progressively written canonically checked
cache; it is not runtime qualification evidence. Every row must reproduce the
existing immutable benchmark score.

FastBack replaces generic dynamic goal columns by static original-stamp pickup masks. Current bytearray version independently verified with601488 gain entries,720 canonical transitions and30 complete deterministic constructions. Stable cached width48 gains336679, total62.389s,maximum2.451s added. Clustered-error forward beam gains321463 independently; these gains are not additive and neither is a complete qualified solver.

Reverse integration replaces early retained construction for low-complexity target patches (at most4C distinct unrotated patches), N>=10,K>=12,initial matches below88%inventory bound. Existing downstream refinement is reused. Smoke20:+104953,all valid,max4.629s. Full development100:+229486,10wins1loss,all valid,max4.596s,total148.052s. One loss is case027−3827; the integrated solver retains no universal per-case old-score guarantee. Packed source27492bytes is a lossless standard-library LZMA wrapper; decoded readable source152485bytes is saved. Static review validates exact decoding and preserved original code. Fullstable qualification follows.

Reverse integration fullstable320:254492748, gain388850,22wins294ties4losses,all valid,max4.655s,total461.480s. Fourlosses027−3827,189−5917,246−6173,313−5102. All14frozenperiodicruntimeholdouts passed,max4.231s. Random/readiness and original36maximum-size checks pending. This does not meet requested261103898.

Saved immutable054:submissions/best_054_254492748.py. Readiness38passed,maximum-size36passed,periodic14passed,all26changedscore outputs reproducedexactly. Supplemental qualification evidencecopiedunderresults/checkpoints/best_054_254492748.*. solvers/current.py nowequals054.

Complementary combined candidate:reverse gate unchanged; on other N>16,D3,K>10 instances, add residual-error-cluster beam before existing downstream refinements and omit the later plain longbeam. Actual combinedsmoke18275957, gain22578 over054smoke,20valid,max4.722s. Source28702bytes; packedliteraldecodedsource passedstaticreview. Stressgatebeforefullsuitepending.

Combined fullstable320:254652429, +159681 over054 and +548531 overcampaignstart053. Against053:41wins273ties6losses; against054:19wins299ties2losses. All320 valid,max4.685s,total456.433s. Full devsubset81293813 exactly reproduces independent-domain prediction. Maximum-size36passedmax4.831s. Finalreadiness,periodicandchanged-outputrepeatpending. Requested7milliongain stillunmet,shortfall6451469.

Checkpoint 055 qualification completed: 38 readiness cases, 36 maximum-size
cases, 14 periodic cases, and all 47 changed-score output reproductions passed.
The immutable submission is `submissions/best_055_254652429.py`; its largest
observed qualification time was 4.901 seconds. Its score improvement is measured
on the unchanged stable suite, and the requested gain remains unmet.

A subsequent performance hypothesis removes unused per-region counts and stamp
masks from the private cluster beam states, copies bytearrays, and preserves all
consumed score planes. Independent canonical and clone-isolation review passed.
All 320 standalone outputs of `solvers/experiments/seven_fast_runtime.py` are
byte-identical to checkpoint 055. Stable total time fell from 456.433 to 445.680
seconds; the slowest single observation was 4.964 seconds. This is an equal-score
runtime experiment, not another strict score checkpoint. Expanded checks remain
required before selecting it.

Two further scoring hypotheses are being measured: long sequence windows rebuilt
against exact suffix wishes, and alternating global assignments across shifted
disjoint-patch layers. They must beat the current measured score within the same
runtime limit before any promotion. Relaxed score headroom is not a prediction
that either method can recover it.

Both additional scoring directions were rejected after measurement. Strict and
neutral long-window reconstruction found no new gain on 36 eligible development
cases beyond the existing cached paths and checkpoint 055. The apparent 13,471
points from taking the best cached seeds only recovers prior regressions; it is
not a search improvement. Two-layer patch assignment, including independent
transfer rotations, produced no wins on its 13 eligible development cases.
Canonical differential checks passed for both directions. Their diagnostic
times are not standalone contest qualification evidence.

Final selection: `submissions/runtime_055_254652429.py`, 29,022 bytes, with exactly
the same 320 scores and output hashes as score checkpoint 055. Readiness 38,
maximum-size 36, periodic 14, and all 47 changed-score output reproductions passed.
The largest observation across all qualification runs was 4.964 seconds. This
runtime variant is logged separately from strict score history. All 56 strict
checkpoint hashes and all 320 frozen input hashes were verified after selection;
`solvers/current.py` is byte-identical to the selected submission.

Final score: 254,652,429, a gain of 548,531 over the campaign start. The requested
7,000,000 gain was not achieved; the shortfall is 6,451,469. New transport bounds
tighten the relaxed aggregate ceiling to 262,303,537, which still does not prove
the requested target impossible. The complete report is `notes/seven_report.md`.
