# Codex Prompt: Heuristic Stamp Optimization Solver

You are working on a heuristic programming contest problem.

Your task is to build a complete local experimentation environment and then iteratively develop a high-scoring Python solver.

Follow `Agent.md` as the governing workflow.

## Problem Summary

Input gives:

- an `N x N` colored grid `A`,
- an immutable target grid `T`,
- a mutable `D x D` stamp `S`,
- colors `0..C-1`,
- a maximum of `K` operations.

Constraints:

- `3 <= N <= 30`
- `D in {2, 3}`
- `2 <= C <= 6`
- `1 <= K <= 180`

One operation chooses `(x, y, r)` where:

- `0 <= x, y <= N-D`
- `r in {0,1,2,3}`

The stamp is placed with rotation `r`.

For stamp cell `(u,v)`, its destination offset is:

\[
R_r(u,v)=
\begin{cases}
(u,v) & r=0,\\
(v,D-1-u) & r=1,\\
(D-1-u,D-1-v) & r=2,\\
(D-1-v,u) & r=3.
\end{cases}
\]

If `R_r(u,v) = (p,q)`, simultaneously swap:

\[
S_{u,v} \leftrightarrow A_{x+p,y+q}.
\]

After lifting the stamp, its orientation resets, but the colors it picked up stay in the reference-orientation stamp cells.

The target `T` never changes.

After at most `K` operations, let `M` be the number of cells where final `A[i][j] == T[i][j]`.

The official instance score is:

```python
P = (1_000_000 * M) // (N * N)
```

Output:

```text
L
x_0 y_0 r_0
...
x_{L-1} y_{L-1} r_{L-1}
```

with `0 <= L <= K`.

If `L == 0`, print only `0`.

The output file must contain no extra tokens and must be at most 100,000 bytes.

---

## Mandatory First Stage

Do not begin with sophisticated heuristic ideas.

First build the local evaluation environment.

Create:

```text
tools/generate_cases.py
tools/simulate.py
tools/score.py
tools/validate_output.py
tools/benchmark.py
cases/
solvers/
submissions/
results/
notes/
```

Implement a canonical simulator with exact simultaneous-swap semantics.

Do not write dedicated unit-test or test-code files. Verification should be performed through the simulator, generated benchmark cases, validator, and benchmark runs rather than by building a separate test suite.

Implement a strict output validator.

Implement the exact official scoring formula.

Create a reproducible testcase generator using fixed seeds and multiple testcase families, including random, structured, easy, difficult, small, large, low-color, high-color, small-K, and large-K cases.

Build at least:

- a fast smoke benchmark,
- a stable development benchmark.

Keep benchmark seeds fixed after creation.

The benchmark runner must report total score, average score, invalid cases, runtime, and useful parameter breakdowns.

---

## Mandatory Initial Submission Checkpoint

After the tools work, implement a simple correct Python baseline.

Compare at least:

1. zero operations,
2. a best-immediate-operation baseline,
3. repeated greedy immediate improvement if practical.

Choose the best measured baseline.

Then immediately save a self-contained submission-ready copy in:

```text
submissions/best_000_initial.py
```

Record its benchmark score and runtime in:

```text
results/history.csv
```

This initial saved submission is mandatory even if the score is weak.

---

## Exploration Before Deep Optimization

Do not commit too early to one heuristic family.

In the early and middle stages, favor breadth over depth:

1. identify several substantially different approaches,
2. implement each only far enough to obtain a meaningful score,
3. benchmark each approach on the same stable benchmark,
4. document the method, score, runtime, strengths, weaknesses, and notable behavior,
5. compare the results before deciding where to spend deeper optimization effort.

The goal is to build an empirical map of the search space first.

Examples of different directions may include:

- pure immediate greedy,
- stamp-content-aware greedy,
- mismatch-prioritized search,
- shallow lookahead,
- beam search,
- randomized greedy,
- sequence post-optimization,
- local search over operation sequences,
- target-demand or color-routing heuristics.

Do not spend a large amount of time micro-optimizing the first plausible approach before several alternative directions have been measured.

Maintain a comparison document, preferably in:

```text
notes/experiments.md
```

For every explored direction, record at least:

```text
Approach:
Core idea:
Implementation level:
Stable benchmark score:
Average score:
Runtime:
Observed strengths:
Observed weaknesses:
Next-step potential:
```

After several distinct directions have been measured, identify the most promising one or two based on actual score and runtime.

Only then begin concentrated refinement: tune parameters, improve candidate selection, reduce unnecessary computation, add limited lookahead, combine compatible ideas, and squeeze additional score from the promising approaches.

Continue to measure every refinement. If a supposedly promising direction stops improving, return to the comparison table and try another direction rather than forcing increasingly complicated changes into one weak line of attack.

---

## Main Optimization Loop

After the initial checkpoint, repeatedly improve the solver.

Work autonomously.

For each experiment:

1. state a concrete hypothesis in `notes/experiments.md`,
2. modify `solvers/current.py`,
3. run correctness/smoke tests,
4. benchmark promising changes on the stable benchmark,
5. compare against the current best,
6. record the measured score, score delta, runtime, and conclusion.

Whenever and only whenever the stable benchmark total score strictly improves:

1. increment the checkpoint number,
2. copy the complete self-contained solver into `submissions/`,
3. use a filename such as:

```text
best_001_<total_score>.py
best_002_<total_score>.py
```

4. append the result to `results/history.csv`.

Never overwrite or delete an older best checkpoint.

The saved checkpoint itself must be ready to submit directly to the judge.

---

## Solver Requirements

All contest solver code must be Python.

The final solver must:

- use standard input/output only,
- require no third-party packages,
- require no local files,
- print no diagnostics to stdout,
- always produce valid output,
- stay within `K`,
- handle all legal constraints,
- have reasonable worst-case runtime.

Use stderr only for local experiments, and remove or disable unnecessary diagnostics in saved submission files.

---

## Optimization Ideas to Investigate

Do not blindly implement all ideas. Measure them.

Because `D <= 3`, one operation affects at most 9 grid cells. Use local delta evaluation.

Investigate:

- immediate greedy gain,
- mismatch-focused candidate generation,
- stamp-aware value functions,
- valuing useful future stamp contents,
- top-candidate pruning,
- equivalent-rotation elimination,
- 2-ply lookahead,
- beam search,
- short rollouts,
- randomized greedy,
- simulated annealing,
- sequence truncation,
- operation deletion,
- local sequence replacement,
- suffix optimization,
- input-derived deterministic random seeds.

A move with negative immediate grid score may still be useful if it loads the stamp with valuable colors. Explicitly investigate this tradeoff.

Also consider global color availability and local target demand, but do not assume a theory is useful without benchmark evidence.

---

## Performance Engineering

Profile the implementation.

Precompute rotation mappings.

Avoid copying the full `N x N` grid for each candidate move.

Use local apply/undo or compact state copying where appropriate.

Since the number of legal raw actions per state is at most:

```python
4 * (N - D + 1) ** 2
```

design candidate evaluation around this bound.

Track both average and worst-case runtime, especially for:

- `N = 30`,
- `K = 180`,
- `D = 3`.

Reject score improvements that make runtime unacceptably risky.

---

## Correctness Safeguards

The most dangerous source of bugs is stamp state handling.

Remember:

- rotation affects where each reference stamp cell is placed,
- the stamp cells themselves retain reference indices,
- colors taken from the grid are stored back into those corresponding reference stamp cells,
- swaps are simultaneous.

Do not create dedicated test programs or unit-test files. Instead, verify optimized transition logic by running generated/random benchmark instances through both the optimized logic and the canonical simulator when needed.

Before saving every best checkpoint, run practical verification through the existing tooling:

- syntax check,
- smoke benchmark,
- randomized generated-case validation through the canonical simulator,
- maximum-size runtime benchmark.

---

## Benchmark Discipline

Do not change the stable benchmark merely because an experiment scores poorly.

Do not call something an improvement unless the measured stable score is strictly higher.

If using randomized solving:

- fix seeds for development comparisons,
- test multiple seeds when variance is significant,
- prefer robust improvements rather than lucky runs.

Keep enough testcase diversity to reduce overfitting.

Useful reports include score grouped by:

- `D`,
- `C`,
- `N` range,
- `K` range,
- generator family.

Use these breakdowns to identify weaknesses.

---

## Autonomous Working Style

Do not stop after producing only a baseline.

Continue the experiment-measure-improve loop for as long as useful within the available work session.

During exploration, prefer trying many meaningfully different approaches and measuring them rather than spending most of the session deeply tuning one idea.

First establish a broad score comparison across multiple heuristic families. Then focus deeper effort on the approaches that actually show the strongest measured potential.

Prefer several validated incremental improvements over one large speculative rewrite.

When an idea fails, record that it failed and move on.

When an idea succeeds, save the new submission checkpoint immediately before attempting riskier changes.

At any point, there must be a known best submission-ready file that can be used even if later experiments fail.

---

## Final Report

At the end, summarize:

- the benchmark suite,
- the initial baseline score,
- every saved best checkpoint,
- the final best benchmark score,
- major successful ideas,
- major failed ideas,
- runtime characteristics,
- the exact path of the best submission-ready Python file.

Do not label an experimental solver as best unless it actually won on the stable benchmark.

The primary objective is measured contest score, not code aesthetics.
