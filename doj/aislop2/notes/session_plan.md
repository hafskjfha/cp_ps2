# Continued measured optimization, 2026-09-26

Goal: improve the existing verified Python solver on the unchanged 320-case suite while preserving every checkpoint and satisfying 5 seconds and 100,000 source bytes.

Specification: AGENTS.md, problem.md, and the user's pasted autonomous experimentation request. Existing infrastructure and checkpoints 000-050 already cover the mandatory first stages and breadth exploration. Continue from verified best050; do not recreate or replace those artifacts.

- [x] Audit canonical rotations, validation, benchmark identity, and current checkpoint evidence using existing tools and inline checks. No new dedicated test files.
- [x] Root: measure retained-parent suffix beam alternatives with deterministic transition budgets. Hypothesis: additional shorter/wider suffix reconstruction can find improvements missed by the current beam without unacceptable runtime.
- [x] Parallel small-grid probe: investigate a distinct exact or beam enhancement after reviewing previous experiments.
- [x] Parallel sequence probe: investigate a distinct sequence optimization, documenting failures as well as wins.
- [x] Run smoke, unchanged full stable320, readiness/random checks, and isolated maximum-size timing for promising candidates. Never use diagnostic subsets to promote a checkpoint.
- [x] Reproduce improved scores, independently review changed logic, save strict improvements immediately through tools/checkpoint.py, and update current.py, history, experiment notes and README.

The user's explicit autonomous workflow governs execution; skill approval gates and dedicated test-file suggestions do not override it. This directory has no Git repository, so isolated experiment files provide separation. Runtime qualification must run without other solver benchmarks competing for CPU. Partial diagnostic timings are provisional.
