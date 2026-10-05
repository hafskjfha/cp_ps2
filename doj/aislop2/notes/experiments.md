# Experiment log

Benchmark seeds and case identities are frozen before solver development. Scores use the exact integer official formula. The full stable suite has 320 cases; smoke has 20 and development has 100. The user confirmed the official time limit is 5 seconds; benchmarks enforce it, and separate maximum-size checks measure runtime margin.

## Baseline hypothesis (pending infrastructure)

Positive immediate-gain greedy should outperform zero operations and the best single swap on aggregate. Compare all three on the same stable cases and save the strongest as the mandatory initial checkpoint before researching advanced heuristics.

Baseline measurements (stable 320; all valid): zero 174748782 (avg 546089.94), single 186065927 (581456.02), positive greedy 228305971 (713456.16). Greedy smoke 15327134. Greedy aggregate subprocess time 18.638s with 4 workers, max 0.328s; independent readiness max 0.393s. Saved submissions/best_000_initial.py. All 27 infrastructure/solver tests pass.

## Experiment 1: neutral plateaus and deterministic restarts

Hypothesis: strict positive greedy stops while useful zero-gain moves can load a stamp that enables later gains. Explore unused stamp states during score plateaus; keep the best prefix, so the search may use all K operations without reducing the returned score. Randomized ties and independent restarts can diversify trajectories. Use packed color comparisons to make multiple runs affordable. This is a new algorithm; test transition/payload packing independently before measuring. Parallel agents investigate 2-ply lookahead and sequence refinement in separate files.

Hypothesis 1b: increasing fixed restarts from 4 to 8 or 12 improves robustness while packed comparisons retain runtime margin. Measure smoke and standalone max-size timings before a larger stable comparison.

Measured plateau4 stable240756242 (+12450271 vs initial), smoke17178504, readiness max0.717s; saved best001. Exact two-ply escape stable240849239 won and saved best002 (see notes/lookahead.md). Twelve one-hot plateau restarts stable242249708 (+1400469 over best002), smoke17251027, readiness max0.806s; saved best003. Increasing 4->8->12 runs had diminishing smoke gains (17178504 ->17244337 ->17251027). One-hot masks halved smoke runtime vs 3-bit XOR at identical scores and random-test sequences.

## Experiment 2: complementary search portfolio

Hypothesis: neutral plateau walks and strictly profitable two-operation escapes solve different instances. Run both self-contained searches and return the sequence with the higher exact final match count. The expected runtime is their sum; measure maximum-size safety under5 seconds. Use twelve cheap plateau restarts and four lookahead restarts; retain exact initial states for independent trials.

Portfolio stable244316245 (+924249 over multi4), smoke17571738, all320 valid; readiness max1.335s, saved best005. Multi4 previously won243391996 and saved best004.

Hypothesis2b: 8-wide lookahead during productive moves, as well as at plateaus, takes complementary paths. Add a third stream to portfolio; predict no per-case score reduction from exact best selection. Verify the full solver runtime; reject if unsafe.

Portfolio3 measured stable245343012 (+1026767), smoke17598532, all320valid, standalone readiness max1.982s; saved best006. Exact backward coordinate descent with randomized neutral ties on the two-search portfolio measured245544191 (+201179), all320valid, readiness max2.309s; saved best007. Sequence experiments are detailed in notes/sequence.md. These are independent search paths, so the strongest unrefined constructor need not yield the strongest refined path.

Profile: tools/profile_solver.py on portfolio3 and N30,D3,C6,K180 found17.1million int.bit_count calls dominating candidate scanning (results/profile_portfolio3.txt). Profiling instrumentation increased runtime to10.692s; this is not the uninstrumented solver runtime (standalone readiness maximum1.982s). An independent experiment is testing transposed action bitsets to reduce Python-level candidate scans.

Best008: sequence_portfolio3_four.py stable246335486, all320valid; four-sweep refinement on three-way portfolio. Standalone36-case N30 K180 holdout PASS max3.819s p95 3.231s mean1.851s (results/stress_sequence_portfolio3_four.json). Saved best008 after readiness.

## Experiment3: bit-sliced all-action maximum

Hypothesis: transpose target matches into action bitsets, add match counts in binary planes, and find the highest gain with bit intersections. This reduces Python candidate scans and preserves exact tie order. First integrate exactly equivalent State into best008, verify byte-identical outputs, then spend speed savings on broader search/refinement under5 seconds. See notes/bitset.md for independent scalar parity tests.

Bitset equivalent integration smoke17738064, all20 output hashes identical to best008, max2.047s under concurrent jobs2. Hypothesis3b: eight lookahead restarts, width64 plateau escapes, and6refinement sweeps will spend saved runtime to improve score. Keep plateau12 and productive width8 unchanged for bounded scope.

Equivalent bitset full stable score246335486, all320 output hashes exactlymatchbest008. Runtime sum69.941s max1.836s withjobs2 (compared94.641s/max4.271s before; differing machine contention makes ratio approximate). Hypothesis3c: use the same transposed max-gain bitsets for neutral plateau runs too; preserve tie order and novel-stamp selection exactly, reduce runtime of strongersearch.

Stronger bitset search stable246786935 (+451449), all320 valid; readiness max2.513s, saved best009. Transposing plateau evaluation too preserves all100 random plateau operation sequences and all20 complete smoke outputs, reducing smoke max3.354->2.482s (contention differs). Hypothesis3d: use the remaining runtime saving for8refinement sweeps instead of6, which preserves or improves the same constructed solution after each exact backward sweep.

Final experiment: full bitset search plus8refinement sweeps stable246874186 (+87251 overbest009), smoke17764025, all320valid. Readiness38/38 passed max2.909s. Saved best010. All60unit/differential tests pass, frozen generator regenerated321files with0changes, all11checkpoint source hashes verified and scores strictly increase. Finalmaximum observed output1496bytes, operations<=180. Independent review found no blocking correctness issues. Exact checkpoint sequential reproduction and36maximum-size holdouts are the final runtime checks.

Final saved-file reproduction: all320cases and all output hashes match exactly, score246874186, sequential mean0.382s max2.711s. Final36case max-size holdout PASS max3.559s p952.864s mean1.655s against5s. Solver, readiness, stable reproduction, and stress source hashes all agree. Final best submissions/best_010_246874186.py; full report notes/final_report.md.

## Continuation round 1: stronger search under the same five-second limit

User requested ongoing optimization until explicitly stopped. Starting checkpoint best010 has stable246874186 and maximum holdout3.559s. Three independent experiments investigate sequence annealing/pair neighborhoods, deeper forward search, and refinement-aware candidate selection. Root hypothesis: exact backward coordinate refinement can be accelerated with dynamic transposed action masks for both prefix colors and suffix wishes. Maintain both sets of masks incrementally while undoing the original prefix and propagating selected suffix swaps. Bit-sliced addition then evaluates all placements together. First require exact scalar sequence parity before spending any runtime savings on more search.

Depth-three rescue agent measured247272076 (+397890), all320valid, readiness38passed max2.814s; savedbest011. Backwardbitset refiner microtiming onmaxcase001: old8sweeps1.937s vs0.277s, identicalsequence (approximately7x component speedup, undercurrentmachine load). Hypothesis:32 exactsweeps can use this saving while preserving or improving the sameconstructedsolution. Compare full fixedsuite even ifsmokegainissmall.

Bitsetrefiner fullstable parity confirmed: every320output hash matchesbest010 exactly.32sweeps onoldconstructors measured247262674 (+388488) butwas superseded bydepth3best011247272076 beforequalifyingpromotion. Bounded neutral/lossy pairedwalks measured248036769 (+764693 vsbest011), readiness38passed max2.539s, savedbest012. Hypothesis: samewalkconstructor with32fastrefinement sweeps improvesor preserves everycase; evaluate runtimebeforepromotion.

Adjacentpair repair measured248753972 (+717203 overbest012), all320valid, readiness20max3.443s; promotedbest013. Hypothesis: globalavailable-color upperbound safely terminates searches andrefinement once reached, savingwork on47stablecases saturated belowN��. Add exactmatchcountmaintenance toState.apply; verifyboundinvariance and unchangedperscore beforeincludinginnewscorecandidate.

Best014: incremental pair sweeps plus sampled exact pair completion measured249115734 (+361762), all320valid and readiness20passedmax3.042s; source checkpoint saved. Selected-walk32 measured248235862 and pool-walk16 measured248256087, both superseded by pair-based bests. Tiny-board exact BFS was considered but not implemented: all color-feasible N<=4,D2 cases with K>1 in the fixed suite are already perfect, so no measurable score opportunity was found there.

Next root hypothesis: explicit three-operation exchange of two disjoint rotated patches can load colors despite a very bad first stamp placement. Sequence P,Q,P swaps the two grid patches and restores the stamp. Evaluate exact gains for candidate P against all disjoint Q with dynamic bitsets. Add this as one inexpensive constructor and measure whether its paths improve the final refined/paired result.

Disjointmacro smoke17801617 tiesparentbest014 onall20scores; nofullstableyet. Strongerhypothesis: general P,Q,P conjugation allows overlappingpatches andchangedstamp. ApplyP tobothprefixcolors andsuffixwishes, choosegloballybestQ exactly viaRefineState, thenundoP inbothdomains. This permits intermediate losses without limitingthe firstgain andcomputes the exact finalmacro gain.


Best015: retained beam search for K3..12 and exact K<=2 scored249389357, +273623 overbest014; all320valid and readiness38passedmax3.371s. Best016: extending beam toK24 at reduced width scored249547073, +157716; everycase nondecreasing, all320valid, readiness38max3.433s.

General conjugate macro constructor tied parent014 smoke17801617, max4.425s under shared load. It has not earned a stable run. New root hypothesis: optimize two separated operations while leaving intervening operations fixed, propagating prefix colors or suffix wishes through that middle block. Exact exhaustive companion checks pass on70 random cases. Replace half of existing adjacent-pair proposals with gaps2..12, retaining the same number of scalar companion scans to control runtime.

Best016 exclusive36-case max-size holdout: PASS36/36, max3.697s,p953.220s,mean1.797s. Root spaced-pair replacement smoke17795573 (-6044), rejected as replacement. General P,Q,P append smoke17801617 tieshead016, all20valid; evaluating development because only37stablecases have bothspare budget>=3 androom belowcolorbound. New spaced_append adds min(900,max(60,100000/N^2)) separated-pair proposals after existingparent, preserving its score floor; smoke pending. Global bound port onto016 fullstable running to establish score parity before integration.

Color-bound early-stop port: stable249547073, all320 per-case scores identical tobest016,51output hashes changed. Runtime sum190.295s versusparent218.552s under differing sharedload; max3.393s. Readiness38/38passedmax3.508s. Speed-only variant retained asbound_hybrid.py, no new best-score checkpoint.
Macro append development79394951 ties every100parent score; no stable run warranted. Low-budget separated-pair append smoke17801617 tiesparent, max4.320s sharedload; parked.
New hypothesis: perturb2..7operations of the best sequence, run4 randomized backward coordinate sweeps, and keep only nondecreasing completed trials. Use2..8 trials bounded by N^2+6K; include the validated color-bound stops. Determinism, legality, and canonical scorefloor pass30random cases. iterated_hybrid.py smoke underway.

Best017 saved249880999 (+333926 over016), guidedtriple after retainedbeam construction; all320valid, readiness20max3.700s. Full unit/differential discovery96tests passed. Iterated hybrid on016 improves development136096 across8cases despite tiedsmoke; most gains onN<=16. iterated_guided_small restricts this work toN<=16 before the guidedtriple stage (whole-solver comparison required; downstream repair may interact). Its smoke17829153 ties017; stable/readiness underway. iterated_guided_post moves perturb/refine after the full017 pipeline, ensuring the final scorefloor; frozen but unmeasured.
Reordering exact operation blocks by shifts and endpoint swaps passes70canonical floor/multiset tests; reorder_guided smoke17829153 ties017, parked pending broader value.
New small-board hypothesis: existing finite beam can usewidth96 anddepth60 whenN<=6,K>24, where actioncounts are tiny and singlecell gains are valuable. Run independently frominitial, apply ordinary refinement, compare truefinalscore with017 and keepbetter. small_beam_guided smoke/development underway.

Best018 saved250064691 (+183692), all320valid, readiness38max3.672s. IL-before-triple interaction improves12cases andregresses2(N7,N13); allN>16scoresunchanged. retained_small_beam.py recomputesboth finaltriple paths fromsharedconstruction then keepsbest, restoringparentfloor; 8random+2regression canonical comparisons pass. It remains unbenchmarked.
Small-board finite beam development+194444 vs017 on2cases (one additionalmatch N6; six additionalmatches N6). Combinedwith018 as small_beam_iterated.py, smoke ties018 andfullstable/readinessongoing.
SA candidate fromgenerator stable250559222, all320valid butmax4.683s sharedload; readiness20max3.799s. Awaitingexclusive36max-size stress beforepromotion. Agentsholdheavyjobsoncecurrentrunsfinish.
Newpreparedsmall_beam_novel.py usesallactions whenN<=4 plusglobalexpanded-state dedup, width128 anddepth80; otherN<=6 uses96width8branches. Twenty-four random two-operation instances match exhaustiveoptimum. No benchmarkyet.

Best019 saved250384135 (+319444 over018), tiny-board widerbeam plus IL. Stable320valid max3.670s; readiness38max3.195s. Higher SAshortscore250559222 awaits isolated36-case stress. Allagentsholdnewheavyjobs for timingwindow.

SA-short isolated36max-size holdout PASS36/36, max4.526s,p954.133s,mean1.967s. All320stablevalid250559222 (+175087 over019), readiness20max3.799s; savedbest020 afterruntimegate. Margin is narrower; nextpriority exactState.apply delta accumulation (agentkernel1.7-2.5x) beforeaddingmorelargeNwork.

Best021 saved250867386 (+308164 over020), retained small-board paths then pair annealing. Stable320valid max4.800s sharedload; readiness20max3.874s. All147N>16outputhashes equal020, so the unchangedmaximum-size search inherits020's isolated36-case runtime evidence (max4.526s).
State.apply delta accumulation fullyverifiedsame320hashesvs020, readiness38max3.632. State constructor geometrycache additionally verifiedsame320hashes, readiness38max3.582. Timing remains sharedload.
Root RefineState cache hypothesis: geometry in natural action bits can be cached across passes; represent shuffled tie rank with binary masks, retainingexactlexicographic tie selection. Initialize value/wish masks fromcellmembershipinstead ofeachrotatedaction.1750mixedswaps/actions and45completerefines matchold exactly. N30eight-sweepmicro0.2732s->0.1665s, sameoperations. refine_cached smokeall20hashesmatch020. CombinedwithverifiedStategeometry/delta onto021 as cached_best021.py; smokeall20samehashes, fullstable/readinessrunning.
Novel smallbeam diagnostic over36cases N<=6,K>24 (NOTaqualifyingbenchmark) finds+62500 each oncases156,284vs019, allvalid,max3.925s. Developmentonly+20408 fromretainedparentrestoration; maymerge novelbeam afterfinalSAto preserveparentfloor.
Preparedreorder_cached.py: exactpositive blockshifts/endpointswaps afterfull021 pipeline, followedbytwoordinaryrefines onlyifchanged. Frozenunmeasured; rootwilltestafterspeedparity.

Cached021 combined State geometry/delta plusRefineState geometry/tie masks: all320 outputhashes identical021, total250867386,max3.530s sharedload; readiness38max3.212s. Qualifiedspeedport. Best022250872488 (+5102) savedafterdual-SA finalchoice restoresonecell case213; readiness20max3.314s.
Pruningneutral/negativecontributionops exactlyvia backwardwishpropagation followedby4refines:150canonical randomsubsequence/floorcheckspass; prune_best022 smoke ties022, max3.083s. No stableyet.
Newexactbinarysearch: N4,D3,C2 packed25bit states; forwardBFSthrough3ops and backwardBFSthrough2ops fromallfeasiblestampcolors.1280canonicaltransition/involutionchecks and25randomreachablepaths pass. Finds5-op perfecttarget forcase019; binary_cached022 smoke+62500 all20valid, fullstable/readinesspending. UsesnoinstanceIDs inalgorithm.
Exactthree-step search for<=144actions testedagainst12canonicalexhaustiveinstances; matchesbest022 onall3applicablestablecases, no newscoreopportunity. Prototypeexact_three_cached.py retainedbutnotpromoted.
Best023 saved250921331 (+48843 over022), boundaryweightedconstructorselectiononlyN>16 withallcaches; readiness38max3.284s. Weightedpostrefinement250917307 andcachedtriple250907216 bothqualifiedbutwere supersededbeforepromotion; preservecomponentsfornextmerge.

Best024: binary_cached022.py scored250934988 (+13657 over023; +62500 over its022 parent). All320 valid, readiness38/38 maximum2.582s. Saved immutable checkpoint024. The independent binary branch and023 large-board selector are being combined in pool_binary_composite.py; smoke17919570 is the expected +62500 over023. Fullstable and readiness are running before promotion.
Full regression discovery after024:123 tests passed in62.092s. Root prune_best022 development is running; generator informed endpoint stable/readiness runs alongside the composite. All other new heavy work is held so an isolated maximum-size stress test can follow when these finish.

Best025: selector+binary composite250983831 (+48843 over024), all320valid, readiness38max2.873s; every output hash matches the intended023/024 parent.
Best026: informed endpoint proposal in annealed pair repair251149505 (+165674 over025), all320valid, readiness20max2.932s. Isolated36 maximum-size holdout PASS, maximum3.136s, p952.894s, mean1.538s. Endpoint mode1 now selects the exact immediate best action on the omitted-pair boundary; other modes, temperature, budget and seed formula remain unchanged. Full fixed comparison against022 has24wins and8losses.
The informed helper is being transplanted onto025 as pool_binary_informed.py; AST audit shows only anneal_walk changes. All high-cost jobs were paused for the isolated run and can now resume.

Exact-three diagnostic expanded to all 12 stable K=3 cases. Every exact optimum ties checkpoint026; D=2 cases max0.213s, D=3 max2.967s under shared load. No score opportunity, so no full benchmark or integration. New hypothesis: annealed replacement of two separated operations with a fixed intervening block can escape adjacent-pair/triple local optima. Implement a moving omitted-window state and exact best companion with canonical differential checks before smoke.

Best027 saved251,280,679, informed endpoints + exact binary + weighted constructor selector. All320 valid and readiness38 passed max2.898s.
Best028 saved251,305,191 (+24,512), two weighted suffix refinement candidates with parent score floor: eight wins, no losses; readiness38 max3.202s. Isolated36 maximum-size holdout passed, max3.325s,p953.279s,mean1.729s (results/stress_weighted_informed.json).
GapWalker canonical checks:35 random sequences with12 moves each exhaustively verify best companion and moving boundary scores, including negative accepted changes;20 deterministic annealed trials verify parent floor. Prepared gap_weighted.py on028, smoke pending.

Gap annealing on028: smoke ties17,942,045; development improves10,001 across two cases (041 +8264,047 +1737), zero regressions; max3.534s. Full stable started.
Packed late beam for N4,D3:1280 canonical transitions/involutions and20 exhaustive two-move optima pass. Smoke ties028; targeted seven-case diagnostic also ties, maximum2.546s, so no full run. Next hypothesis: meet-in-the-middle search from the final board using wildcard backward stamp constraints; per-position/color bitsets find exact compatible forward states without enumerating all goal stamps.

Wildcard exact finisher prepared as wildcard_weighted.py. For N4,D3, forward BFS depth4 holds exact packed colors; backward BFS depth4 starts from target plus nine wildcard stamp cells, joined by25x6 position/color bitsets of all forward states. This avoids enumerating goal stamp permutations.1280 packed transition/involution tests and18 reachable targets throughdepth8 validate exact joins and operation budgets. No score measurement yet.

Best029 saved251,345,195 (+40,004), gap-pair annealing on028. Seven wins/no losses; all320 valid max3.841s under shared load, readiness38 max3.191s. Canonical endpoint optimum, moving boundary and score floor checks passed.
Generator triple candidate251,481,350 (+176,159 over028),26 wins/no losses, all320 valid max3.882s, readiness20 max3.518s. Root running isolated36 stress beforepromotion030; other workers hold. Exact constructor snapshot undo on028 has320/320 byte parity/readiness38 max2.870s and is being transplanted to the triple candidate.

Best030 saved251,481,350 (+136,155 over029; +176,159 over028), informed triple annealing. Isolated36 maximum-size holdout passes: max3.953s,p953.808s,mean1.955s. Timing window released. Exact constructor undo on this parent is ready for full parity; forward/backward coordinate sweeps and wildcard finishing now test on030.

Wildcard finisher on030 passes smoke at17,962,810 (tie), then diagnostic seven N4/D3 cases gains125,000: both cases156 and296 reach16/16 with eight extra legal swaps. All seven valid, maximum2.179s; remaining outputs retain parent floor. The diagnostic is not a qualifying benchmark; fixed320 run is now underway on frozen wildcard_triple.py. Large-board behavior unchanged from030.

Exact packed BFS through four operations on N4,D3 ties the sole additional stable K4 case160 at13/16, runtime0.070s. Prototype wildcard_exact_four.py remains parked without full benchmark; no score claim or promotion.

Best031 saved251,606,350 (+125,000 over030), exact wildcard finisher. All320 valid max3.862s; readiness38 max3.710s. Exactly two output hashes differ (156/296), all larger-board behavior retains030 isolated timing evidence.
Partial-goal wildcard extension to N5/6,D3 ties allfour eligible diagnostic cases, max4.308s; parked without full benchmark.
New N4 suffix finisher removes2,4,8,12 trailing operations before exact depth8 completion, retaining parent if no perfect target. Diagnostic adds62,500 on case180, which reaches16/16 in21 operations; max amongseven eligible cases2.347s. Copied qualified constructor classes into wildcard_suffix_fast.py to retain speed; smoke running. Readiness agent independently reviews and tests a10-case tiny-board runtime holdout before promotion.

Future exact-search direction (not implemented): replace expensive N5/6 full forward3 state enumeration with a bounded packed forward beam through4 moves, index all retained states by position/color, and join backward partial-goal constraints through2 moves. This offers a six-operation neighborhood while retaining true parent floor and using fewer forward index states. It may help near-perfect small boards, but no measured gain is claimed.

Wildcard suffix+constructor speed candidate full320 confirmed251,668,850 (+62,500 over031), allvalid,max3.957s. Onlycase180 output hash differs from031. Readiness38 is underway; separate tiny holdout10 passedmax2.077s, branch-coverage tracing still inprogress.
Prepared wildcard_beam_small.py: N5/6 partial-goal finisher now indexes a256-wide packed forward beam throughup to6 steps and joins exact backward constraints through2, rather than full forward3 enumeration. Canonical floor and complete two-move checks pass; no score measurement yet. The pure full-enumeration partial variant was rejected after tyingallfour eligiblecases.

Best032 saved251,668,850, readiness38 max3.138s. Independent tiny-board holdout13/13 valid,max3.885s; three extra fixed-seed reachableC6 cases exercise repeated suffix search with unsolved output and fullinventorybound. Report results/pool_wildcard_suffix_holdout.json preserves inputs/hashes/seeds/branch evidence.

N5..9 beam+wildcard join diagnostic gains27,971 on two cases but one non-improving case costs4.716s. Ablation to forward packed beam alone, allowing two successive six-move repairs, improves55,942 on the same12-case diagnostic with max2.743s: case26575->77 matches,31757->59. No regressions; expensive backward joins add no measured value here and are omitted.24 canonical floor/two-move completeness checks pass;1320 N7..9 transition checks pass. Preparing late_beam_forward.py on qualified forward-coordinate source (251,678,439) to combine independent five large-board improvements with this finishing stage; smoke running.

Best033 saved251,678,439 (+9,589), alternating forward/backward coordinate sweeps. Full320 valid,max3.620s; readiness38 max3.464s. Five single-cell gains and no regressions.
Late-beam repair merged onto033 as late_beam_forward.py, smoke20 valid andtied17,962,810,max4.181s under sharedload. Full320 underway; diagnostic previous parent indicated+55,942 oncases265/317, so expectedtotal251,734,381, unconfirmed untilfullrun.

Prune-plus-two-cleanup experiment on modern late-beam parent ties everydevelopment100 score andoutputhash; nofullrun warranted. Four canonical prune/wrappergroups passed.
Wildcard target cache qualified320 exactoutputparity vs032, readiness38max3.714s. Pairedtinyholdout worst4.480->3.369s; all13 unchanged. Integration fragmentpool_wildcard_cache_fragment.py ready.

Best034 saved251,734,381 (+55,942): late beam two-stage repair adds two matches each on265/317. All320valid,max3.731s; readiness38max3.448s. Targeted packed transition/floor checks passed.

Cap4 late-beam diagnostic adds31,250 over034 (case31759->61),12valid,max2.498s. Built late_beam_four_fast.py onallcombinedspeedports (pool_all_fast); onlyfinalcapchanges. Smoke20 valid,tied17,962,810,max3.302s. Full320 nowrunning; generatorprovidesindependent late-beam smallboardholdouts.


### Checkpoint 035: four late repairs plus exact speed ports
Stable 320 total251,765,631 (+31,250 over034), all valid, max3.337s; readiness38 max3.010s. Isolated N30/K180 holdout36: all valid, max3.391s,p953.368s,mean1.802s. Saved submissions/best_035_251765631.py. Only late repair cap2→4 changes score; count/snapshot/cache ports preserve parent search. Independent late-beam13 holdouts valid; canonical transition and floor tests passed.

### Parallel refinement count planes (ongoing)
Hypothesis: updating match-count bit planes for all affected patches together avoids copying all region counts and revisiting each changed region. Added cached cover bitsets and binary increment/decrement in RefineState.apply. WeightedRefineState untouched. Exact1200 mixed actual/wish state transitions and24 complete sweeps agree with035. Alternating microtiming 2500applications perconfig measured1.13–1.33x faster acrossN6/16/30,D2/3; full solver parity/speed pending.

Planes-only follow-up: regioncounts are unnecessary once bitplanes are initialized; RefineState now discards them and trial snapshots handleNone. Separate source refine_planes_only.py.6groups passed (bothcandidatevariants,1200transitions+24sweeps+600nestedtrialsteps each); smokeall20outputhashesexpectedexact,score17,962,810,max3.048s; full320ongoing. Applymicro1.23–1.45x. AllWeightedRefineState behavior unchanged.
Inventory audit035:115/320already atcolor-bound. Most largest scoregaps are tinyK with no spareoperations. Retained late-beam extra512width/depth8 prepared on035,24canonicalhelpercasespassed; diagnosticqueued. Separate late_beam_inventory_gate.py removes raw<=8wrongcellguard because inventory-limited cases may have few recoverable errors despite many permanent errors; onlynewfrozeneligiblecase233,diagnosticqueued. No score claimyet.


### Checkpoints036 and037
Commutator036:251,771,548, all320valid,319parent035hashesunchanged, one+1cellcase173;readiness38max3.088,stablemax3.252. Hottriple037:251,801,728,+36,097vs035(8wins0loss),readiness20max3.122,stablemax3.741;all100devoutputsrepeatstable. Bothimmutablecheckpoints saved in order.037totalbestbut036hasacomplementarygain;combinedcandidatewillbemeasured.
Planes-only speedportcomplete:320exact035hashes,readiness38passedmax2.667;sharedstablemax3.352,sum292.311. No whole-solver speedclaimfromsharedtimings. Generatorcomposesqualifiedport+hotthencomm.

Deep retained beam diagnostic035:8eligiblevalid,+43,403 (056+1cell27,778 and317+1cell15,625),max3.333s. Source late_beam_deeper.py leaves original256wide6depth4repair path untouched, then addsone512wide8depthattempt forN5..9,D3,spare>=3,<=8errors, exactparentfloor. Helper24canonicalknownreachable/floor/budgetcasespassed. Smoke/full qualificationpending;predictedtotal251809034 exceeds037. Inventorygate ablation onlyneweligible233ties outputexact in1.825s;parked.

Independent planes-only reviewfoundnoissues; auditedallcountconsumersandWeightedRefineStateASTidentity. Additionaloraclespassed168boundary/wildcardtransitions,120scalarbest/tiechecks,16nestedrestorepairs,96weightedtransitionswithbothcachewarmuporders,724covermasks. Reportresults/pool_refine_planes_review.json.
Pendingrootnextproposal: globalPQPpatchswapappend can exchangedisjointpatches while restoringstamp; copiedcanonicalcommutatorgain/restorationenginewith3operationwordandallplacementseconds.288canonicalworddeltas/restorationsplus8independentreachablepatchswapgain/determinism/restorationtests passed. Fileslate_palindrome_append.py(localpairs) andlate_patch_swap_append.py(globalpairs) unmeasured.


### Checkpoint038: retained deeper late beam
Stable251,809,034 (+43,403vs035,+7,306vs037),320valid,max3.924(sharedload),readiness38max3.100. Independent13holdouts allvalidwithcanonical/probeparity,max3.375mean2.542;6enteredsearch,4reacheddepth8,3repaired(includingdepth8success). Savedbest_038_251809034.py;current.pycopiesit.
Hot+comm+planes compositionqualified251,807,645,exactpercasemax036/037hashes,readiness20max2.785,stablemax3.498. Doesnotexceed038so no newcheckpoint;sourceanneal_hot_commutator_fast.py isbasisforallcomponentsmerge. Annealedfourwindow035qualified251,778,027,4singlecellwins(005,213,219,287),readiness38max3.296;first3complementhot+11,025.
Best-firstsuccessful-layerbeamvariantpassed10exhaustivetwo-leveloracles but all8affectedcasesexacttie038,so parked. Two-successivedeeprepairsvariant nowtests only2caseswherefirstrepairwasfound;nochangeselse.

Doubledeeprepair variant:onlytwoqualifying035→038improvedcases056/317 rerun;bothexact038hashes,max2.655;nofulljustified. Stamp-awarebeamvariant late_stamp_beam.py addsnew8depth384widthsearchonretained038,withsecondaryrankcachedsumofresidualdesiredcolorcounts onstamp.20canonicalfloor/budget/two-stepchecks passed;targeteddiagnosticrunning.
GlobalPQPon035 duplicatedcomm173gainbut3movesinstead4;localPQP13alltie. Sequentialcomm036→globalPQPdiagnostic13findsoneadditional173cell+5917vs036,max2.679allvalid. Readinessagentpreparesallcomponents+PQPmerge forlaterqualification.

All-repairs compositionqualifiedexactunion251,862,073 (+53,039vs038),320validmax3.945,readiness38max2.938;isolated36maximumstresspendingbeforecheckpoint039. Finalcombinedsourceanneal_all_repairs_complete.py preparedfromallrepairs+PQP+stamp-awarebeam+broaderlowKpackedbeam. Componentshavenewdiagnosticgains5917+12345+6993;expectedunion251887328 isonlyhypothesisuntilfull. LowK26eligiblevalid(+6993cases182/310),max2.558,standalonesmoke/devexact038.
Prune-then-cycles hypothesis: zero-contributionoperations canfreebudgetfor a laterrepair evenwhencleanup-alonepruningties. Source late_prune_cycles.py(038parent) allowsrawprunedtie internally, triesonecommutator+onePQP with10000paircap, thenreturns onlystrictfinalgain.18inversepair-knownsequencefloor/K/determinismcasespass;smoke20validtiedmax3.303. Developmentqueueduntiltimingrelease.


### Checkpoint039 saved
Combinedallrepairs251,862,073,320validmax3.945(shared),readiness38max2.938;isolated36allvalidmax3.336p953.264mean1.781. Savedimmutablebest_039_251862073.py,current.pycopiesit. Timingwindowreleased.
Prune-then-cycledevelopment100rejected:80,314,429,allscore/outputhashesexact038,max3.301. No fulljustified. Rootwidth256vs384stamp-awarebeam ablation pending7eligiblecasesdiagnostic:seeklesslatebeamcostwithoutlosing265boundgain,notclaimingsameuntilmeasured.


### Qualification: algebra27_t3_r5
Hypothesis: Five sparse routing repairs recover additional mismatches within the same bounded permutation search. Packed source 9541 bytes; fixed benchmark unchanged.
Saved checkpoint 042: stable 252085720, delta +47113, all320 valid, max 3.609s, readiness20 valid; submissions/best_042_252085720.py.


### Qualification: algebra27_t3_r8
Hypothesis: Size-adaptive sparse routing through eight profitable repairs after three relocation rounds. Packed source 9546 bytes; fixed benchmark unchanged.


## Round4: algebraic routing and temporal relocation
Starting best039 =251862073. Frozen320 manifest unchanged. The revised statement includes a10000-byte source limit, absent from prior readiness checks; old039 is107628bytes. Old checkpoints are preserved as historical benchmarks. Readiness and promotion now enforce10000B. The exact literal LZMA wrapper is decoded without execution and the inner program undergoes the existing dependency/filesystem/dynamic-execution checks. New compact files use a Python Latin-1 source encoding and must retain their saved bytes.

Hypotheses: (1) compositions (P Q)^3 cancel unaffected three-cycles and isolate small useful permutations; (2) cancel inverse operation pairs to free budget without changing grid or stamp; (3) optimize operation insertion at every temporal boundary, and remove/reinsert low-value operations against backward-propagated final wishes. Earlier constructor/search layers are replaced by these compact approaches, retaining informed core027. This is a change of solver architecture, not a claim that compression alone preserves039's score.

Fresh039 repeat:320/320 output hashes identical to saved039 evidence. Compact027 cache:320 valid,total251280679. New insertion/deletion deltas verified against exhaustive canonical oracles. Macro permutation and packing tests passed; independent reviews continue.

Checkpoint040:251963428 (+101355 over039),320valid,max3.583s,readiness20valid,max3.493s,9548B. Three global relocation rounds and three sparse routes.
Checkpoint041:252038607 (+75179 over040),320valid,max3.441s,readiness20valid,max3.080s,9539B. Four sparse routes.

Rejected directions: longer6/10/16-operation suffix-wish block reconstruction and causal-gap reconstruction both tied all100 development cases; color-scarcity weighted refinement also tied100. Generic exact three-operation tail finishing tied18 eligible core027 cases. No promotion for these. Detailed reports are in notes/regret_experiments.md and results/regret_*.json.

Increasing global relocation rounds5 to8 at five deletion candidates tied the cached full320 total252152063; increasing to10 rounds/eight candidates also tied the corresponding route12 result252192457. No checkpoint is awarded for these ties. The route12 candidate keeps8 rounds for its frozen configuration; final timing will include its actual cost.
Saved checkpoint 043: stable 252147480, delta +61760, all320 valid, max 4.148s, readiness20 valid; submissions/best_043_252147480.py.


### Qualification: algebra27_t5_r8
Hypothesis: Search five low-loss deletion candidates across five global relocation rounds before sparse routing. Packed source 9545 bytes; fixed benchmark unchanged.


### User correction: source limit100000 bytes
The user clarified that the submitted-source limit is100000 bytes, not10000. problem.md now agrees. Updated readiness/promotion/qualification checks and boundary tests to100000. Earlier round4 compact checkpoints remain valid because they met the stricter bound; future candidates can keep all039 methods in ordinary Python after whitespace compaction. No prior checkpoint or evidence is overwritten. Continuing original ten-improvement task.
Saved checkpoint 044: stable 252152063, delta +4583, all320 valid, max 3.786s, readiness20 valid; submissions/best_044_252152063.py.


### Qualification: algebra27_t8_r12
Hypothesis: Complete up to twelve profitable sparse routes on smaller boards with bounded larger-board work. Packed source 9541 bytes; fixed benchmark unchanged.
Saved checkpoint 045: stable 252192457, delta +40394, all320 valid, max 3.793s, readiness20 valid; submissions/best_045_252192457.py.


### Qualification: algebra39_b3
Hypothesis: Retain full prior search portfolio with exact temporal relocation and bit-parallel six-operation permutation routing; plain Python below100000 bytes. Packed source 87946 bytes; fixed benchmark unchanged.


### Full-core integration after100000-byte correction
New plainPython candidatealgebra39_cycles.py is88186bytes. AST-preserving token whitespace compaction retains names and requires no decompression. Restored all039 specialized searches; appended exact temporal repair plus bit-parallel permutation routing. The bit scorer preserves scalar operations exactly:40 cachedpaths and36 freshfullpowerholdouts match;maxhelper0.133s versus1.485s scalar. The fastengine funds30 profitable six-operation repairs and complementary12/18/10/24-operation cycles. Cached320diagnostics: b3=252388472; b12=252571424; b30=252747393; cycles=252862932, with53wins/no losses versus039 forcycles. These are diagnostic projections until their full CLI benchmarks complete.
Independentreviewpassed symbolic/canonical permutations, shiftedcolor masks, legalanchors, signedoffsets, count-plane overflow bounds, and earliest-action ties. Metadata inresults/route_bits_full_power_holdout.json andresults/temporal_review.json.
Saved checkpoint 046: stable 252388472, delta +196015, all320 valid, max 3.713s, readiness20 valid; submissions/best_046_252388472.py.


### Qualification: algebra39_b12
Hypothesis: Expanded global relocation plus twelve size-adaptive sparse repairs using exact parallel anchor scoring. Packed source 87947 bytes; fixed benchmark unchanged.
Saved checkpoint 047: stable 252571424, delta +182952, all320 valid, max 3.838s, readiness20 valid; submissions/best_047_252571424.py.


### Qualification: algebra39_b30
Hypothesis: Fast exact anchor scoring funds up to thirty profitable sparse routing steps across all board sizes. Packed source 87923 bytes; fixed benchmark unchanged.
Saved checkpoint 048: stable 252747393, delta +175969, all320 valid, max 4.566s, readiness20 valid; submissions/best_048_252747393.py.


### Qualification: algebra39_cycles
Hypothesis: Complement six-operation repairs with twelve-, eighteen-, ten-, and twenty-four-operation cycle powers and revisit shorter generators. Packed source 88186 bytes; fixed benchmark unchanged.
Saved checkpoint 049: stable 252862932, delta +115539, all320 valid, max 4.996s, readiness20 valid; submissions/best_049_252862932.py.


### Final runtime review and proven-bound shortcut

The ten requested score improvements are checkpoints040-049. Final049 improves
53 stable cases, ties267, and loses none relative to039. All50 historical source
hashes and all320 frozen inputs passed the independent integrity audit.

Additional049 validation passed36 maximum-size cases (max4.868s) and13 deeper-beam
holdouts. An initial tracing-harness mismatch was corrected; canonical outputs
were valid. The separate slow-case repeat found a real issue: case265 first ran
in3.868s and then exceeded the five-second timeout at5.026s.

New candidate runtime_route_early_bound.py tries cheap sparse routing before the
expensive late beam on small D3 boards, and accepts only a solution at the global
color-inventory upper bound. Failed probes leave the old search and random state
unchanged. Independent canonical and AST reviews passed. Fullstable320 now
passes with exactly252862932, no per-case score changes, max4.947s; readiness20
passes, max4.607s. Case265 is1.894s in this full run. Repeated slow cases and
maximum-size/small-board holdouts are being rerun before selecting the variant.

This is a runtime-only tie, not an eleventh score improvement. If final checks
pass, retain strict history049 and save a separate immutable runtime variant.


### Large-board runtime margin and exact speed ports

The early-bound-only variant retained the full stable score, but a separate
maximum-size reachable D3/C6 holdout timed out at5.015s. Its previous049 output
had722matches and took4.868s. This second real timing failure is preserved in
results/runtime_route_early_stress.json; the candidate was not selected.

Profile-guided exact speed ports now cache immutable target masks, initialize
refinement count planes from mismatch cover masks, defer insertion tie ranking
until a gain can improve the incumbent, fuse backward grid/wish transitions,
use stable heap top-eight selection, and update construction match-count planes
in parallel. The original searches and random draws are preserved.

Initializer equivalence:60configs and1800mixedupdates, best-action and every-field
parity, cached-row isolation. Stable top-eight selection:400 randomized oracles.
Temporal helpers:35configs x30mixedtransitions and24 complete repair comparisons;
large D3 temporal micro1.52x faster. State.apply:1920canonicaltransitions,
64escape/RNG/restores,32clonechecks,48involutions;micro1.19-1.55x faster.
The alternate transposed RefineState.apply was rejected for inconclusive speed.

Preliminary combinedv1 large holdout checks produced the exact049 output hash,
722matches,180operations in3.431s and3.406s. Finalcombined adds the validated
State.apply speed port and is91944bytes. All qualification uses frozen
solvers/experiments/runtime_combined_final.py, jobs1 and five-second timeouts.


### Final selection: runtime_049_252862932.py

All final checks passed: smoke20 max3.775s; stable320 total252862932,max4.010s;
readiness20 plus deterministic repeat max3.067s;19slow-case repeats max3.635s;
36maximum-size holdouts max4.795s;13small-board holdouts max3.766s. All320 output
hashes match the early-bound variant exactly. Former large timeout now2.881s
with722matches; former small timeout fourrepeats1.273-1.577s. Maximumobserved
runtime4.795s stillleavesnarrow0.205s margin; judge/hiddenruntime notguaranteed.

Saved immutable submissions/runtime_049_252862932.py (91944bytes), siximmutable
validation reports, and results/runtime_variants.json. Updated best.json and
current.py to this verifiedruntime-onlytie. All50strictscorecheckpoints and
history.csv preserved. Round4's ten strictscoreimprovements remain040-049.
Final source SHA2563330e36b6f33ca8fe42b976ef11319b5536c2dcd137ba1b5c505b1e6079ca068.
Report: notes/round4_report.md. Finalintegrityaudit: results/round4_final_integrity.json.

### Requested i1 review: exact suffix-label block beam

Reviewed notes/idea/i1.md against the experiment history and current source.
Most mechanisms already exist. The new combination is a full-state beam for
internal block reconstruction using the exact backward labels of a fixed
suffix; earlier 6/10/16-gap reconstruction was greedy or two-step lookahead.
Hypothesis: retaining competing paths through the gap can improve coordinated
pickup/deposit choices. Test a separate retained-parent variant of runtime049,
with fixed expansion budgets, exact wildcard/stamp objectives, and strict score
floor. Full details and results are kept in notes/i1_review.md.
Requested i1 experiment completed: full-state block beam on runtime049 yields
252894799 (+31867), six wins/314 ties/no losses on stable320, all valid,
max3.737s. Readiness20 plus deterministic repeat passed max3.302s; maximum-size
36-case holdout passed max4.284s. All six new winning outputs reproduced exactly.
Saved immutable best_050_252894799.py (98653 bytes), benchmark/readiness copies,
history row50 and updated best.json/current.py. Initial smoke tied18045220;
dev100 gained1479. Internal-first ablation tied smoke and was parked. All gains
came from suffix reconstruction at depth4/5/8; no separate benefit from internal
live suffix labels was measured. Canonical/exhaustive objective tests passed.
Full audit, commands, coverage limits and results: notes/i1_review.md.

### Continued session: retained suffix reconstruction
Hypothesis: an additional suffix beam with alternate width/depth can escape the latest retained beam trajectory. Parent is immutable best050; canonical final scoring accepts only strict gains. Extra budget is120000 transitions, deterministic input-derived seed.
Development100 diagnostics (cached verified parent outputs, provisional shared-machine runtimes): width8/depth4 tied; width6/depth6 gained3086 in one case; width4/depth10 gained8279 in five cases (001,015,018,071,086). No losses. Incremental aggregate9.065s, max0.566s for width4/depth10. Candidate99710bytes, source standard-library only. Proceed to smoke and unchanged stable320 before any promotion. Evidence: results/session_suffix_diagnostic.json; plan notes/session_plan.md.

### Parallel breadth probes in continued session
Exact short-horizon meet-in-the-middle: all nine eligible frozen cases already match the exact optimum; rejected as a score direction. Sixteen canonical exhaustive comparisons passed. A separately proven N=D shortcut reduces the entire reachable board orbit to existing exact_two(K<=2). See notes/session_small.md.
Segment rotation conjugation: rotate every action in one contiguous interval by the same offset, propagate sparse endpoint differences, score with exact backward wishes, and verify the accepted edit independently with SequenceState.delta. Cached development100 gain5442, threewins/97ties/no losses (007,043,063); additional aggregate2.119s,max0.218s under shared load. Exhaustive25200mutations plus648independent reviewer mutations passed. See notes/session_sequence.md.
Combined hypothesis: append the exact segment-rotation best edit after retained suffix reconstruction and add the proven N=D early exact shortcut. All score edits retain their parent floor. solvers/experiments/session_combined.py is99738bytes after token whitespace compaction, removal of six unused docstrings, and reversible renaming of four identifiers; reversible AST equivalence is recorded in results/session_combined_compaction.json. Prepared for qualification after the suffix candidate; no best claim yet.

Suffix full stable320 completed:252909754, average790342.98125, +14955 over050; sevenwins/313ties/no losses, invalid0. Aggregate381.612s,max4.669s. Improved cases001,015,018,071,086,170,286 each gain one match. Readiness20passed,max3.706s. Stress/reproduction gate still pending at this entry.

Saved immutable checkpoint051:252909754; readiness20 passed, stress36 passed(max4.188s,p954.032s,average2.220s), all seven winning output hashes reproduced. File submissions/best_051_252909754.py. Full supporting JSON reports use results/session_suffix_*.json.

Combined full stable320:252937025, average790428.203125, +27271 over051; elevenwins/309ties/no losses, invalid0. Aggregate353.798s,max4.174s. This is +42226 over050 and +24631054(+10.7886%) over initial000. Readiness38 passed,max3.807s; final stress/reproduction gates pending at this entry. Score gains come from exact segment rotation; N=D shortcut is a runtime change with equal optimal scores.

Saved immutable checkpoint052:252937025. Readiness38 passed; maximum-size36 passed(max4.351s); all eleven new winning outputs reproduced exactly. Final source99738bytes; current.py matches best052. Fresh integrity verified all53checkpoint hashes and320frozen inputs. Complete report: notes/session_report.md. Worst final observed runtime4.351s. Final profile and canonical case007 gain check also passed.


### Million-point improvement campaign (2026-09-26)
Starting checkpoint052:252937025 on unchanged stable320. Requested threshold253937025 (+1000000). Existing infrastructure and immutable initial/checkpoints reused. Independent probes: early sparse routing/reconstruction; informed small-board search; global sequence annealing; diversified weighted construction. All provisional cache diagnostics use canonical simulation; promote only fresh complete stable/readiness plus isolated maximum-size runtime. Keep source<=100000 bytes and per-case limit5seconds. No dedicated test files.

Million campaign probes: 24 multi-operation perturb/refine trials gave0 dev gain; width12 longbeam+176433 vs050, width24+253535 vs050 (+241186 vs052), width48+295215 vs052 but excess maximum additional cost2.45s. Full320 cached width24 gave+894028 over052. New quotient small-board beam gave+135749 complementary; prefix macro reconstruction+104785; objective perturbation8trials+52045. These independent deltas are not added as final evidence because interaction/runtime gating can change paths.
Final hypothesis: retain052 except largest D3 (N>=24,K>=120), where saved pre-suffix stage _i1_parent reserves time for width16 longbeam; width24 otherwise. Apply quotient small-stage, bounded prefix macro reconstruction with proven safe cutoff, then8objective trials except largestD3. Expected combined gain>1M; final needs full320 measurement. Source99011 bytes, readable research source retained, reversible token-name compaction AST checks passed. Final smoke20 passed total18148426,max4.250s; stable isolated jobs1 running. Independent reviews: 6075beam choices/transitions,3000quotient transitions,60macro random+15repeats,30objectiveparity checks; merged small-edge cases passed.

Byte audit caught CRLF expansion during generated-source writes; normalized exact final source toLF with write_bytes. Actual99011bytes,SHA2560629d2b4e63e2772a4f06795041e115ea9b2b62bbc5536e9c21f5661de9bb7fa. Static inspect_source passes all dependency/I/O/source-size checks; reverse compaction AST equals readable source. Oversized runs aborted, final gates restarted on normalized bytes.

Fresh standalone stable320: 254103898,delta+1166873 vs052;81wins/239ties/0losses;invalid0;runtime420.485s,max4.608s. Target+1000000 met by score. Readiness/holdout gates still pending; no checkpoint yet.

Runtime boundary failure preserved: checkpoint053 times out on independent N23,D3,C6,K180 holdout at5.029s. Hypothesis: using the earlier portfolio stage for N20..23,D3,K>=120 frees time before new beam. Keep beam width and all later phases unchanged. Four affected stable inputs inspected:009/302 already at color upper bound,046 earlier stage same score,270 beam decisively wins; expect exact score parity, to be measured. New runtime variant preserves053 immutable.

Runtime adjustment reproduces all four affected stable outputs exactly; prior N23 timeout now4.398s,valid812854. Expanded early-parent selection only; new beam widths and following phases unchanged. Candidate99031bytes SHA2568044713f3496957bd0389d681f672ea6169eabc25e34a727eacb46a9a9a6e297. Static/readable reverse-AST parity passed. Full320/readiness/max-size/boundary replay running, to select as runtime-only variant if exact score tie confirmed.

First runtime variant rejected: three stable timeouts158/173/205 despite initial successful runs; all completed outputs identical. Further bounded work allocation: skip extra longbeam/objective attempts on smallD3 boards already>=88%of color bound andK>=100, use earlier parent forN>=20,D3,K>=100, cap small quotient exploration at600000 transitions whenK>8. New million_safe.py99261bytes. All36affected stable cases valid with exactly equal scores (one harmless tied sequence change);all18boundary holdouts valid,max4.290s. Prior timed cases now3.29-3.57s. Full fresh final qualification started.

Final safe variant fullstable320 passed,total254103898,all320 per-case scores exactly match053,319identical output hashes. Invalid0, runtime424.724s,max4.341s. Original+1166873 gain fully retained. Final readiness/max-size checks underway.

Selected immutable submissions/runtime_053_254103898.py:254103898,+1166873 over starting052;81wins,no regressions. All320 scores reproduced;319 identical outputs. Final smoke20,stable320,readiness38,maximum-size36,andboundary18 passed;worst verified4.820s. Current/best.json/runtime_variants updated; all54strict checkpoints retained unchanged. Full report:notes/million_report.md.


### Seven-million campaign
Start254103898, target261103898 on unchanged stable320. Four parallel directions: new forward construction potentials, backward/mixed wildcard construction, distant/global sequence search, and rigorous upper bounds. Experiments and measurements: notes/seven_campaign.md and notes/seven_*.md. Root promotes only fully verified strict improvements.

Saved checkpoint054:254492748 (+388850 over053),22wins4losses320valid,max4.655s. Readiness38passedmax4.374;max-size36passedmax4.566;periodic14passedmax4.231;all26changedoutputs reproducedexactly. Source27492bytes,standard-librarylosslesswrapper. Bestfile:submissions/best_054_254492748.py. Target261103898 remains unmet.

Saved checkpoint055:254652429 (+159681 over054/+548531 campaign),320valid,41wins6lossesagainst053,max4.685s. Readiness38passedmax4.901;max-size36passedmax4.831;periodic14passedmax4.316;all47changedoutputsreproducedexactly. Source28702bytes. Investigatingexactscore-parityclusterstateperformanceportbecauseboundaryruntimeiscloseto5s.


Further scoring experiments were measured and rejected. Long-window reconstruction
searched 12, 24, and 32 moves jointly against exact suffix wishes. Strict and
neutral variants found no new score gain on 36 eligible development cases beyond
already cached paths and checkpoint 055. Two shifted global-assignment layers,
including independent transfer rotations, produced no wins on 13 eligible
 development cases. Canonical validation passed; no experimental gain is credited.
Details: notes/seven_construct.md and notes/seven_sequence_layered.md.

The private cluster-state performance port preserves all 320 output hashes and
scores. Its stable run took 445.680 seconds (previously 456.433), with a maximum
of 4.964 seconds. Readiness 38 and maximum-size 36 passed; maximum-size time fell
from 4.831 to 4.620 seconds. A further stamp-plane cache had a 74.6% hit rate but
only about a 1% helper improvement and no large-case timing benefit. That cache
was rejected. Final periodic and changed-output reproduction checks are pending
before selecting the bytearray performance port as an equal-score variant.


Final seven-million campaign selection: submissions/runtime_055_254652429.py,
29,022 bytes, score 254,652,429 (+548,531). It reproduces all 320 checkpoint055
scores and output hashes. Readiness 38, maximum-size 36, periodic 14, and all 47
changed-output reproductions passed. Worst measured time: 4.964 seconds of five.
All 56 strict checkpoint hashes and all 320 input hashes were verified. The
runtime-only selection is recorded separately; score checkpoints 054 and 055
remain immutable. The requested gain remains unmet by 6,451,469 points.
Complete report: notes/seven_report.md; machine summary: results/seven_final_summary.json.

## Million-point campaign from055
Checkpoint056:255,006,286 (+353,857 over055),320valid,375.834s total,max4.070s. Early width64 quotient forward construction pluscluster16, generalized12-step3cycle/conjugation tail repair, exact packed refinement initialization/scoring. Readiness38,max-size36,and36 changed outputs reproduced; worstverification4.395s. File:submissions/best_056_255006286.py. Research and next experiments:notes/m2_campaign.md. Requested gain of1,000,000 remains unmet.


## 2026-09-30: isolated Optuna simulated-annealing tuning

User requested a separate folder containing continuously resumable Optuna parameter search. Added optuna_tuning/ with a standalone greedy-plus-sequence-SA solver, canonical subprocess evaluation, SQLite/TPE tuner, immutable local checkpoints, tests, and Korean instructions. Hypothesis: optimizing temperatures and mutation distribution improves final-match sequence search within five seconds. Original solvers/checkpoints and frozen cases were preserved.

Unchanged stable320: initial greedy 228,305,971; default SA (3,000 iterations) 236,948,550 (+8,642,579); Optuna trial5 240,667,550 (+3,719,000 over default SA). Trial5 improved 110 cases and regressed 6 relative to default SA. All three passed stable320, readiness38, and full stable output reproduction. Tuned maximum observed qualification runtime: 0.683s. Thirteen actual trials (12 complete, one pruned) included stop/resume verification; tuning used smoke20 and full stable evaluation was separate.

SA-local checkpoints and history: optuna_tuning/runs/smoke_demo/verified/; best: best_002_240667550.py. Global best remains submissions/best_056_255006286.py at 255,006,286. New tests: 30 passed. Full discovery: 294 passed; existing CLI scripts tools.test_regret_cached27, tools.test_regret_rebuild, and tools.test_regret_variants fail discovery by parsing unittest arguments at import. Details: optuna_tuning/results/verification.md, verification.json, project-tests.log. Continuous tuning was not left running in the background.
