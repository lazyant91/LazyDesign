# LazyDesign RUN Artifact Metadata Binding Handover

작성 시각: 2026-08-06 23:28 KST

## 1. 저장소 상태

- GitHub 저장소: `lazyant91/LazyDesign`
- 로컬 작업공간: `Z:\workspace\LazyDesign`
- 작업 브랜치: `docs/initial-reference-design`
- 이 문서 작성 직전 HEAD: `4250a442761042fcb6b37067956f7fdb8aefedc5`
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

이번 세션은 Stitch 작업이 아니므로 Stitch 전용 절차를 실행하지 않았다. local Codex CLI, subagent, 병렬 agent도 사용하지 않았다.

## 2. 이번 세션에서 발견한 RUN metadata 무결성 공백

직전 harness는 다음 항목을 이미 기계적으로 검증했다.

- packet v2 prompt/context 계약
- pinned SDK와 package 값
- controlled build command와 exit code
- build 당시 project-state SHA-256
- build 후 source 변경 여부
- captured generated/evidence 파일 hash

그러나 `RUN.md`의 다음 두 필드는 실제 artifact와 연결되지 않았다.

```text
Reference files supplied
Generated file list
```

이전 구현에서는 다음과 같은 부정확한 metadata가 있어도 capture가 가능했다.

### Baseline reference metadata 오류

Baseline packet에는 LazyDesign reference가 전혀 없지만 다음과 같이 기록할 수 있었다.

```text
Reference files supplied: see PACKET.json
```

### Generated file list 오류

실제 generated/deleted 파일과 무관하게 다음과 같은 prose를 기록할 수 있었다.

```text
Generated file list: captured automatically
```

따라서 RUN metadata만 읽는 reviewer는 실제 packet/reference와 생성 결과를 잘못 이해할 수 있었다.

## 3. 4250a44 — RUN metadata artifact binding

커밋:

```text
4250a442761042fcb6b37067956f7fdb8aefedc5
```

메시지:

```text
test: bind run metadata to captured artifacts
```

변경 파일:

- `scripts/evaluation_harness.py`
- `tests/test_evaluation_harness.py`
- `evaluation/README.md`
- `docs/superpowers/plans/2026-08-06-winui3-component-reference-v0.1.md`

## 4. Reference files supplied 계약

Packet의 `references` 배열이 비어 있으면 RUN 값은 정확히 다음이어야 한다.

```text
Reference files supplied: none
```

현재 이는 모든 baseline run에 적용된다.

Packet의 `references` 배열이 비어 있지 않으면 RUN 값은 정확히 다음이어야 한다.

```text
Reference files supplied: see PACKET.json
```

현재 이는 모든 guided run에 적용된다.

다른 표현은 허용하지 않는다.

예:

```text
no references
baseline
fixed context
DESIGN.md and components
see context directory
```

위와 같은 값은 의미가 비슷해도 contract mismatch로 거부된다.

검증 위치:

- `inspect-packet`
- `capture`
- `validate-results`

오류:

```text
RUN.md reference metadata differs from packet
```

## 5. Generated file list 계약

RUN의 `Generated file list`는 prose가 아니라 compact JSON이다.

형식:

```json
{"changed":["<path>","<path>"],"deleted":["<path>"]}
```

예:

```text
Generated file list: {"changed":["MainWindow.xaml","MainWindow.xaml.cs"],"deleted":["app.manifest"]}
```

### changed

다음 파일이 포함된다.

- 시작 프로젝트에 있었고 내용이 달라진 파일
- 시작 프로젝트에 없었고 generation이 새로 추가한 파일

### deleted

시작 프로젝트에 있었지만 current packet project에서 사라진 파일을 포함한다.

### 제외 경로

다음 build output 디렉터리는 metadata와 capture generated 파일 집합에서 제외한다.

```text
bin
obj
.vs
```

### 정렬

Path는 repository-relative POSIX 형식을 사용한다.

```text
MainWindow.xaml
Views/ConnectionPage.xaml
```

Changed records는 기존 `_file_hashes` 정렬 규칙을 사용한다.

1. path casefold 기준
2. 원래 path 기준

Deleted paths는 정렬된 문자열 목록이다.

JSON은 다음 옵션으로 직렬화된다.

```python
ensure_ascii=False
separators=(",", ":")
```

따라서 불필요한 공백이 없어야 한다.

검증 위치:

- `inspect-packet`
- `capture`
- `validate-results`

오류:

```text
RUN.md generated file list differs from project
```

## 6. inspect-packet expected_run_metadata

정확한 JSON을 운영자가 손으로 계산하지 않도록 유효 packet의 inspection 결과에 다음 필드를 추가했다.

```json
{
  "expected_run_metadata": {
    "Reference files supplied": "none",
    "Generated file list": "{\"changed\":[\"MainWindow.xaml\"],\"deleted\":[]}"
  }
}
```

Guided 예:

```json
{
  "expected_run_metadata": {
    "Reference files supplied": "see PACKET.json",
    "Generated file list": "{\"changed\":[\"MainWindow.xaml\"],\"deleted\":[]}"
  }
}
```

`expected_run_metadata`는 packet contract가 유효할 때 제공된다.

- `ready`
- `in_progress`
- `capture_ready`

Missing 또는 stale packet에는 exact metadata를 신뢰할 수 없으므로 제공하지 않는다.

## 7. 실제 run 순서 변경

동일 model/reasoning의 독립 fresh-context 실행기가 확보된 경우 한 run은 다음 순서를 따른다.

1. 새 v2 packet을 prepare한다.
2. `inspect-packet`에서 `ready`를 확인한다.
3. fresh context에서 generation을 실행한다.
4. prompt 변경, 추가 지시, repair를 하지 않는다.
5. generation이 끝난 뒤 controlled build를 정확히 한 번 실행한다.
6. build 후 non-build-output source를 수정하지 않는다.
7. `inspect-packet`을 실행한다.
8. 출력의 `expected_run_metadata` 두 값을 `RUN.md`에 그대로 복사한다.
9. Build command/result도 `build.txt`와 일치시킨다.
10. 실제 수행한 verification evidence를 기록한다.
11. `inspect-packet`에서 `capture_ready`를 확인한다.
12. repair 없이 capture한다.

예시:

```powershell
python scripts/evaluation_harness.py prepare --condition baseline --scenario connection-settings --destination evaluation/.runs/v2/baseline/connection-settings
python scripts/evaluation_harness.py inspect-packet --packet evaluation/.runs/v2/baseline/connection-settings --condition baseline --scenario connection-settings
python scripts/evaluation_harness.py build --packet evaluation/.runs/v2/baseline/connection-settings
python scripts/evaluation_harness.py inspect-packet --packet evaluation/.runs/v2/baseline/connection-settings --condition baseline --scenario connection-settings
python scripts/evaluation_harness.py capture --packet evaluation/.runs/v2/baseline/connection-settings --destination evaluation/baseline/connection-settings
```

첫 inspection은 generation 전 `ready` 확인용이다.

두 번째 inspection은 build 후 exact RUN metadata를 얻기 위한 것이다. 이 시점에서는 RUN 또는 verification이 아직 완성되지 않아 `in_progress`일 수 있다.

RUN과 verification을 완성한 뒤 세 번째 inspection을 실행하고 `capture_ready`를 요구한다.

## 8. TDD 증거

### RED — baseline reference mismatch

테스트:

```text
test_capture_refuses_reference_metadata_that_differs_from_packet
```

절차:

1. baseline packet prepare
2. valid RUN 작성
3. `Reference files supplied: none`을 `see PACKET.json`으로 변조
4. capture 시도

기존 구현에서는 capture가 성공했다.

실제 RED 결과:

```text
AssertionError: ValueError not raised
```

새 구현은 `ValueError`로 거부한다.

### RED — generated file list mismatch

테스트:

```text
test_capture_refuses_generated_file_list_that_differs_from_project
```

절차:

1. guided packet prepare
2. `MainWindow.xaml` 변경
3. valid RUN 작성
4. exact compact JSON을 `captured automatically`으로 변조
5. capture 시도

기존 구현에서는 capture가 성공했다.

실제 RED 결과:

```text
AssertionError: ValueError not raised
```

새 구현은 `ValueError`로 거부한다.

### RED — copyable inspection metadata

테스트:

```text
test_inspect_reports_copyable_expected_run_metadata
```

기존 구현에는 `expected_run_metadata` 필드가 없었다.

실제 RED 결과:

```text
KeyError: 'expected_run_metadata'
```

새 구현은 packet의 exact reference/generated metadata를 반환한다.

### GREEN

- 새 metadata 테스트 3개 통과
- evaluation harness 테스트 전체 34개 통과
- 전체 Python 테스트 54개 통과

## 9. 테스트 fixture 순서 수정

새 contract는 RUN metadata가 generation 결과를 정확히 반영해야 한다.

기존 synthetic test fixture 일부는 다음 순서였다.

1. `complete_run(packet)`
2. project 파일 변경
3. capture

이는 실제 운영 계약과 반대 순서였다.

유효 fixture는 다음 순서로 수정했다.

1. project 파일 변경/추가/삭제
2. `complete_run(packet)`
3. capture

Build 후 source 변경을 의도적으로 검증하는 negative test는 기존 순서를 유지하며 capture 거부를 확인한다.

## 10. 현재 검증 증거

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
- Python tests: **54 passed**
- evaluation harness tests: **34 passed**
- Python compile: pass
- JSON parse: pass
- fixture selected SDK: **9.0.313**
- fixture build: warning 0, error 0
- whitespace check: pass

검증으로 생성된 fixture `bin`, `obj`, Python `__pycache__`는 제거했다.

완료 보고 전에는 최종 handover commit이 반영된 정확한 최종 SHA에서 같은 검증을 새로 실행해야 한다.

## 11. 현재 packet/result 상태

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

## 12. Fresh-context 실행 차단 상태

현재 대화는 LazyDesign reference와 harness 내용을 이미 읽었으므로 baseline fresh context가 아니다.

비밀값을 출력하지 않고 확인한 runner credential 상태는 이전과 같다.

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

따라서 baseline/guided fresh-context generation 6회는 실행하지 않았으며 결과를 합성하지 않았다.

## 13. 아직 수행하지 않은 검증

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

## 14. 범위와 변경 제한

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
