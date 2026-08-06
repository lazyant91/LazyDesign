# LazyDesign 평가 산출물 무결성 Handover

작성 시각: 2026-08-06 19:56 KST

## 1. 저장소 상태

- GitHub 저장소: `lazyant91/LazyDesign`
- 로컬 작업공간: `Z:\workspace\LazyDesign`
- 작업 브랜치: `docs/initial-reference-design`
- 이 문서 작성 직전 HEAD: `77c3f40d03b4d6101020789acfbcecf0c22c4b97`
- upstream: `origin/docs/initial-reference-design`
- 기본 브랜치: `origin/main`
- 시작 프로젝트 snapshot commit: `b73babad19d0153707a49e5ba1ed9fb0a42c33ef`
- prompt/reference input commit: `7d01aae3cdc0241a7aa7ede7ee09738a6d5ee7cc`
- Draft PR: `#1`
- PR base/head: `main <- docs/initial-reference-design`

다음 세션은 위 HEAD를 가정하지 말고 remote, `origin/HEAD`, branch, upstream, HEAD, status, worktree를 실제로 다시 확인한다. 기존 변경과 추적되지 않은 파일이 있으면 보존하고 switch, stash, restore, reset, clean을 자동 수행하지 않는다.

## 2. 이번 세션의 변경

### 77c3f40 — evaluation artifact integrity

변경 파일:

- `scripts/evaluation_harness.py`
- `scripts/evaluation_report.py`
- `tests/test_evaluation_harness.py`
- `tests/test_evaluation_report.py`
- `tests/test_evaluation_gate.py`
- `evaluation/README.md`
- `evaluation/rubric.md`
- `docs/superpowers/plans/2026-08-06-winui3-component-reference-v0.1.md`

### Capture 무결성

`CAPTURE.json`은 이제 다음 SHA-256과 파일 집합을 기록한다.

- `PROMPT.md`
- `PACKET.json`
- `RUN.md`
- `generated/` 전체 파일 목록과 해시
- `evidence/` 전체 파일 목록과 해시
- 삭제된 시작 프로젝트 파일 목록

`validate-results`는 캡처 후 다음 변경을 거부한다.

- `RUN.md` 수정
- `PACKET.json` 수정 또는 임의 필드 추가
- `generated/` 파일 수정, 추가, 제거
- `evidence/` 파일 수정, 추가, 제거
- 고정 prompt/reference/start fixture 변경

### Metrics evidence 무결성

`evaluation_report.py`는 보고서를 쓰기 전에 다음을 수행한다.

1. baseline/guided 6개 결과에 대해 `validate-results` 재실행
2. 모든 score evidence 파일 존재 확인
3. score evidence가 자신의 condition/scenario 경로 안에 있는지 확인
4. traceable improvement가 해당 guided scenario를 가리키는지 확인
5. finding evidence가 baseline 또는 guided 결과 파일을 가리키는지 확인
6. `:<start>-<end>` line range가 실제 UTF-8 파일 범위 안에 있는지 확인
7. 검증 실패 시 `scores.md`, `findings.md`, `gate-decision.md`를 생성하지 않음

Evidence 경로는 `evaluation/` 기준 상대 경로다.

예시:

```text
baseline/connection-settings/generated/MainWindow.xaml:12-40
guided/device-list/evidence/dark-theme-observation.txt
guided/failure-confirmation/RUN.md:18-22
```

## 3. 현재 검증 증거

현재 branch에서 실행:

```powershell
python scripts/check_reference.py
python scripts/evaluation_harness.py validate
python -m unittest discover -s tests -p 'test_*.py' -v
python -m py_compile scripts/check_reference.py scripts/evaluation_harness.py scripts/evaluation_evidence.py scripts/evaluation_gate.py scripts/evaluation_report.py tests/test_evaluation_harness.py tests/test_evaluation_evidence.py tests/test_evaluation_gate.py tests/test_evaluation_report.py
python -m json.tool evaluation/run-matrix.json
python -m json.tool evaluation/verification.schema.json
python -m json.tool evaluation/gate-metrics.schema.json
dotnet build evaluation/fixtures/winui-start/LazyDesign.EvaluationApp.csproj -c Debug -p:Platform=x64
git diff --check
```

결과:

- reference structural check: pass
- evaluation run matrix: pass
- Python tests: **36 passed**
- Python compile: pass
- JSON parse: pass
- WinUI fixture build: warning 0, error 0
- whitespace check: pass
- unresolved `TBD|TODO`: none

검증 중 생성한 `bin`, `obj`, `__pycache__`는 제거했다.

## 4. 아직 수행되지 않은 작업

실제 평가 작업은 여전히 수행되지 않았다.

- baseline 3회
- guided 3회
- 생성물 build
- 실제 scenario render
- 420 DIP와 520 DIP rendered observation
- Light, Dark, High Contrast
- text scaling
- 한국어·영어 장문
- keyboard와 focus
- ComboBox popup
- CommandBar overflow
- ListView selection
- InfoBar retry/dismissal
- ContentDialog default/close action과 focus return
- Narrator
- Accessibility Insights
- 실제 rubric 점수
- 실제 findings
- 실제 gate 판정

실행하지 않은 이유:

- 현재 대화가 이미 LazyDesign reference를 읽어 baseline fresh context로 사용할 수 없음
- 로컬 Codex CLI 사용 금지
- subagent와 병렬 agent 사용 금지
- OpenAI/Azure OpenAI API key 없음
- 같은 model identifier와 reasoning level의 독립 fresh context 6개를 생성할 실행기가 없음

현재 세션에서 코드를 대신 생성하거나 synthetic 결과를 실제 baseline/guided로 저장하면 실험 조건 위반이다.

## 5. 다음 실제 실행 절차

각 실행 직전에 존재하지 않는 새 destination으로 packet을 만든다.

```powershell
python scripts/evaluation_harness.py prepare --condition baseline --scenario connection-settings --destination evaluation/.runs/baseline/connection-settings
python scripts/evaluation_harness.py prepare --condition baseline --scenario device-list --destination evaluation/.runs/baseline/device-list
python scripts/evaluation_harness.py prepare --condition baseline --scenario failure-confirmation --destination evaluation/.runs/baseline/failure-confirmation
python scripts/evaluation_harness.py prepare --condition guided --scenario connection-settings --destination evaluation/.runs/guided/connection-settings
python scripts/evaluation_harness.py prepare --condition guided --scenario device-list --destination evaluation/.runs/guided/device-list
python scripts/evaluation_harness.py prepare --condition guided --scenario failure-confirmation --destination evaluation/.runs/guided/failure-confirmation
```

각 run에서:

1. 같은 model identifier와 reasoning level 사용
2. 별도 fresh context 사용
3. prompt 보완, 중간 조언, repair 금지
4. `RUN.template.md`를 `RUN.md`로 복사하고 모든 필드 작성
5. `verification.template.json`을 `verification.json`으로 복사하고 모든 check 작성
6. 실제 evidence 파일을 `evidence/`에 저장
7. capture 실행

Capture 예시:

```powershell
python scripts/evaluation_harness.py capture --packet evaluation/.runs/baseline/connection-settings --destination evaluation/baseline/connection-settings
```

6개 capture 후:

```powershell
python scripts/evaluation_harness.py validate-results --root evaluation
```

이 명령이 pass하기 전에는 scoring을 시작하지 않는다.

## 6. Scoring과 보고서 생성

구조화 입력:

```text
evaluation/results/metrics.json
```

계약:

```text
evaluation/gate-metrics.schema.json
```

보고서 생성:

```powershell
python scripts/evaluation_report.py evaluation/results/metrics.json --output-dir evaluation/results
```

이 명령은 먼저 6개 결과와 모든 evidence path를 검증한 뒤 다음을 함께 생성한다.

- `scores.md`
- `findings.md`
- `gate-decision.md`

Exit code:

- `0`: PASS
- `2`: valid FAIL
- `1`: 결과 또는 metrics 불완전/무효

PASS인 경우에만 `DESIGN.md`를 `validated-v0.1`로 변경하고 precision expansion을 승인한다. FAIL이면 `v0.1-candidate`를 유지하고 수정 대상 reference page 또는 retrieval behavior를 기록한다.

## 7. 다음 세션 시작 순서

1. `C:\Users\lky57\.wgpt\AGENTS.md`를 실제 파일에서 읽는다.
2. 저장소 및 하위 `AGENTS.md`를 읽는다.
3. remote, `origin/HEAD`, branch, upstream, HEAD, status, worktree를 확인한다.
4. 이 handover와 이전 evidence/reporting handover를 읽는다.
5. 현재 SHA에서 static, tests, JSON, build를 다시 실행한다.
6. 동일 model/reasoning fresh-context 실행기가 확보된 경우에만 6개 run을 시작한다.
7. 모든 run을 repair 없이 capture한다.
8. `validate-results`를 통과시킨다.
9. 실제 `metrics.json`을 작성한다.
10. `evaluation_report.py`로 세 보고서를 생성한다.
11. gate 결과에 따라 README와 DESIGN 상태를 갱신한다.
12. PR은 Draft로 유지하고 사용자 승인 없이 Ready 전환 또는 merge하지 않는다.

## 8. 환경과 범위 제한

- Windows Design Kit component-level inspection 미완료
- `ui-kit` evidence 비활성
- gate 전 신규 component 범위 추가 금지
- GitHub Actions 추가 금지
- resolver, adapter, custom control library, static analyzer 추가 금지
- 현재 reference 문서를 UI-kit evidence로 승격하지 않음

이 Remote 환경은 `C:\Users\lky57\.wgpt\AGENTS.md`가 allowlist 밖이라 직접 읽기를 차단했다. 우회하거나 allowlist를 변경하지 않았다.

Narrator 실행 파일은 이전 세션에서 발견됐지만 실제 Narrator 검증은 수행하지 않았다. Accessibility Insights는 일반 설치 경로에서 발견되지 않았다. 실제 run에서는 해당 항목을 `not_run`과 구체적인 사유로 기록한다.
