# Exact short-horizon meet-in-the-middle probe

Reference: immutable best_050_252894799.py. Existing short beam, exact two moves, perfect-target wildcard N4/D3 finishing, and packed suffix beam are already covered.

Hypothesis: enumerate all forward half-path states and all backward half-path target wishes, then maximize exact score using bit-sliced indexes. This can prove the best K=3 answer on modest grids and K=4 on small grids, without pruning away temporarily bad actions. Preserve the complete parent unless the exact answer improves. Deterministic state deduplication permits shorter paths. Canonical simulator differential checks and <=20 frozen diagnostic cases gate any recommendation; root owns full stable qualification.

## Results

Exact MITM was canonically verified against exhaustive enumeration on 16 tiny random cases. All nine eligible frozen benchmark cases tie the parent: 032,080,112,144,160,176,192,240,288. Component maximum runtime 0.216 seconds under shared load. These establish that the reference is already exact optimal on the selected short horizons; no full stable run is warranted. Results are in results/session_small_component.json. The experimental integrated session_small.py is 100181 bytes and is **not submission ready**; it is retained solely as a rejected probe. The helper is session_small_fragment.py.

A separate cheap exact shortcut handles N=D: after any number of operations, the board is a rotation of its original contents or of the original stamp. Every former image is achievable in at most two operations; every latter in one. Therefore existing exact_two with min(K,2) solves this domain globally, without running the portfolio or repair pipeline. Forty random same-size cases compared against exhaustive packed orbits through depth five and canonical output simulation, all passed. Self-contained candidate session_small_fast.py preserves the entire parent and adds this shortcut; root may adopt as a runtime-only equal-score change after measurement. No score improvement is claimed.

Diagnostics stopped at root request for isolated stable qualification.
