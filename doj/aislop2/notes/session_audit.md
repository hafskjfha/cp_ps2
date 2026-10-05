# Independent evaluation audit, 2026-09-26

Read-only audit of the current problem statement, generator, simulator, output
validator, scorer, benchmark runner, submission checker, checkpoint promotion,
history and checkpoint 050. No benchmark or solver implementation was changed.
All checks below were inline Python commands using the existing tools; no
dedicated test file was created.

## Verified

- 160 independently implemented matrix-rotation comparisons cover all four
  rotations for both D=2 and D=3. Canonical operation involution, color
  conservation, and one-to-one contact mappings passed. Reference stamp cells
  receive the rotated contact cells, with orientation reset after each move.
- Twelve malformed output examples were rejected, including count/token
  mismatches, illegal coordinates/rotation, nonintegers, non-ASCII data and
  output above 100,000 bytes. Legal zero-operation and boundary examples pass.
- All 321 frozen generator outputs (320 cases and manifest) regenerate
  byte-for-byte. Every input hash and header matches the manifest. All forty
  reachable-family witnesses reproduce their target under the canonical
  simulator. Suite sizes remain 20 smoke, 100 development and 320 stable.
- All 51 history entries retain matching source hashes, benchmark solver hashes,
  readiness hashes, manifest identities and exact official scores. Every saved
  benchmark has 320 unique valid case rows and acceptable recorded runtime;
  scores strictly increase from 228,305,971 to 252,894,799.
- At audit time, solvers/current.py was byte-identical to
  submissions/best_050_252894799.py, SHA256
  5dec351dbf778347262a72adbac2b44ae9d57243b96494cc69abddda88085a38.
  Static compilation/import/stdin checks pass. It is 98,653 bytes.
- Best050 stored stable evidence: total 252,894,799, average 790,296.246875,
  maximum 3.7366376 seconds. Stored readiness: 20/20 plus deterministic repeat,
  maximum 3.3017447 seconds. These are audited previous measurements, not newly
  rerun performance measurements.
- Best050 duplicated transition checks passed on N=3,4,9,16,30 and both D:
  1,800 comparisons across transition, seq_transition and State.apply;
  600 i1 packed-transition comparisons; thirty exhaustive gain and exact tied
  candidate-set comparisons for State.best_candidates. Each path was compared
  with tools.simulate, and action geometry was independently checked.

## Non-blocking findings

No scoring, rotation, stamp-state, frozen-suite or present-best readiness bug
was found.

- Source capacity is tight: best050 has 1,347 bytes remaining below the current
  100,000-byte limit. Check the source size of each new candidate before a full
  benchmark. Historical best039 is 107,628 bytes and is not submission-ready
  under the current source limit. Preserve it as historical evidence; use the
  verified current best for submission.
- tools/benchmark.py uses subprocess.run(capture_output=True), which buffers
  output without a limit before validation. A faulty output flood can consume
  excessive evaluator memory. tools/check_submission.py already has bounded
  draining; reusing that behavior would strengthen the benchmark harness.
- tools/checkpoint.py validates all stable benchmark rows, but trusts the
  readiness report's passed flag and source digest without independently
  validating its static result, case rows or determinism result. Checking those
  fields would prevent promotion from accidentally malformed readiness
  evidence. Existing best050 evidence itself passes these checks.
- Transition differential evidence is deliberately separate from the readiness
  JSON, whose transition_differential field says not_run. The command output
  and this note document the new independent checks; the earlier i1 checks are
  documented in notes/i1_review.md. This separation is explicit in the checker,
  not a claim that differential verification was absent.

Benchmark timing was left to the coordinating agent to avoid load contention.

## Suffix and segment-rotation review

Reviewed solvers/experiments/session_suffix.py against immutable best050 and
reviewed solvers/experiments/session_sequence_fragment.py independently.

- The suffix candidate retained the exact best050 source prefix. At review it
  was 99,710 bytes, SHA256
  5172751628c86c1b0cbcc7091bab3ecc43a5df1067d418395f2b4305e3849ff4.
  Static compilation, standard-library imports and stdin checks passed, with
  no filesystem I/O or benchmark-specific hardcoding found.
- Suffix replacement respects the operation budget: its retained prefix has
  length `cut`, and the new block depth is at most `K-cut`. The objective scores
  the target grid with wildcard stamp labels, and replacement occurs only on a
  strict score improvement. The inherited packed transition orientation is
  unchanged and correct.
- The segment-rotation identity was checked independently. Increasing every
  operation rotation in a segment by q is equivalent to rotating its input
  stamp by q, performing the original segment, then inversely rotating the
  output stamp. The fragment uses exactly those input and output index maps.
  Its sparse differences follow the same swap permutation as the baseline;
  backward target labels account for the unchanged suffix. An additional
  SequenceState.delta comparison checks the proposed full-result gain before
  acceptance. Coordinates and sequence length are preserved.
- A lightweight inline check exhaustively scored 648 segment candidates on six
  legal random N=4 instances spanning both D values. The fragment selected the
  exact maximum final grid score in all six. Six independent suffix calls with
  width=1, depth=3 and budget=300 respected K and the parent score floor through
  the canonical simulator. The complete command took 0.743 seconds of wall
  time. This is verification cost, not a solver performance benchmark.

No correctness issue was found. These observations do not establish a stable
benchmark improvement or qualify worst-case solver runtime. The coordinating
agent owns those runs and reported checkpoint051 saved after its full gates,
with stable score 252,909,754; this audit did not rerun that benchmark.

## Combined candidate static review

Reviewed solvers/experiments/session_combined.py and its readable companion
solvers/experiments/session_combined_source.py. The reviewed combined file is
99,738 bytes, leaving 262 bytes below the current source limit, with SHA256
a3b32accc115fa0dc91143b6bbaaeb25226651d8e8557c70bbcd6f3b1a7a5442.

Static compilation, stdin and standard-library checks pass with no review
flags. Independently reversing the four identifier-token renames and removing
docstrings produces an AST exactly equal to the source companion. The wrapper
calls the retained parent, then suffix reconstruction, then segment rotation in
the intended order. No source file was modified during review.

The new N=D shortcut is exact. With one full-grid placement, every odd-length
operation sequence leaves a rotation of the original stamp on the grid, which
can be produced in one operation. Every even-length sequence leaves a rotation
of the original grid, which can be produced in two operations, with the identity
also available in zero. Thus exact_two with min(K,2) covers every attainable
final grid for K>=2; for K=1 it compares the exact best single move against zero
moves. Its result is legal and globally optimal for this case.

This is correctness and static-source approval only. At the time this section
was recorded, the coordinating agent's combined stable benchmark was running;
combined score, full readiness and timing qualification remained pending.
