Hypothesis: Small boards benefit from beam search over states modulo stamp rotation. Stamp rotations are equivalent because every next operation may freely rotate the stamp. Canonicalizing each picked-up patch before storing child states removes rotational duplicates, while an accumulated orientation phase recovers exact legal operation rotations. A fixed random quarter of cells receives slight extra weight in beam ranking; raw matches still govern answer retention.

Failed: bidirectional beam with conserved final-stamp candidates yielded no gains over parent052 on selected small cases. Larger plain beam alone gave wins but weaker results than canonical stamp beam.

Final merge stage: solvers/experiments/million_small_stage.py, 4527 bytes, expects existing build, _st, and color_bound globals; helper small_beam_stage(n,d,c,k,grid,target,stamp,reference). Guard 4<=N<=12 and4<=K<=16, early stop at conserved-color upper bound. Beam width512, increased to2048 for D3,N<=6; 1,000,000-transition cap. Deterministic seed941 and weighted tie guidance. No benchmark IDs in code.

Full frozen320 diagnostic after root longbeam24 cached outputs: all validated and canonically simulated; stage retained +135749 score (085:+15625,145:+12346,148:+80000,308:+27778), no regressions. Added total10.6893s; maximum2.1401s on308, whose parent052 runtime1.57s. Other added maxima1.28s on241,1.22s on016,1.19s on289. Evidence results/million_small_final_stable.json. Combined with longbeam24 gain894028 gives +1029777 before runtime adaptation of the root stage.

Rotation and canonical state correctness: 3000 randomly sampled transitions across100 random instances, N3..9,D2/3,C2..6, compared after every step to canonical simulator. All passed.

Width512-only alternative gives +107971, dropping308 reserve; available by setting width=512. Final official promotion belongs to root whole-solver stable benchmark.
