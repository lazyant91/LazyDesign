# LazyDesign 평가 실행 하네스 Handover

작성 시각: 2026-08-06 17:35 KST

## 1. 저장소 상태

- GitHub 저장소: lazyant91/LazyDesign
- 로컬 작업공간: Z:\workspace\LazyDesign
- 작업 브랜치: docs/initial-reference-design
- 문서 작성 직전 HEAD: 271dd9956953b6bd444dbd3db30463cb25989525
- 시작 프로젝트 snapshot commit: b73babad19d0153707a49e5ba1ed9fb0a42c33ef
- prompt/reference input commit: 7d01aae3cdc0241a7aa7ede7ee09738a6d5ee7cc
- Draft PR: #1
- PR base/head: main <- docs/initial-reference-design

다음 세션은 위 HEAD를 가정하지 말고 remote, origin/HEAD, branch, upstream, HEAD, status, worktree를 다시 확인한다. PR은 Draft 상태를 유지하고 Ready 전환 또는 병합하지 않는다.

## 2. 이번 세션에서 추가된 커밋

### 8098feb - controlled run packets

추가 파일:

- evaluation/run-matrix.json
- scripts/evaluation_harness.py
- tests/test_evaluation_harness.py
- evaluation/README.md 실행 절차
- evaluation/.runs/ ignore

기능:

- 동일 fixture commit에서 fresh project packet 생성
- baseline에는 LazyDesign reference를 넣지 않음
- guided에는 시나리오별 고정 reference set만 넣음
- prompt와 reference를 작업 트리가 아니라 pinned input commit에서 추출
- prompt, reference, 시작 프로젝트 파일의 SHA-256 기록
- 기존 packet 디렉터리를 재사용하거나 덮어쓰지 않음

### 36ad7a1 - capture and verify runs

기능:

- 생성 후 PROMPT.md, guided context, 시작 프로젝트 manifest 변조 검사
- RUN.md 필수 필드와 미해결 placeholder 검사
- fixture 대비 변경·추가 파일을 generated/에 보존
- 삭제 파일을 CAPTURE.json에 보존
- bin, obj, .vs는 결과 캡처에서 제외
- baseline/guided 6개 결과의 동일 모델, reasoning, stopping condition, OS, SDK, tool access, network policy 검사
- 모든 실행에서 Fresh context: yes, Generation intervention: none 요구

### 271dd99 - mechanical quality gate

추가 파일:

- evaluation/gate-metrics.schema.json
- scripts/evaluation_gate.py
- tests/test_evaluation_gate.py

기능:

- 3개 시나리오 x baseline/guided x 10개 rubric score 검증
- 7개 defect count 검증
- 6개 gate condition 기계 판정
- baseline denominator가 0이면 not demonstrated
- anatomy와 accessibility defect가 각각 감소해야 함
- 불필요한 ControlTemplate과 complexity defect는 증가하지 않아야 함
- guided score가 오른 모든 category에 기존 LazyDesign rule ID와 evidence가 있어야 함
- PASS exit 0, 유효한 FAIL exit 2, 입력 오류 exit 1
- gate-decision.md 결정론적 생성

## 3. 현재 검증 증거

문서 작성 전 현재 브랜치에서 실행:

    python scripts/check_reference.py
    python scripts/evaluation_harness.py validate
    python -m unittest discover -s tests -p 'test_*.py' -v
    python -m py_compile scripts/check_reference.py scripts/evaluation_harness.py scripts/evaluation_gate.py tests/test_evaluation_harness.py tests/test_evaluation_gate.py
    python -m json.tool evaluation/run-matrix.json
    python -m json.tool evaluation/gate-metrics.schema.json
    dotnet build evaluation/fixtures/winui-start/LazyDesign.EvaluationApp.csproj -c Debug -p:Platform=x64
    git diff --check

결과:

- reference structural check: pass
- evaluation run matrix: pass
- Python tests: 14 passed
- Python compile: pass
- JSON parse: pass
- WinUI fixture build: warning 0, error 0
- whitespace check: pass

Gate CLI synthetic verification:

- PASS fixture: exit 0
- zero overflow denominator가 있는 유효한 FAIL fixture: exit 2
- synthetic 파일은 evaluation/.remote-temp/에서 제거함

실제 결과 검사:

    python scripts/evaluation_harness.py validate-results --root evaluation

현재 baseline/guided 6개 결과 디렉터리가 없으므로 exit 1이 정상이다. 누락된 여섯 경로를 모두 출력한다.

## 4. 아직 수행되지 않은 핵심 작업

- baseline 3회
- guided 3회
- 생성물 build
- 실제 scenario render
- 420 DIP와 520 DIP
- Light, Dark, High Contrast
- text scaling
- 한국어·영어 장문
- keyboard와 focus
- ComboBox popup
- CommandBar overflow
- ListView selection
- ContentDialog default/close action
- Accessibility Insights
- Narrator
- rubric 실제 점수
- gate 실제 판정

현재 세션에서 실행하지 않은 이유:

- 현재 대화는 이미 LazyDesign 문서를 읽어 baseline context로 사용할 수 없음
- 로컬 Codex CLI 사용 금지
- subagent와 병렬 agent 사용 금지
- OPENAI_API_KEY와 AZURE_OPENAI_API_KEY 없음
- 동일 모델 family/reasoning의 독립 fresh context를 자동 생성할 실행기가 없음

현재 세션이 baseline 코드를 작성하거나 guided 결과를 수리하거나 synthetic 결과를 실제 점수로 커밋하면 실험이 무효다.

## 5. 6개 packet 준비

기존 evaluation/.runs/ packet은 재사용하지 않는다. 각 실제 실행 전에 destination이 없는 새 packet을 만든다.

    python scripts/evaluation_harness.py prepare --condition baseline --scenario connection-settings --destination evaluation/.runs/baseline/connection-settings
    python scripts/evaluation_harness.py prepare --condition baseline --scenario device-list --destination evaluation/.runs/baseline/device-list
    python scripts/evaluation_harness.py prepare --condition baseline --scenario failure-confirmation --destination evaluation/.runs/baseline/failure-confirmation

    python scripts/evaluation_harness.py prepare --condition guided --scenario connection-settings --destination evaluation/.runs/guided/connection-settings
    python scripts/evaluation_harness.py prepare --condition guided --scenario device-list --destination evaluation/.runs/guided/device-list
    python scripts/evaluation_harness.py prepare --condition guided --scenario failure-confirmation --destination evaluation/.runs/guided/failure-confirmation

각 packet 내용:

    PROMPT.md
    PACKET.json
    RUN.template.md
    project/
    context/       guided only

## 6. 각 fresh context 실행 절차

1. 모든 6개 실행에서 같은 model identifier와 reasoning level을 정한다.
2. tool access와 network policy를 동일하게 정한다. 기본은 network disabled다.
3. baseline context에는 project/와 PROMPT.md만 제공한다.
4. guided context에는 project/, PROMPT.md, packet의 context/ 파일만 제공한다.
5. prompt를 보완하거나 실행 도중 조언을 추가하지 않는다.
6. 모델은 packet의 project/ 안에서만 생성한다.
7. 생성 중 build 오류나 UI 결함을 사람이 수리하지 않는다.
8. 실패 결과도 그대로 둔다.
9. RUN.template.md를 RUN.md로 복사하고 모든 필드를 실제 값으로 채운다.
10. build와 render/theme/input/accessibility evidence를 서로 구분해 기록한다.
11. 필요한 로그나 관찰은 packet의 evidence/ 아래에 둔다.
12. 캡처 전 PROMPT.md, PACKET.json, context/를 수정하지 않는다.

필수 RUN 필드:

    Model identifier
    Reasoning level
    Fresh context
    Generation stopping condition
    Starting project repository and SHA
    Operating system
    .NET SDK
    Windows App SDK package
    Tool access
    Network access
    Generation intervention
    Build result
    Rendered checks performed
    Checks not performed

## 7. 결과 캡처

예시:

    python scripts/evaluation_harness.py capture --packet evaluation/.runs/baseline/connection-settings --destination evaluation/baseline/connection-settings

나머지 다섯 실행도 condition/scenario에 맞는 destination으로 캡처한다.

Capture는 기존 destination을 덮어쓰지 않는다. 잘못 캡처한 결과를 삭제하고 다시 만드는 방식으로 결과를 수리하지 않는다. 오류가 있으면 원인을 기록하고 원본 packet을 보존한다.

6개 캡처 후:

    python scripts/evaluation_harness.py validate-results --root evaluation

이 명령이 pass하기 전에는 점수 계산을 시작하지 않는다.

## 8. runtime verification matrix

### Connection settings

- 420 DIP content width
- long Korean labels/helper/validation
- long English equivalents
- TextBox label/helper/validation separation
- ComboBox popup and selected value
- ToggleSwitch checked state
- Save Button keyboard activation
- tab order and focus visual

### Device list

- 520 DIP content width
- long Korean and English device names
- CommandBar primary and overflow commands
- ListView selected/unselected state
- empty state
- keyboard navigation and focus
- remove command state

### Failure and confirmation

- InfoBar title, message, severity, retry, dismissal
- long Korean failure message
- ContentDialog selected device identity
- primary Remove, Cancel, close behavior
- default focus, Enter, Escape
- focus return after close

### Environment layers

각 시나리오에서 실제 수행 여부를 분리 기록한다.

- build
- rendered runtime
- Light
- Dark
- High Contrast
- text scaling
- keyboard/input
- Narrator
- Accessibility Insights

실행하지 못한 항목은 not performed로 기록한다. build success를 render 또는 accessibility success로 표현하지 않는다.

## 9. scoring과 gate

6개 결과가 모두 immutable 상태로 준비된 후 rubric을 채점한다.

구조화 입력:

    evaluation/results/metrics.json

형식:

    evaluation/gate-metrics.schema.json

각 guided score가 baseline보다 높은 scenario/category에는 traceable_improvements entry가 필요하다.

Gate 생성:

    python scripts/evaluation_gate.py evaluation/results/metrics.json --output evaluation/results/gate-decision.md

- exit 0: PASS
- exit 2: valid FAIL
- exit 1: invalid/incomplete metrics

PASS인 경우에만 DESIGN.md를 validated-v0.1로 변경하고 precision expansion을 승인한다. FAIL이면 v0.1-candidate를 유지하고 정확한 reference page 또는 retrieval behavior 수정 대상을 기록한다.

## 10. Windows Design Kit와 범위 제한

- Windows Design Kit component-level inspection 미완료
- ui-kit evidence 비활성
- gate 전 신규 component 범위 추가 금지
- GitHub Actions 추가 금지
- resolver, adapter, custom control library, static analyzer 추가 금지
- 현재 component/foundation 문서를 실제 UI-kit evidence로 승격하지 않음

## 11. 다음 세션 시작 순서

1. C:\Users\lky57\.wgpt\AGENTS.md를 실제 파일에서 읽는다.
2. 저장소 및 하위 AGENTS.md를 읽는다.
3. remote, origin/HEAD, branch, upstream, HEAD, status, worktree를 확인한다.
4. 원격 branch가 예상과 다르면 fetch 후 충돌 여부를 먼저 확인한다.
5. 이 handover와 evaluation/README.md, evaluation/rubric.md, evaluation/run-matrix.json을 읽는다.
6. 전체 static/tests/build를 현재 SHA에서 다시 실행한다.
7. 동일 모델과 reasoning을 사용할 수 있는 fresh-context 실행기를 확보한 경우에만 baseline/guided 6회를 시작한다.
8. 생성 도중 수정, repair, prompt 보완을 하지 않는다.
9. 모든 결과를 capture하고 validate-results를 통과시킨다.
10. rubric을 채점하고 gate script를 실행한다.
11. 결과에 따라 README와 DESIGN 상태를 갱신한다.
12. PR은 Draft 상태로 유지하며 사용자 승인 없이 Ready 전환 또는 merge하지 않는다.

## 12. 알려진 환경 제한

이 Remote 환경은 C:\Users\lky57\.wgpt\AGENTS.md가 allowlist 밖이라 직접 읽기를 차단했다. 우회하거나 allowlist를 변경하지 않았다. 다음 로컬 환경에서 접근 가능하면 반드시 다시 직접 읽는다.

Narrator 실행 파일은 발견됐지만 실제 assistive-technology 검증은 수행하지 않았다. Accessibility Insights는 일반 설치 경로에서 발견되지 않았다.
