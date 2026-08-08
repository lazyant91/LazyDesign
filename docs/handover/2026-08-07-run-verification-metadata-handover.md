# LazyDesign RUN Verification Metadata Binding Handover

작성 시각: 2026-08-07 01:07 KST

## 1. 저장소 상태

- GitHub 저장소: `lazyant91/LazyDesign`
- 로컬 작업공간: `Z:\workspace\LazyDesign`
- 작업 브랜치: `docs/initial-reference-design`
- 이 문서 작성 직전 HEAD: `4ad2ccfd66fc834ca0009597fe1b0bb709c77860`
- upstream: `origin/docs/initial-reference-design`
- 기본 브랜치: `origin/main`
- 시작 프로젝트 snapshot commit: `b73babad19d0153707a49e5ba1ed9fb0a42c33ef`
- prompt/reference input commit: `7d01aae3cdc0241a7aa7ede7ee09738a6d5ee7cc`
- Draft PR: `#1`
- PR base/head: `main <- docs/initial-reference-design`

다음 세션은 작업 시작 전에 다음을 실제 상태에서 다시 확인한다.

- `C:\Users\lky57\.wgpt\AGENTS.md`
- 저장소 `AGENTS.md`와 하위 `AGENTS.md`
- remote
- `origin/HEAD`
- 현재 branch와 upstream
- HEAD SHA
- working tree
- worktree 목록

기존 변경, ignored packet, 실행 프로세스를 보존한다. 자동 switch, stash, restore, reset, clean을 수행하지 않는다.

이번 세션은 Stitch 또는 Figma 작업이 아니다. local Codex CLI, subagent, 병렬 agent를 사용하지 않았다.

## 2. 이번 세션에서 확인한 무결성 공백

직전 harness는 다음 RUN 필드를 실제 artifact와 연결했다.

```text
Reference files supplied
Generated file list
```

그러나 다음 두 필드는 `verification.json`과 연결되지 않았다.

```text
Rendered checks performed
Checks not performed
```

이전 구현에서는 다음과 같은 모순이 capture될 수 있었다.

1. `RUN.md`에는 `Rendered checks performed: not performed`라고 기록한다.
2. `verification.json`의 `rendered_runtime`은 `pass`로 기록하고 실제 evidence를 연결한다.
3. capture를 실행한다.

또는 `verification.json`의 대부분 check가 `not_run`인데 RUN에는 다음처럼 추상적인 prose만 기록할 수 있었다.

```text
Checks not performed: render, theme, input, accessibility
```

이 경우 reviewer는 어떤 check가 실제로 수행됐고 어떤 check가 수행되지 않았는지 RUN만으로 정확히 재현할 수 없었다.

## 3. 4ad2ccf — verification status와 RUN metadata 결합

커밋:

```text
4ad2ccfd66fc834ca0009597fe1b0bb709c77860
```

메시지:

```text
test: bind RUN checks to verification evidence
```

변경 파일:

- `scripts/evaluation_harness.py`
- `tests/test_evaluation_harness.py`
- `evaluation/README.md`
- `docs/superpowers/plans/2026-08-06-winui3-component-reference-v0.1.md`

## 4. Rendered checks performed 계약

`RUN.md`의 `Rendered checks performed`는 prose가 아니라 compact JSON 배열이다.

예시:

```text
Rendered checks performed: ["dark_theme","rendered_runtime"]
```

목록에 포함되는 check 조건:

- `verification.json` check status가 `pass` 또는 `fail`
- check ID가 `static_review`가 아님
- check ID가 `build`가 아님

`fail`도 실제로 수행된 check이므로 목록에 포함한다.

예를 들어 다음 check가 실패했더라도 실제로 실행했다면 목록에 포함한다.

```text
high_contrast
keyboard_navigation
narrator
```

다음 check는 별도 RUN 필드와 evidence 계약이 있으므로 이 배열에서 제외한다.

```text
static_review
build
```

정렬은 check ID 문자열 오름차순이다.

JSON 직렬화 옵션:

```python
ensure_ascii=False
separators=(",", ":")
```

따라서 불필요한 공백을 넣지 않는다.

다음 값은 유효하지 않다.

```text
not performed
render and theme
rendered runtime, dark theme
see verification.json
```

## 5. Checks not performed 계약

`RUN.md`의 `Checks not performed`도 compact JSON 배열이다.

예시:

```text
Checks not performed: ["accessibility_insights","high_contrast","narrator"]
```

목록에는 `verification.json`에서 status가 정확히 `not_run`인 모든 check ID를 포함한다.

이 목록은 다음도 포함할 수 있다.

```text
build
static_review
```

예를 들어 build를 수행하지 않았다면:

```text
Checks not performed: ["build",...]
```

정렬과 JSON 직렬화 규칙은 `Rendered checks performed`와 같다.

다음 값은 유효하지 않다.

```text
render, theme, input, accessibility
not performed
all runtime checks
see verification.json
```

## 6. 네 가지 exact RUN metadata

유효한 scored run은 다음 네 필드를 기계적으로 계산한다.

```text
Reference files supplied
Generated file list
Rendered checks performed
Checks not performed
```

Artifact 기반 필드:

```text
Reference files supplied: none
Generated file list: {"changed":["MainWindow.xaml"],"deleted":[]}
```

Verification 기반 필드:

```text
Rendered checks performed: ["rendered_runtime"]
Checks not performed: ["accessibility_insights","dark_theme","high_contrast"]
```

`inspect-packet`의 `expected_run_metadata`가 이 네 값을 반환한다.

`verification.json`이 아직 없으면 artifact 기반 두 필드만 반환한다.

`verification.json`이 존재하고 parse 가능하면 verification 기반 두 필드도 반환한다.

최종 `capture_ready`가 되려면 verification 자체의 schema/evidence 검증도 통과해야 한다.

## 7. 검증 위치

Verification metadata 일치 검증은 다음 세 단계에 적용된다.

### inspect-packet

RUN과 verification이 모두 존재할 때 모순을 `completion_errors`에 기록하고 `capture_ready`를 거부한다.

오류:

```text
RUN.md rendered-check metadata differs from verification
RUN.md not-performed metadata differs from verification
```

### capture

RUN과 verification이 불일치하면 destination을 생성하지 않고 `ValueError`로 중단한다.

### validate-results

Captured result의 RUN과 verification을 다시 비교한다. 따라서 capture 이후 metadata가 변조되거나 잘못된 result가 들어온 경우에도 validation이 실패한다.

## 8. RUN template 변경

새 packet의 `RUN.template.md`는 다음처럼 안내한다.

```text
Rendered checks performed: record after verification
Checks not performed: record after verification
```

이전 값:

```text
Rendered checks performed: not performed
```

`not performed`는 새 exact JSON 계약과 충돌하므로 template에서 제거했다.

Packet validation은 현재 template와 byte-level contract를 비교한다. 새로 실행할 scored run은 항상 현재 harness로 새 v2 packet을 prepare한다.

기존 v1 packet은 수정하거나 migration하지 않는다.

## 9. 실제 run 순서 변경

이전 순서에서는 build 직후 artifact metadata를 먼저 RUN에 복사하고 verification을 나중에 작성했다.

이제 최종 RUN은 verification status를 알아야 하므로 순서는 다음과 같다.

1. 새 v2 packet을 prepare한다.
2. `inspect-packet`에서 `ready`를 확인한다.
3. 독립 fresh context에서 generation을 실행한다.
4. prompt 변경, 추가 지시, repair를 하지 않는다.
5. controlled build를 정확히 한 번 실행한다.
6. build 후 non-build-output source를 수정하지 않는다.
7. runtime/static/accessibility 검증을 실제로 수행한다.
8. evidence 파일을 작성한다.
9. `verification.template.json`을 기반으로 `verification.json`을 완성한다.
10. `evaluation_evidence.py`로 verification을 검증한다.
11. `inspect-packet`을 실행한다.
12. `expected_run_metadata`의 네 값을 `RUN.md`에 그대로 복사한다.
13. Build command/result를 `build.txt`와 일치시킨다.
14. 나머지 RUN 필드를 실제 값으로 완성한다.
15. `inspect-packet`을 다시 실행한다.
16. status가 `capture_ready`인지 확인한다.
17. repair 없이 capture한다.

예시:

```powershell
python scripts/evaluation_harness.py prepare --condition baseline --scenario connection-settings --destination evaluation/.runs/v2/baseline/connection-settings
python scripts/evaluation_harness.py inspect-packet --packet evaluation/.runs/v2/baseline/connection-settings --condition baseline --scenario connection-settings
python scripts/evaluation_harness.py build --packet evaluation/.runs/v2/baseline/connection-settings
python scripts/evaluation_evidence.py evaluation/.runs/v2/baseline/connection-settings/evidence/verification.json
python scripts/evaluation_harness.py inspect-packet --packet evaluation/.runs/v2/baseline/connection-settings --condition baseline --scenario connection-settings
python scripts/evaluation_harness.py inspect-packet --packet evaluation/.runs/v2/baseline/connection-settings --condition baseline --scenario connection-settings
python scripts/evaluation_harness.py capture --packet evaluation/.runs/v2/baseline/connection-settings --destination evaluation/baseline/connection-settings
```

두 번의 후반 inspection 목적은 다르다.

- 첫 번째: verification이 완성된 상태에서 exact RUN metadata를 얻는다.
- 두 번째: RUN까지 완성한 뒤 `capture_ready`를 확인한다.

## 10. TDD 증거

### RED — verification과 RUN의 runtime metadata 모순

테스트:

```text
test_capture_refuses_runtime_check_metadata_that_differs_from_verification
```

절차:

1. guided connection-settings packet prepare
2. all-not-run RUN/verification fixture 완성
3. `render.txt` evidence 작성
4. `verification.json`의 `rendered_runtime`을 `pass`로 변경
5. RUN의 기존 runtime metadata는 변경하지 않음
6. capture 시도

기존 구현 결과:

```text
AssertionError: ValueError not raised
```

새 구현은 capture를 거부한다.

### RED — inspect에 verification metadata 없음

테스트:

```text
test_inspect_reports_copyable_expected_verification_metadata
```

기존 구현 결과:

```text
KeyError: 'Rendered checks performed'
```

새 구현은 `expected_run_metadata`에 두 verification 기반 필드를 포함한다.

### RED — template의 stale not performed 값

기존 template:

```text
Rendered checks performed: not performed
```

추가 assertion은 다음 값을 요구했다.

```text
Rendered checks performed: record after verification
```

기존 구현에서 assertion이 실패했고 template 변경 후 통과했다.

### GREEN

- 새 targeted 테스트 3개 통과
- evaluation harness 테스트 전체 34개 통과
- 전체 Python 테스트 56개 통과

## 11. 현재 검증 증거

기능 커밋 전 working tree에서 실행:

```powershell
python scripts/check_reference.py
python scripts/evaluation_harness.py validate
python -m unittest discover -s tests -p 'test_*.py' -v
python -m py_compile scripts/check_reference.py scripts/evaluation_harness.py scripts/evaluation_evidence.py scripts/evaluation_gate.py scripts/evaluation_report.py tests/test_evaluation_harness.py tests/test_evaluation_evidence.py tests/test_evaluation_gate.py tests/test_evaluation_report.py
python -m json.tool evaluation/run-matrix.json
python -m json.tool evaluation/verification.schema.json
python -m json.tool evaluation/gate-metrics.schema.json
Push-Location evaluation/fixtures/winui-start
dotnet --version
dotnet build LazyDesign.EvaluationApp.csproj -c Debug -p:Platform=x64
Pop-Location
git diff --check
```

결과:

- reference structural check: pass
- evaluation run matrix: pass
- Python tests: **56 passed**
- evaluation harness tests: **34 passed**
- Python compile: pass
- JSON parse: pass
- fixture selected SDK: **9.0.313**
- fixture build: warning 0, error 0
- whitespace check: pass

검증으로 생성된 fixture `bin`, `obj`, Python `__pycache__`는 제거했다.

완료 보고 전에는 이 handover commit이 반영된 정확한 최종 SHA에서 같은 검증을 새로 실행해야 한다.

## 12. 현재 packet/result 상태

기존 v1 packet 6개는 ignored 경로에 보존되어 있으며 모두 stale이다.

```text
ready: 0
in_progress: 0
capture_ready: 0
stale: 6
missing: 0
```

다음 실제 run root:

```text
evaluation/.runs/v2
```

실제 scored result 6개는 아직 없다.

```text
baseline/connection-settings: missing
baseline/device-list: missing
baseline/failure-confirmation: missing
guided/connection-settings: missing
guided/device-list: missing
guided/failure-confirmation: missing
```

`validate-results`는 의도대로 exit 1이다.

## 13. Fresh-context 실행 차단 상태

현재 대화는 LazyDesign reference와 harness 내용을 이미 읽었으므로 baseline fresh context가 아니다.

비밀값을 출력하지 않고 확인한 runner credential 상태는 이전 세션과 같다.

```text
OPENAI_API_KEY_PRESENT=False
AZURE_OPENAI_API_KEY_PRESENT=False
AZURE_OPENAI_ENDPOINT_PRESENT=False
OPENAI_BASE_URL_PRESENT=False
Python openai package installed=True
```

프로젝트 지침상 다음 실행 수단을 사용하지 않는다.

- local Codex CLI
- subagent
- parallel agent

따라서 baseline/guided fresh-context generation 6회는 실행하지 않았고 결과를 합성하지 않았다.

## 14. 아직 수행하지 않은 실제 검증

- baseline fresh-context generation 3회
- guided fresh-context generation 3회
- 실제 generated scenario build 6회
- 실제 app launch와 rendered screen 확인
- 420 DIP와 520 DIP behavior
- Light theme
- Dark theme rendered verification
- High Contrast
- text scale greater than 100%
- 한국어·영어 장문
- keyboard navigation
- focus visual
- ComboBox popup
- CommandBar overflow
- ListView selection
- InfoBar retry/dismissal
- ContentDialog default/close action과 focus return
- Narrator
- Accessibility Insights
- 실제 rubric score
- 실제 findings
- 실제 gate decision

Starting fixture build 성공은 generated scenario build나 runtime 검증으로 보고하지 않는다.

## 15. 범위와 변경 제한

- `DESIGN.md` 상태는 `v0.1-candidate` 유지
- precision expansion 계속 차단
- 신규 component 추가 금지
- GitHub Actions 추가 금지
- resolver, adapter, custom control library, static analyzer 추가 금지
- Windows Design Kit component-level inspection 미완료
- `ui-kit` evidence 비활성
- 기존 v1 packet 삭제, 수정, migration 금지
- Accessibility Insights 또는 SDK 도구 설치는 사용자 승인 없이 금지
- GUI app, Narrator, theme, High Contrast, text scaling 설정은 실제 run 절차 밖에서 변경 금지
- PR은 Draft 유지
- 사용자 승인 없이 Ready 전환 또는 merge 금지

## 16. 다음 작업 판단

다음 세션은 먼저 동일 model/reasoning의 독립 fresh-context 실행기와 필요한 credential이 확보됐는지 확인한다.

실행기가 확보된 경우:

- 실제 v2 packet 하나만 prepare
- `ready` 확인
- exact prompt/reference set으로 generation
- controlled build
- 실제 verification/evidence 작성
- 네 가지 `expected_run_metadata` 복사
- `capture_ready` 확인
- immutable capture
- 같은 조건으로 나머지 5회 반복

실행기가 여전히 없으면 실제 scored packet을 미리 prepare하지 않는다.

추가 static harness 변경은 구체적으로 재현되는 무결성 오류가 있을 때만 수행한다. 단순 convenience 기능이나 speculative schema 확장은 추가하지 않는다.
