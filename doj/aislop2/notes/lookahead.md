# Lookahead experiments

## Hypothesis 1: bounded two-move escape

Strict positive-gain greedy leaves useful stamp transfers unexplored at local maxima. At a plateau, evaluate 32 diverse outgoing stamp states from first moves with gains down to -2, then choose a pair only if its exact total gain is positive. Retain the best output prefix. Pack stamp and target colors as one-hot bit fields so immediate match counts use `int.bit_count`. Maintain local region match counts after each actual or tentative swap.

The candidate budget bounds runtime; a deterministic input-derived PRNG diversifies the first-move candidate sample. Baseline stable score: 228305971; smoke score: 15327134.

Measured `lookahead.py`: smoke 17286944 (20/20 valid, maximum 0.409s); stable 240849239 (320/320 valid, total process runtime 24.321s, maximum 0.477s). Stable delta +12543268. Readiness passed 38/38 cases (maximum 0.231s). Differential packed-gain and swap-state tests pass 80 random trajectories plus 30 solved instances. Candidate frozen for potential checkpoint promotion.

## Hypothesis 2: broader outgoing stamp sampling

The first result leaves substantial runtime headroom. Increasing plateau candidate width from 32 to 128 should find profitable transfers missed by a small sample, especially when only a few outgoing stamp arrangements fit remaining target patches. Keep every other behavior unchanged for this ablation.

Width 128 smoke: 17363100 (20/20 valid, maximum 1.181s). Stable 241275111 (320/320 valid, total process runtime 34.657s, maximum 1.172s), delta +425872 versus width32. Readiness passed 38/38 (maximum 0.610s). The parallel plateau experiment now scores 242249708, so width128 is not the global best and is retained as an experiment.

## Hypothesis 3: diversified positive greedy paths with two-ply escape

Many immediate gains tie; choosing a different tied placement changes the stamp and all later options. Run the original width32 algorithm plus three paths with deterministic shuffled action tie ordering and choose the highest final number of matches. This preserves the original path while adding complementary local maxima exploration. Each restart retains exact positive-total two-ply escape behavior. Compare score gains and maximum runtime before increasing the restart budget.

Four-path smoke 17530904 (20/20 valid, maximum 1.455s). Stable 243391996 (320/320 valid, total process runtime 42.608s, maximum 1.602s), delta +2542757 versus width32 and +1142288 versus the then-global plateau_hot12 best. Readiness passed 38/38 (maximum 0.791s). Candidate frozen in `lookahead_multi4.py` and reported to the root agent for checkpoint promotion.

## Hypothesis 4: two-ply choice during productive greedy steps

Plateau-only lookahead cannot recover opportunities lost earlier, particularly with a tight K budget. At positive-gain states, inspect eight diverse first moves within one point of the best immediate gain, maximize exact two-step total, and execute the selected first move. Require at least +1 immediate gain in these receding-horizon steps, preventing zero-gain loops. Continue width32 positive-total escapes at plateaus. This tests a distinct beam-like decision policy rather than additional restarts.

Productive-step smoke 17428869 (20/20 valid, maximum 0.881s). Stable 242181328 (320/320 valid, total process runtime 32.500s, maximum 0.824s), delta +1332089 versus width32, but -1210668 versus multi4. Readiness passed 38/38 (maximum 0.804s). Candidate retained for complementary behavior, not promoted alone.

## Combined-result analysis

Summing per-case maxima of already measured outputs gives:

- plateau_hot12 + multi4: 244316245.
- multi4 + productive: 244702527.
- plateau_hot12 + multi4 + productive: 245343012.
- Adding width128 to all three: 245407794 (only +64782 for appreciable additional work).

These are measured candidate-output comparisons, not a submitted ensemble benchmark. Root agent is responsible for producing and benchmarking any concrete combined solver. Sum of separately measured maximum per-case times for the three-way combination is 3.23s with two benchmark jobs; shared-process runtime must be checked directly.

All four candidates pass the canonical differential tests in `python -m unittest tools.test_lookahead -v`: each checks 80 random trajectories of 25 operations (packed gains, full grid, full stamp, cached match counts), and 30 complete solver trajectories. Each candidate has its own smoke, stable, and readiness JSON under `results/lookahead*`. Stable benchmark and solver files were not modified after their final measurements.
