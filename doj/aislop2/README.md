# Heuristic stamp solver laboratory

The official objective and swap semantics are in `problem.md`. The limits are **5,000 ms per input** and **100,000 source bytes**, as corrected by the user during round4. Solvers use standard-library Python, read one instance from stdin, and write only the operation count and operations. Python 3.10+ is required for `int.bit_count`; measurements here use CPython 3.12.12 on this machine.

## Pick a submission

The current measured best is recorded in [`results/best.json`](results/best.json). The [checkpoint history](results/history.csv) includes every strict improvement. The [initial-round report](notes/final_report.md) is a snapshot from before ongoing optimization resumed.

The renewed million-point campaign has saved [`submissions/best_056_255006286.py`](submissions/best_056_255006286.py): **255,006,286**, a verified **+353,857** over runtime055. Stable320, readiness38, maximum-size36, and reproduction of all36 changed-score outputs passed. Worst qualification runtime: **4.395s**. The requested threshold is **255,652,429**; research continues in [the campaign log](notes/m2_campaign.md). `solvers/current.py` matches this checkpoint.

The seven-million campaign selects [`submissions/runtime_055_254652429.py`](submissions/runtime_055_254652429.py): **254,652,429**, a measured **+548,531** over runtime053 on the unchanged stable320 suite. All 320 cases are valid and their outputs exactly match score checkpoint 055; readiness 38, maximum-size 36, periodic 14, and reproduction of all 47 changed outputs passed. Stable total runtime fell from 456.433 to 445.680 seconds. Worst observed qualification time: **4.964s**, leaving limited margin below five seconds. The requested +7,000,000 remains unmet. The **29,022-byte** self-contained file uses a lossless standard-library wrapper; readable source and research details are in [the campaign report](notes/seven_report.md). `solvers/current.py` matches this selected file. Both new score checkpoints 054 and 055 remain immutable.

The million-point campaign selected [`submissions/runtime_053_254103898.py`](submissions/runtime_053_254103898.py): **254,103,898** on the unchanged stable320 suite, **+1,166,873** over checkpoint052, with **81 wins and no regressions**. The **99,261-byte** standalone file passed stable320,readiness38,maximum-size36 and18additional boundary checks; worst final observed time **4.820s**. It preserves every per-case score of checkpoint053 while addressing later runtime failures. See [the complete campaign report](notes/million_report.md). This historical selection remains preserved.

The previous continued session selected [`submissions/best_052_252937025.py`](submissions/best_052_252937025.py): **252,937,025** on unchanged stable 320, average **790,428.20**. New strict checkpoints 051 and 052 add 42,226 over 050 with eighteen improved cases and no regressions. Readiness 38 and all 36 maximum-size holdouts passed; worst observed final runtime **4.351s**. The file is **99,738 bytes** and that historical source remains preserved. See [the complete session report](notes/session_report.md) for all checkpoint scores, successful and rejected probes, and verification evidence.

The i1 review produced [`submissions/best_050_252894799.py`](submissions/best_050_252894799.py): **252,894,799** on the unchanged 320-case suite, **+31,867** over runtime049, six improved cases and no regressions. It is **98,653 bytes**; readiness and 36 maximum-size holdouts passed, with a worst observed time of **4.284 seconds**. See [`notes/i1_review.md`](notes/i1_review.md) for the prior-method audit, block-beam experiment, and evidence. That checkpoint remains preserved as the prior best.

Round4 selected [`submissions/runtime_049_252862932.py`](submissions/runtime_049_252862932.py): **252,862,932** on the frozen320 cases, **91,944 bytes**, and all final runtime checks passed. This is a faster variant with the same per-case scores as checkpoint049; the ten new strict improvements040–049 remain immutable. See the [round4 report](notes/round4_report.md) for the complete progression, runtime limits, and validation evidence. Runtime-only selections are recorded separately in [`results/runtime_variants.json`](results/runtime_variants.json).

`results/best.json` identifies the strongest verified submission. `results/history.csv` lists every strict best, its immutable submission filename, source hash, score, and supporting benchmark/readiness reports. `submissions/` files are self-contained: copy the selected `.py` file directly to the judge. `solvers/current.py` tracks work in progress and is not the authority for selecting a submission.

Starting with checkpoint 040, promotion checks submitted-source size. Initial round4 files satisfied the stricter provisional 10,000-byte limit; the user subsequently corrected it to **100,000 bytes**, and the checker follows that correction. Earlier checkpoints and their scores remain historical records; checkpoint039 exceeds even the corrected limit before whitespace compaction. Some intermediate compact checkpoints contain an inspectable standard-library LZMA payload and a Python Latin-1 encoding declaration: upload those exact saved files without converting their encoding. Readable experiment sources remain under `solvers/experiments/`. Readiness decodes only an exact literal wrapper, then inspects the actual program for forbidden dependencies, filesystem access, and further dynamic execution. New final candidates can use ordinary readable Python source under the corrected limit.

## Reproduce

```powershell
python tools/generate_cases.py
python tools/benchmark.py submissions/BEST_FILE.py --suite smoke --jobs 1 --output results/recheck_smoke.json
python tools/benchmark.py submissions/BEST_FILE.py --suite stable --jobs 1 --output results/recheck_stable.json
python tools/check_submission.py submissions/BEST_FILE.py --random 30 --timeout 5 --output results/recheck_readiness.json
python tools/stress_solver.py submissions/BEST_FILE.py --timeout 5 --output results/recheck_stress.json
```

Replace `BEST_FILE.py` with the filename recorded in `results/best.json`. The benchmark exits nonzero on any invalid output or timeout. Use `--jobs 1` for clean runtime measurements; parallel runs can inflate per-process times under contention. Do not run concurrent benchmarks during final runtime checks.

The frozen seed is `20260925`. There are 20 smoke cases, 100 development cases, and 320 stable cases, nested in that order. The full stable suite decides checkpoints. Families include random, near-target, reachable-by-swaps, checkerboard, stripes, repeated-stamp, nearly-uniform, and local-adversarial instances. All legal N values, both D values, all C values, and K endpoints are covered. Additional runtime stress cases are separate holdouts.

`cases/manifest.json` stores seeds, parameters, families, suite memberships, and input hashes. Regeneration refuses different existing files by default. Benchmarks verify input hashes and execute an isolated snapshot of solver bytes, so a later edit cannot contaminate a running result. Every result includes per-case validity, exact integer score, matches, operations, elapsed time, source hash, and parameter/family breakdowns.

## Tools

- `simulate.py`: canonical reference-orientation stamp swaps, parsing, final grid and stamp.
- `validate_output.py`: ASCII integers, byte limit, count, exact token count, coordinates, rotation range.
- `score.py`: exact `(1_000_000 * matches) // (N*N)` scoring.
- `benchmark.py`: frozen suites, subprocess timeouts, JSON evidence, parameter breakdowns.
- `check_submission.py`: syntax/import/I/O inspection, random and boundary inputs, deterministic repeat, bounded subprocess output.
- `stress_solver.py`: sequential maximum-size runtime holdouts.
- `checkpoint.py`: rejects stale evidence, invalid cases, ties, changed benchmark identities, or evidence exceeding five seconds; saves exclusive checkpoint files and evidence.
- `compact_submission.py`: deterministic name/token compaction, bounded standard-library compression, and exact literal-wrapper decoding.
- `qualify_variant.py`: smoke, full stable, readiness, and immutable promotion for one frozen experimental candidate.
- `profile_solver.py`: cProfile report for bottleneck analysis; instrumented runtime is not contest runtime.

Run tools from this repository root. Solver files can run from any directory without local helpers. `notes/experiments.md` is the central log; linked research logs describe hypotheses, successful and failed variants, score deltas, and runtime tradeoffs. All scores are local measurements on generated inputs, not predictions of the official 40-input score.
