# Million-point improvement campaign

Selected submission: [`runtime_053_254103898.py`](../submissions/runtime_053_254103898.py). This file is self-contained, 99,261 bytes, standard-library Python, and identical to `solvers/current.py`.

| Measurement | Score |
|---|---:|
| Initial greedy checkpoint 000 | 228,305,971 |
| Starting best checkpoint 052 | 252,937,025 |
| Requested threshold | 253,937,025 |
| Final selected solver | **254,103,898** |
| Gain in this campaign | **1,166,873** |
| Margin above requested gain | 166,873 |

The benchmark remains the frozen 320 suite, seed 20260925:20 smoke, 100 development, 320 stable, with random,near-target,reachable,checkerboard,stripes,repeated-stamp,nearly-uniform and local-adversarial families. Scores use the canonical simulator and `(1000000*matches)//(N*N)` for every input. Final average:794,074.68125. **81 cases improved,239 tied, 0 regressed.** These are local320-case results; the unseen official 40-case result has not been measured.

## Successful changes

- Full-budget beam search keeps 24 alternative states through long move sequences, using bit-parallel action gains and a one-step continuation estimate. It then applies exact backward and pair refinement. The largest D=3 instances use width 16 to control runtime.
- Small-board beam search identifies stamp states equivalent under rotation, tracks the orientation needed to recover legal moves, and spends its search budget on more distinct states.
- Prefix reconstruction replaces a weak suffix with short color-routing sequences, retaining the candidate only when the true final score improves.
- Eight objective-perturbation trials use random 1/2 cell weights to find different refinement paths, then restore the real match-count objective and retain its best result.
- Size,move-budget,and remaining-score guards avoid spending extra search on near-complete boards. Longer small-board searches use a 600000-transition cap; shorter ones retain 1000000.

## Measured exploration

| Direction | Evidence | Conclusion |
|---|---|---|
| Long beam,width 24 | +894,028 after 052 on cached stable 320 | Main scoring advance |
| Canonical-stamp small beam | +135,749 after long beam 24 | Complementary improvement |
| Prefix color routing | +104,785 after long beam 24 | Complementary improvement |
| Objective perturbation | +52,045 after long beam 24 | Useful with runtime guards |
| 24 perturb/refine restarts | 0 gain on development 100 | Rejected |
| Broad global sequence mutation | Only+1,480 on development 100 after 50k proposals | Rejected for cost |
| Distant conjugate routing | Similar score to cheaper prefix routing; up to 4.12s added | Rejected |
| Uniform width48 long beam | More dev points,up to 2.45s added | Rejected for runtime |

The independent diagnostic deltas above overlap and are not additive. Only the fresh standalone final benchmark determines the selected score. Diagnostic implementation and full measurements are in `notes/million_small.md`, `notes/million_macro.md`, `notes/million_anneal.md`, and `results/million_*.json`.

## Runtime qualification

| Check on selected bytes | Result | Maximum seconds |
|---|---:|---:|
| Smoke |20/20 valid|4.791|
| Frozen stable |320/320 valid|4.341|
| Random/boundary readiness |38/38 plus deterministic repeat|4.057|
| N=30, K=180 holdout |36/36 valid|4.820|
| Search-parameter boundary holdout |18/18 valid|4.290|

Aggregate stable runtime:424.724s, average1.327s. Worst final observed time:4.820s against the 5s limit. Runtime measurements use isolated sequential subprocesses.

The first score checkpoint 053 passed stable/readiness/max-size but later failed an added N=23, D=3, K=180 boundary at 5.029s. A first runtime revision also timed out on three already-near-complete boards. Both failures are preserved in the results. The selected runtime variant removes unnecessary extra searches and passes all expanded checks; use it instead of the original053 source.

All 320 per-case scores were reproduced in the final run.319 operation outputs also remain byte-identical to the first successful score run; the other is a different equal-score sequence. Transition reviews covered 6075 long-beam choices across 1200 states and 3000 canonical-stamp transitions,plus randomized routing/refinement checks. The byte-level source audit verifies standard-library imports,stdin/stdout use,source size,and reversible AST-equivalent identifier compaction. Windows line endings are normalized in the exact submitted bytes.

SHA256:`dd865b4ea01fe859fe7c820a9a1b5201b7213cd3da29ba186cea4bc9ebf318ac`

## Checkpoints

This campaign adds strict score checkpoint 053 and selects its separately preserved runtime variant. All previous checkpoints remain immutable. `results/history.csv` records strict improvements; `results/runtime_variants.json` records runtime-only selections; `results/best.json` identifies the submission to use.

| ID | Stable score | Immutable source |
|---:|---:|---|
|000|228,305,971|[best_000_initial.py](../submissions/best_000_initial.py)|
|001|240,756,242|[best_001_240756242.py](../submissions/best_001_240756242.py)|
|002|240,849,239|[best_002_240849239.py](../submissions/best_002_240849239.py)|
|003|242,249,708|[best_003_242249708.py](../submissions/best_003_242249708.py)|
|004|243,391,996|[best_004_243391996.py](../submissions/best_004_243391996.py)|
|005|244,316,245|[best_005_244316245.py](../submissions/best_005_244316245.py)|
|006|245,343,012|[best_006_245343012.py](../submissions/best_006_245343012.py)|
|007|245,544,191|[best_007_245544191.py](../submissions/best_007_245544191.py)|
|008|246,335,486|[best_008_246335486.py](../submissions/best_008_246335486.py)|
|009|246,786,935|[best_009_246786935.py](../submissions/best_009_246786935.py)|
|010|246,874,186|[best_010_246874186.py](../submissions/best_010_246874186.py)|
|011|247,272,076|[best_011_247272076.py](../submissions/best_011_247272076.py)|
|012|248,036,769|[best_012_248036769.py](../submissions/best_012_248036769.py)|
|013|248,753,972|[best_013_248753972.py](../submissions/best_013_248753972.py)|
|014|249,115,734|[best_014_249115734.py](../submissions/best_014_249115734.py)|
|015|249,389,357|[best_015_249389357.py](../submissions/best_015_249389357.py)|
|016|249,547,073|[best_016_249547073.py](../submissions/best_016_249547073.py)|
|017|249,880,999|[best_017_249880999.py](../submissions/best_017_249880999.py)|
|018|250,064,691|[best_018_250064691.py](../submissions/best_018_250064691.py)|
|019|250,384,135|[best_019_250384135.py](../submissions/best_019_250384135.py)|
|020|250,559,222|[best_020_250559222.py](../submissions/best_020_250559222.py)|
|021|250,867,386|[best_021_250867386.py](../submissions/best_021_250867386.py)|
|022|250,872,488|[best_022_250872488.py](../submissions/best_022_250872488.py)|
|023|250,921,331|[best_023_250921331.py](../submissions/best_023_250921331.py)|
|024|250,934,988|[best_024_250934988.py](../submissions/best_024_250934988.py)|
|025|250,983,831|[best_025_250983831.py](../submissions/best_025_250983831.py)|
|026|251,149,505|[best_026_251149505.py](../submissions/best_026_251149505.py)|
|027|251,280,679|[best_027_251280679.py](../submissions/best_027_251280679.py)|
|028|251,305,191|[best_028_251305191.py](../submissions/best_028_251305191.py)|
|029|251,345,195|[best_029_251345195.py](../submissions/best_029_251345195.py)|
|030|251,481,350|[best_030_251481350.py](../submissions/best_030_251481350.py)|
|031|251,606,350|[best_031_251606350.py](../submissions/best_031_251606350.py)|
|032|251,668,850|[best_032_251668850.py](../submissions/best_032_251668850.py)|
|033|251,678,439|[best_033_251678439.py](../submissions/best_033_251678439.py)|
|034|251,734,381|[best_034_251734381.py](../submissions/best_034_251734381.py)|
|035|251,765,631|[best_035_251765631.py](../submissions/best_035_251765631.py)|
|036|251,771,548|[best_036_251771548.py](../submissions/best_036_251771548.py)|
|037|251,801,728|[best_037_251801728.py](../submissions/best_037_251801728.py)|
|038|251,809,034|[best_038_251809034.py](../submissions/best_038_251809034.py)|
|039|251,862,073|[best_039_251862073.py](../submissions/best_039_251862073.py)|
|040|251,963,428|[best_040_251963428.py](../submissions/best_040_251963428.py)|
|041|252,038,607|[best_041_252038607.py](../submissions/best_041_252038607.py)|
|042|252,085,720|[best_042_252085720.py](../submissions/best_042_252085720.py)|
|043|252,147,480|[best_043_252147480.py](../submissions/best_043_252147480.py)|
|044|252,152,063|[best_044_252152063.py](../submissions/best_044_252152063.py)|
|045|252,192,457|[best_045_252192457.py](../submissions/best_045_252192457.py)|
|046|252,388,472|[best_046_252388472.py](../submissions/best_046_252388472.py)|
|047|252,571,424|[best_047_252571424.py](../submissions/best_047_252571424.py)|
|048|252,747,393|[best_048_252747393.py](../submissions/best_048_252747393.py)|
|049|252,862,932|[best_049_252862932.py](../submissions/best_049_252862932.py)|
|050|252,894,799|[best_050_252894799.py](../submissions/best_050_252894799.py)|
|051|252,909,754|[best_051_252909754.py](../submissions/best_051_252909754.py)|
|052|252,937,025|[best_052_252937025.py](../submissions/best_052_252937025.py)|
|053|254,103,898|[best_053_254103898.py](../submissions/best_053_254103898.py)|

**Selected runtime variant:** [runtime_053_254103898.py](../submissions/runtime_053_254103898.py). Original053 is retained as a historical scoring checkpoint and is superseded for runtime safety.
