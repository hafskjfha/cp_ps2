# Stamp optimization implementation plan

Goal: produce the highest measured score attainable in this work session, with a reliable local evaluator and immutable, self-contained Python submission checkpoints.

Spec: `problem.md`, `AGENTS.md`, and `codex_prompt.md`.

The user's explicit autonomous experimentation workflow governs execution. This directory is not a Git repository; work stays directly in the requested workspace. No deployment or external changes are needed.

- [x] Build and independently test canonical rotations/simulator, strict output validator, and official scorer.
- [x] Generate and freeze 20 smoke, 100 development, and 320 stable cases with varied families and fixed seeds. Use the full 320-case stable set for checkpoint decisions if runtime permits.
- [x] Build subprocess benchmark runner with validation, timeout, provenance, breakdowns, and JSON results.
- [x] Compare zero, best single operation, and repeated positive greedy; verify and save best_000_initial.py.
- [x] Investigate measured improvements from neutral/negative setup moves, stamp awareness, lookahead and sequence refinement. Record each hypothesis before experiments, measure smoke then stable, and immediately save each strict best.
- [x] Independently review the final submission and tools, reproduce best score, test random/min/max inputs, and report exact submission path.

Interfaces: tools.simulate.Instance(n,d,c,k,a,t,s), flattened arrays; parse_instance(text); simulate(instance,ops)->(grid,stamp); match_count(instance,grid). tools.validate_output.validate_output(instance,bytes)->ops. Manifest at cases/manifest.json, case paths relative to repository root.

Review focus: rotated pickup orientation; mismatches near grid edges; all-uniform or unreachable color demands; K=1 and N=D; output token/byte limits and timeout handling.

Runtime policy: user confirmed the official time limit is 5,000 ms. Enforce a 5-second per-instance local timeout, target below 4 seconds with margin at maximum constraints, and report separate single-process worst-case measurements.
