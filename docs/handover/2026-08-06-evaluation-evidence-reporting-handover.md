# LazyDesign 평가 증거 및 보고서 자동화 Handover

작성 시각: 2026-08-06 19:12 KST

## 1. 저장소 상태

- GitHub 저장소: `lazyant91/LazyDesign`
- 로컬 작업공간: `Z:\workspace\LazyDesign`
- 작업 브랜치: `docs/initial-reference-design`
- 이 문서 작성 직전 HEAD: `95763ca910753192b20a27a17928599938919686`
- 시작 프로젝트 snapshot commit: `b73babad19d0153707a49e5ba1ed9fb0a42c33ef`
- prompt/reference input commit: `7d01aae3cdc0241a7aa7ede7ee09738a6d5ee7cc`
- Draft PR: `#1`
- PR base/head: `main <- docs/initial-reference-design`

다음 세션은 위 HEAD를 가정하지 말고 remote, `origin/HEAD`, branch, upstream, HEAD, status, worktree를 실제로 다시 확인한다. 기존 변경과 추적되지 않은 파일이 있으면 보존하고 switch, stash, restore, reset, clean을 자동 수행하지 않는다.

## 2. 이번 세션의 커밋

### d30ddd2 — structured evaluation evidence

추가 또는 변경:

- `evaluation/verification.schema.json`
- `scripts/evaluation_evidence.py`
- `scripts/evaluation_harness.py`
- `evaluation/gate-metrics.schema.json`
- `scripts/evaluation_gate.py`
- 관련 README, rubric, 테스트

기능:

- 각 run packet에 `evidence/verification.template.json` 생성
- capture 전에 `evidence/verification.json` 필수 검증
- 공통 runtime check와 시나리오별 interaction check를 정확한 집합으로 강제
- check status를 `pass`, `fail`, `not_run`으로 제한
- `pass`와 `fail`은 실제 evidence 파일과 설명을 요구
- `not_run`은 빈 evidence와 구체적인 사유를 요구
- template placeholder 사유를 그대로 두면 capture 거부
- verification JSON 자체나 template을 evidence로 참조하는 우회 거부
- Connection settings는 420 DIP, Device list는 520 DIP를 강제
- text scaling을 수행했으면 100보다 큰 실제 scale 값 요구
- 한국어·영어 장문 검증 시 `ko-KR`, `en-US` 기록 요구
- High Contrast 수행 시 실제 contrast theme 이름 요구
- 모든 rubric 점수에 category, score, evidence, uncertainty가 있는 `score_evidence` 10개 요구

### 95763ca — deterministic Task 11 reports

추가 또는 변경:

- `scripts/evaluation_report.py`
- `tests/test_evaluation_report.py`
- `evaluation/gate-metrics.schema.json`
- `scripts/evaluation_gate.py`
- implementation plan, evaluation README, rubric

기능:

- 하나의 `evaluation/results/metrics.json`에서 다음 세 파일을 함께 생성
  - `evaluation/results/scores.md`
  - `evaluation/results/findings.md`
  - `evaluation/results/gate-decision.md`
- scenario/category별 baseline·guided 점수와 증거, uncertainty 출력
- scenario별 defect counts와 traceable improvements 출력
- findings의 6개 고정 섹션 출력
  - attributable improvements
  - unchanged defects
  - regressions
  - ambiguous decisions
  - ignored rules
  - unnecessary output
- attributable improvements와 ignored rules는 기존 LazyDesign rule ID를 요구
- 보고서 명령은 PASS exit 0, valid FAIL exit 2, invalid input exit 1
- JSON 최상위가 object가 아닌 경우도 일관된 입력 오류로 처리

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
- Python tests: 28 passed
- Python compile: pass
- JSON parse: pass
- WinUI fixture build: warning 0, error 0
- whitespace check: pass

보고서 CLI synthetic 검증:

- PASS metrics: exit 0
- valid FAIL metrics: exit 2
- PASS output에 `scores.md`, `findings.md`, `gate-decision.md` 정확히 생성
- FAIL output의 gate 문서에 `Overall result: **FAIL**` 기록
- synthetic 파일과 build 산출물은 검증 후 제거함

## 4. 아직 수행되지 않은 핵심 작업

다음 실제 평가 작업은 여전히 수행되지 않았다.

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
- InfoBar action/dismissal
- ContentDialog default/close action과 focus return
- Narrator
- Accessibility Insights
- 실제 rubric 점수
- 실제 findings
- 실제 gate 판정

실행하지 않은 이유:

- 현재 대화는 이미 LazyDesign reference 내용을 읽어 baseline fresh context로 사용할 수 없음
- 로컬 Codex CLI 사용 금지
- subagent와 병렬 agent 사용 금지
- OpenAI/Azure OpenAI API key 없음
- 같은 model identifier와 reasoning level을 사용하는 독립 fresh context 6개를 생성할 실행기가 없음

현재 세션에서 코드를 대신 생성하거나 synthetic 결과를 실제 baseline/guided로 저장하면 실험 조건 위반이다.

## 5. packet 준비와 실행

각 실행 전에 존재하지 않는 새 destination으로 packet을 만든다. 기존 `.runs` packet을 재사용하지 않는다.

```powershell
python scripts/evaluation_harness.py prepare --condition baseline --scenario connection-settings --destination evaluation/.runs/baseline/connection-settings
python scripts/evaluation_harness.py prepare --condition baseline --scenario device-list --destination evaluation/.runs/baseline/device-list
python scripts/evaluation_harness.py prepare --condition baseline --scenario failure-confirmation --destination evaluation/.runs/baseline/failure-confirmation
python scripts/evaluation_harness.py prepare --condition guided --scenario connection-settings --destination evaluation/.runs/guided/connection-settings
python scripts/evaluation_harness.py prepare --condition guided --scenario device-list --destination evaluation/.runs/guided/device-list
python scripts/evaluation_harness.py prepare --condition guided --scenario failure-confirmation --destination evaluation/.runs/guided/failure-confirmation
```

모든 실행에서 다음을 동일하게 유지한다.

- exact model identifier
- reasoning level
- generation stopping condition
- operating system과 SDK
- tool access
- network policy
- 시작 프로젝트 SHA
- prompt bytes

각 실행은 별도 fresh context이며 prompt 보완, 중간 조언, 생성물 repair를 하지 않는다. 실패 결과도 그대로 보존한다.

## 6. structured verification 작성

생성 후 `RUN.template.md`를 `RUN.md`로 복사해 모든 필드를 실제 값으로 채운다. 이어서 `evidence/verification.template.json`을 `evidence/verification.json`으로 복사한다.

각 check 작성 규칙:

- 실제 수행하고 증거 파일이 있으면 `pass` 또는 `fail`
- 수행하지 않았으면 `not_run`
- `pass`와 `fail`은 `evidence` 배열에 `path`와 `detail`을 기록
- evidence path는 packet의 `evidence/` 아래 실제 파일을 가리켜야 함
- `not_run`은 evidence 배열을 비우고 구체적인 사유 기록
- template의 placeholder 사유를 그대로 두지 않음
- build, render, theme, input, accessibility를 서로 다른 check로 기록

예시 검증:

```powershell
python scripts/evaluation_evidence.py evaluation/.runs/baseline/connection-settings/evidence/verification.json
```

시나리오별 주요 check:

### Connection settings

- 420 DIP
- TextBox validation
- ComboBox popup
- ToggleSwitch state
- Save Button activation

### Device list

- 520 DIP
- CommandBar overflow
- ListView selection
- empty state
- remove command state

### Failure and confirmation

- InfoBar retry/dismissal
- ContentDialog default action
- ContentDialog close action
- focus return

공통 check에는 Light, Dark, High Contrast, text scaling, 한국어·영어 장문, keyboard, focus, Narrator, Accessibility Insights가 포함된다.

## 7. 결과 capture와 조건 검증

예시:

```powershell
python scripts/evaluation_harness.py capture --packet evaluation/.runs/baseline/connection-settings --destination evaluation/baseline/connection-settings
```

Capture는 다음을 검사한다.

- packet prompt와 reference hash
- pinned start project manifest
- `RUN.md` 필수 필드
- `verification.json` 구조와 evidence 파일
- 기존 destination 비존재

6개 capture 후:

```powershell
python scripts/evaluation_harness.py validate-results --root evaluation
```

이 명령이 pass하기 전에는 scoring을 시작하지 않는다.

## 8. scoring과 세 보고서 생성

구조화 입력:

```text
evaluation/results/metrics.json
```

계약:

```text
evaluation/gate-metrics.schema.json
```

각 scenario/condition은 다음을 포함한다.

- `scores`: 10개 정수 0, 1, 2
- `score_evidence`: category 1–10 각각 한 개
- `defects`: 7개 defect count

Guided score가 baseline보다 높은 모든 category에는 `traceable_improvements` entry가 필요하다. 모든 findings 섹션도 metrics에 기록한다.

보고서 생성:

```powershell
python scripts/evaluation_report.py evaluation/results/metrics.json --output-dir evaluation/results
```

생성 파일:

- `scores.md`
- `findings.md`
- `gate-decision.md`

PASS인 경우에만 `DESIGN.md`를 `validated-v0.1`로 변경하고 precision expansion을 승인한다. FAIL이면 `v0.1-candidate`를 유지하고 수정할 reference page 또는 retrieval behavior를 구체적으로 기록한다.

## 9. 다음 세션 시작 순서

1. `C:\Users\lky57\.wgpt\AGENTS.md`를 실제 파일에서 읽는다.
2. 저장소 및 하위 `AGENTS.md`를 읽는다.
3. remote, `origin/HEAD`, branch, upstream, HEAD, status, worktree를 확인한다.
4. 이 handover와 이전 evaluation harness handover를 읽는다.
5. `evaluation/README.md`, `evaluation/rubric.md`, `evaluation/run-matrix.json`을 읽는다.
6. 현재 SHA에서 static, tests, JSON, build를 다시 실행한다.
7. 동일 model/reasoning의 fresh-context 실행기가 확보된 경우에만 6개 run을 시작한다.
8. 각 run을 repair 없이 capture한다.
9. `validate-results`를 통과시킨다.
10. 실제 rubric과 findings를 `metrics.json`에 작성한다.
11. `evaluation_report.py`로 세 보고서를 생성한다.
12. gate 결과에 따라 README와 DESIGN 상태를 갱신한다.
13. PR은 Draft로 유지하고 사용자 승인 없이 Ready 전환 또는 merge하지 않는다.

## 10. 범위와 환경 제한

- Windows Design Kit component-level inspection 미완료
- `ui-kit` evidence 비활성
- gate 전 신규 component 범위 추가 금지
- GitHub Actions 추가 금지
- resolver, adapter, custom control library, static analyzer 추가 금지
- 현재 reference 문서를 UI-kit evidence로 승격하지 않음

이 Remote 환경은 `C:\Users\lky57\.wgpt\AGENTS.md`가 allowlist 밖이라 직접 읽기를 차단했다. 우회하거나 allowlist를 변경하지 않았다.

Narrator 실행 파일은 이전 세션에서 발견됐지만 실제 Narrator 검증은 수행하지 않았다. Accessibility Insights는 일반 설치 경로에서 발견되지 않았다. 이러한 항목은 실제 run의 `verification.json`에 `not_run`과 구체적인 사유로 기록한다.
