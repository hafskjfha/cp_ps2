# Optuna로 담금질 파라미터 계속 튜닝하기

이 문제는 **연산열 자체에 담금질법을 적용**할 수 있습니다. 연산을 교체·삽입·삭제하거나 두 연산의 순서를 바꾸고, 바뀐 지점부터 스탬프와 격자를 다시 계산합니다. 최종 일치 칸 수 차이 `delta`가 음수여도 `exp(delta / temperature)` 확률로 수용합니다. 최선의 연산열은 별도로 보관하므로 각 실행의 결과는 초기 탐욕해보다 나빠지지 않습니다.

이 폴더는 새로운 SA 실험입니다. 기존 최고 제출본을 초기해로 사용하는 구현은 아닙니다. 저장소 전체의 최고 기록은 여전히 상위 `results/best.json`이 기준입니다. 여기서 얻은 학습 점수를 기존 최고 점수와 직접 비교하지 마세요.

## 바로 실행 — 이 작업 환경

저장소 루트 `C:\dev\ps\doj\aislop2`에서 PowerShell로 실행합니다. 이 폴더의 `.venv`에 Optuna를 설치했습니다.

```powershell
# dev 100개, trial 횟수 제한 없이 계속 실행
& .\optuna_tuning\.venv\Scripts\python.exe .\optuna_tuning\tune.py --trials 0
```

**Ctrl+C로 중단하고 동일한 명령으로 재개**합니다. 완료한 trial은 SQLite에 즉시 보존됩니다. 강제로 종료한 실행의 미완료 trial은 재개 시 실패 처리하고 다음 번호부터 진행합니다. 한 출력 폴더에는 한 프로세스만 실행할 수 있습니다.

기본 설정은 dev 100개로 튜닝하고, 완료한 trial 10개마다 새로운 학습 최고 후보가 있으면 stable 320개 검증을 수행합니다. 유한 실행이 끝날 때도 미검증 최고 후보를 검증합니다. 처음 검증할 때는 탐욕 초기해를 먼저 평가하여 독립적인 `best_000_initial.py` 체크포인트를 만듭니다.

```powershell
# 짧은 동작 확인: smoke 20개, 3 trial, 자동 stable 검증은 생략
& .\optuna_tuning\.venv\Scripts\python.exe .\optuna_tuning\tune.py --suite smoke --trials 3 --validate-every 0 --output-dir optuna_tuning/runs/quick

# 위 실험을 10 trial 더 실행하고 마지막에 stable 검증
& .\optuna_tuning\.venv\Scripts\python.exe .\optuna_tuning\tune.py --suite smoke --trials 10 --validate-every 10 --output-dir optuna_tuning/runs/quick

# 후보에 대한 stable 검증만 실행
& .\optuna_tuning\.venv\Scripts\python.exe .\optuna_tuning\tune.py --suite smoke --validate-only --output-dir optuna_tuning/runs/quick

# 기본 dev 실험을 최대 약 8시간 실행
& .\optuna_tuning\.venv\Scripts\python.exe .\optuna_tuning\tune.py --hours 8

# 여러 고정 시드의 평균으로 별도 실험: 비용도 시드 수만큼 증가
& .\optuna_tuning\.venv\Scripts\python.exe .\optuna_tuning\tune.py --seeds 0,1,2 --output-dir optuna_tuning/runs/multiseed
```

`--trials`는 이번 실행에서 추가할 trial 수입니다. `0`은 무제한입니다. `--hours`는 새 trial을 시작할 기한이므로 진행 중인 trial 및 종료 시 검증 시간만큼 초과할 수 있습니다. Ctrl+C 중단 시에는 새로운 검증을 시작하지 않습니다. 이번 구현 작업에서는 유한한 검증 실행만 수행하며, 무기한 백그라운드 작업을 켜 두지 않습니다.

## 다른 Python 환경에 설치

Python 3.10 이상과 pip/venv가 필요합니다. 제출 프로그램에는 Optuna가 필요 없습니다.

아래 가상환경 생성 명령은 `.venv`가 없을 때 실행합니다. 이미 있는 가상환경을 다른 버전의 Python으로 덮어 만들면 이전 버전용 바이너리 패키지가 남을 수 있습니다.

```powershell
python -m venv optuna_tuning/.venv
& .\optuna_tuning\.venv\Scripts\python.exe -m pip install -r optuna_tuning/requirements.txt
```

Linux/macOS에서는 `.venv/Scripts/python.exe` 대신 `.venv/bin/python`을 사용합니다. 설치와 실행에 같은 가상환경의 Python 경로를 사용하세요. 테스트한 Optuna 버전은 5.0.0입니다.

### `Install dependencies`만 출력될 때

현재 튜너는 Optuna의 하위 의존성에서 발생한 ImportError에도 이 안내를 표시합니다. 실제 원인은 다음 명령으로 확인합니다.

```powershell
& .\optuna_tuning\.venv\Scripts\python.exe -c "import sys; print(sys.version); import numpy, optuna; print(numpy.__version__, optuna.__version__)"
```

Python 3.11 환경에 `cp312` NumPy 바이너리가 남아 있는 등 버전이 섞인 경우에는, 현재 Python에 맞는 패키지를 강제로 다시 설치합니다. 일반 설치만 하면 이미 설치되었다고 판단하여 잘못된 바이너리가 그대로 남을 수 있습니다.

```powershell
& .\optuna_tuning\.venv\Scripts\python.exe -m pip install --force-reinstall -r optuna_tuning/requirements.txt
```

Python 버전이 달라지면 이전 실험의 실행 환경과도 달라집니다. 이 경우 기존 기록은 보존하고 새 `--output-dir`을 사용하세요. 이전 환경에서 실행했던 결과는 그대로 남습니다.

## 탐색 대상과 점수

| 파라미터 | 기본 탐색 범위 | 의미 |
|---|---:|---|
| `iterations` | 500–8,000 | 담금질 이웃 탐색 횟수 |
| `start_temp` | 0.15–8.0, 로그 | 시작 온도, 일치 칸 수 단위 |
| `cooling_ratio` | 0.002–0.5, 로그 | 종료 온도 / 시작 온도 |
| `insert_weight`, `delete_weight`, `swap_weight` | 각 0.1–8.0, 로그 | 이웃 연산 선택 비율 |
| `local_probability` | 0–1 | 기존 좌표 근처를 선택할 확률 |
| `local_radius` | 1–5 | 근처 좌표 탐색 반경 |
| `tail_bias` | 0.5–5.0 | 연산열 뒤쪽을 수정하는 정도 |

교체 가중치 `replace_weight=4`는 고정합니다. 모든 가중치를 같은 배수로 바꾸는 중복 탐색을 피하기 위해서입니다. 초기 trial은 기본 파라미터이고, Optuna의 초기 무작위 탐색 뒤 TPE 탐색을 사용합니다. `--iterations-min`, `--iterations-max`로 비용을 제한할 수 있습니다. 전체 연산 수는 항상 입력의 `K` 이내입니다.

각 케이스에서 독립적인 제출 파일을 subprocess로 실행하고, 기존 `tools/validate_output.py` 및 `tools/simulate.py`로 검증한 뒤 다음 점수를 계산합니다.

```python
score = (1_000_000 * matches) // (N * N)
objective = 모든_케이스와_시드의_score_평균
```

평균 비율을 먼저 반올림하는 대신 **각 케이스의 공식 정수 점수를 먼저 계산**합니다. `--case-timeout` 기본값은 4.5초, 허용 최댓값은 공식 제한인 5초입니다. 하나라도 시간초과나 잘못된 출력이면 해당 trial 전체를 실패 처리하여 최적 파라미터로 채택하지 않습니다. 기본 median pruning은 같은 순서의 케이스별 누적 평균을 비교합니다. `--no-prune`으로 비활성화할 수 있습니다.

여러 시드를 지정하면 평균으로 파라미터를 선택하지만, 내보내는 단일 제출 파일에는 **첫 번째 시드**를 고정합니다. 따라서 stable 검증은 실제 내보낸 그 파일로 별도로 수행합니다.

## 저장되는 파일과 제출본 선택

기본 결과 폴더는 `optuna_tuning/runs/default/`입니다.

| 경로 | 용도 |
|---|---|
| `study.db` | Optuna trial 상태, 점수, 파라미터의 원본 기록 |
| `configuration.json` | 코드·케이스·시드·환경·탐색 범위 지문 |
| `trials/trial_*.json` | 케이스별 점수·시간·출력 해시, 실패 및 가지치기 기록 |
| `trials.csv` | trial 요약; 강제 종료 직전 행은 DB에만 남을 수 있음 |
| `best_params.json` | 학습 최고 파라미터와 검증 상태 |
| `best_candidate.py` | 학습 최고 파라미터를 넣은 독립 실행 후보 |
| `last_validation.json` | 마지막 후보의 stable 검증 결과 |
| `verified/best.json` | **이 실험에서 검증된 최고 제출본의 경로** |
| `verified/history.csv` | stable 점수가 엄격하게 상승한 체크포인트 이력 |
| `verified/checkpoints/best_*.py` | 보존되는 단일 Python 제출 파일 |
| `verified/qualifications/` | stable, readiness, 전체 재현 평가 근거 |

`best_candidate.py`는 학습 최고 후보이며, 자동 검증을 끄면 검증되지 않은 상태입니다. 제출본은 `verified/best.json`의 `checkpoint` 경로에서 고르세요. full stable 점수의 엄격한 상승, 정적 제출 검사, 최소/최대 및 랜덤 입력 검사, 전체 stable 출력의 재현 확인을 모두 통과해야 새 체크포인트를 만듭니다. 기존 파일은 덮어쓰지 않습니다. 동점이나 퇴보 시 기존 검증 최선이 유지됩니다.

학습에 사용하지 않은 stable 나머지 케이스도 검증에 포함됩니다. 다만 smoke/dev는 stable의 부분집합이고, stable도 반복 관측되므로 완전히 독립적인 최종 holdout은 아닙니다. 충분히 튜닝한 뒤 새 고정 시드의 추가 사례에서도 확인하세요. 케이스 패밀리별 점수와 실행 시간은 `stable.json`의 `breakdown`에 들어 있습니다.

코드, 케이스, 시드, 실행 Python/Optuna 버전, 탐색 범위, timeout, pruning을 바꾸면 **새 `--output-dir`**를 사용합니다. trial 수, 실행 시간, 검증 주기는 재개하면서 바꿀 수 있습니다. 실행 중에는 시작할 때 읽은 solver 소스를 고정하고, trial 번호에서 정한 TPE 시드를 사용하여 정상 중단·재개의 파라미터 순서도 재현합니다. 강제 종료로 실패한 trial은 번호가 소비됩니다. 일시적인 검증 실패는 재시도할 수 있고, 성공한 검증도 `--revalidate`로 다시 실행할 수 있습니다.

실험 폴더 내부 `verified/` 기록과 기존 저장소 전체의 `submissions/` 기록은 별도입니다. 이 도구가 전역 최고를 자동으로 바꾸지는 않습니다. 전역 승격에는 기존 `tools/checkpoint.py` 절차를 사용하세요.

## 테스트와 근거

```powershell
& .\optuna_tuning\.venv\Scripts\python.exe -m unittest optuna_tuning.test_sa_solver optuna_tuning.test_evaluation optuna_tuning.test_tune -v
```

회전 D=2/3, 랜덤 연산열 및 600개 변이의 차등 검사, 출력 유효성·타임아웃, 제출 파일 독립 실행, SQLite 재개, 중단된 trial 복구, 재개 전후 파라미터 순서, 프로세스 종료 후 잠금 복구를 검사합니다. 측정 요약은 `results/verification.md`, 최초 SA 비교의 상세 기록은 `results/sa_feasibility.json`에 저장합니다.

Optuna API는 공식 [Study 문서](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html)와 [SQLite 저장·재개 문서](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/001_rdb.html)를 참고했습니다. SQLite는 한 번에 하나의 튜닝 프로세스로 사용합니다.
