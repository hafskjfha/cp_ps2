# 검증 결과 (2026-09-30)

실제 Optuna 5.0.0 환경에서 12 trial을 실행한 뒤 같은 SQLite 실험을 재개하여 1 trial을 추가했습니다. 총 13회 중 12회 완료, 1회 가지치기, 실패 0회입니다. 기존 고정 smoke20/dev100/stable320 케이스를 변경하지 않았습니다.

## 점수와 체크포인트

| 방법 | stable320 총점 | 직전 대비 | 평균 점수 | 1차 stable 최대 시간 |
|---|---:|---:|---:|---:|
| Initial greedy baseline (SA iterations=0) | 228,305,971 | - | 713456.16 | 0.411s |
| Default simulated annealing (3000 iterations) | 236,948,550 | +8,642,579 | 740464.22 | 0.461s |
| Optuna trial 5 | 240,667,550 | +3,719,000 | 752086.09 | 0.549s |

기본 담금질은 탐욕해 대비 78개 개선/0개 악화였습니다. 튜닝 후보는 기본 담금질 대비 110개 개선/6개 악화/204개 동점으로 총점이 상승했습니다. 튜닝에 사용한 smoke 점수는 기본 담금질 16,492,950에서 16,894,302로 상승했습니다.

모든 체크포인트는 stable320 출력 유효성, 38개 readiness 입력(최소·최대 포함), 추가 결정성 검사, 전체 stable320 재실행의 출력 해시·점수 일치를 통과했습니다. 세 단계가 각각 별도 파일로 보존됩니다.

- `best_000_initial.py`: source 9,236 bytes; 관측 최대 0.411s.
- `best_001_236948550.py`: source 9,239 bytes; 관측 최대 0.546s.
- `best_002_240667550.py`: source 9,339 bytes; 관측 최대 0.683s.

이 SA 실험의 최선: `optuna_tuning/runs/smoke_demo/verified/checkpoints/best_002_240667550.py`.
저장소 전체 최선은 여전히 `submissions/best_056_255006286.py` (255,006,286점)입니다. 이번 SA 후보는 이 기존 최선을 넘지 못했습니다. 상위 submissions/history/current와 benchmark 입력은 교체하지 않았습니다.

## 재현 명령

```powershell
& .\optuna_tuning\.venv\Scripts\python.exe optuna_tuning/tune.py --suite smoke --trials 12 --validate-every 0 --output-dir optuna_tuning/runs/smoke_demo
& .\optuna_tuning\.venv\Scripts\python.exe optuna_tuning/tune.py --suite smoke --trials 1 --validate-every 0 --output-dir optuna_tuning/runs/smoke_demo
& .\optuna_tuning\.venv\Scripts\python.exe optuna_tuning/tune.py --suite smoke --validate-only --output-dir optuna_tuning/runs/smoke_demo
```

위 실행 이력은 이미 저장되어 있습니다. 같은 trial을 처음부터 재현하려면 새 output-dir을 사용하세요. 기존 실험을 계속 튜닝하려면 `--trials 0`을 사용합니다. 기본 담금질도 비교하기 위해 iterations=0, 기본 params를 각각 export_source/qualify로 순서대로 검증한 뒤 튜닝 후보를 검증했습니다. 각 immutable 검증 근거는 `../runs/smoke_demo/verified/qualifications/`에 있습니다.

## 테스트 및 리뷰

- 신규 테스트 30개 모두 통과: 회전, 600회 변이 차등, 최소/최대, 결정성, 유효성/타임아웃, 독립 제출 파일, 재개, 강제 종료 복구, 파라미터 순서, 검증 재시도, 소스 고정.
- 전체 `python -m unittest discover -v`: 297개 중 294개 통과, 3개 기존 스크립트 검색 오류. 소요 273.285초. 상세: `project-tests.log`.
- `tools.test_regret_cached27`: import 시 `discover`를 solver 이름으로 사용하여 존재하지 않는 discover.py를 찾음.
- `tools.test_regret_rebuild`: import 시 unittest 인자를 solver 경로로 처리하여 import spec이 None이 됨.
- `tools.test_regret_variants`: import 시 자체 argparse가 `discover -v`를 거부함.
- 위 세 파일은 이번에 수정하지 않은 기존 CLI 실험 스크립트입니다. 전체 테스트가 전부 성공했다고 보고하지 않습니다.
- 독립 코드 리뷰에서 실행 중 solver 소스 고정, 검증 기록 복구, 실패한 검증 재시도, 강제 종료 후 잠금 해제를 확인했습니다.

무기한 백그라운드 탐색은 켜 두지 않았습니다. 제출 파일은 Optuna나 로컬 helper를 가져오지 않으며, 저장된 결과 파일을 읽지 않습니다.
