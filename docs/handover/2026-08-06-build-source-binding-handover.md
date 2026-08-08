# LazyDesign Controlled Build Source Binding Handover

작성 시각: 2026-08-06 22:41 KST

## 1. 저장소 상태

- GitHub 저장소: `lazyant91/LazyDesign`
- 로컬 작업공간: `Z:\workspace\LazyDesign`
- 작업 브랜치: `docs/initial-reference-design`
- 이 문서 작성 직전 HEAD: `acdfdb6a1786cc1a3978e1ccee643689dd9c4602`
- upstream: `origin/docs/initial-reference-design`
- 기본 브랜치: `origin/main`
- 시작 프로젝트 snapshot commit: `b73babad19d0153707a49e5ba1ed9fb0a42c33ef`
- prompt/reference input commit: `7d01aae3cdc0241a7aa7ede7ee09738a6d5ee7cc`
- Draft PR: `#1`
- PR base/head: `main <- docs/initial-reference-design`

다음 세션은 remote, `origin/HEAD`, branch, upstream, HEAD, status, worktree를 실제로 다시 확인한다. 기존 변경, ignored packet, 실행 프로세스를 보존하고 자동 switch, stash, restore, reset, clean을 수행하지 않는다.

이번 세션에서 다음 지침을 실제 파일에서 읽었다.

- `C:\Users\lky57\.wgpt\AGENTS.md`
- `Z:\workspace\LazyDesign\AGENTS.md`

Stitch 요청이 아니므로 Stitch 전용 절차는 실행하지 않았다. local Codex CLI, subagent, 병렬 agent도 사용하지 않았다.

## 2. 이번 세션에서 발견한 build 무결성 공백

직전 controlled build는 pinned SDK, Windows App SDK, exit code를 검증했지만 build 결과를 실제 generated source 상태와 충분히 묶지 않았다.

이전 동작에서는 다음이 가능했다.

1. controlled build를 실행한다.
2. `evidence/build.txt`를 만든다.
3. build 후 `project/MainWindow.xaml` 같은 generated source를 수정한다.
4. 기존 build evidence로 capture한다.

또한 `RUN.md`의 Build command가 단순히 다음 prefix로 시작하기만 하면 통과했다.

```text
python scripts/evaluation_harness.py build --packet 
```

따라서 실제 packet과 다른 packet 경로를 기록해도 capture가 가능했다.

추가로 current packet에서 top-level `.csproj` 개수를 재탐색했기 때문에 모델이 pinned project를 삭제하거나 alternate project를 추가하면 helper가 packet을 invalid로 처리했다. 그러나 이러한 변경은 생성 결과의 build 실패 또는 불필요한 복잡성으로 보존하고 평가해야 한다.

## 3. acdfdb6 — controlled build source binding

커밋:

```text
acdfdb6a1786cc1a3978e1ccee643689dd9c4602
```

메시지:

```text
test: bind controlled builds to generated source
```

변경 파일:

- `scripts/evaluation_harness.py`
- `tests/test_evaluation_harness.py`
- `evaluation/README.md`
- `docs/superpowers/plans/2026-08-06-winui3-component-reference-v0.1.md`

## 4. Pinned project target

Harness는 현재 packet에서 `.csproj`를 탐색해 선택하지 않는다.

시작 프로젝트 commit의 tree에서 top-level `.csproj`를 확인하고 정확히 하나만 허용한다. 현재 pinned project 파일은 다음과 같다.

```text
LazyDesign.EvaluationApp.csproj
```

Controlled build target은 항상 다음 경로다.

```text
<packet>/project/LazyDesign.EvaluationApp.csproj
```

생성이 `Alternate.csproj`를 추가해도 build target은 바뀌지 않는다. alternate project는 generated artifact로 남아 XAML simplicity/complexity 평가 대상이 된다.

생성이 pinned project 파일을 삭제해도 packet을 invalid로 중단하지 않는다. `dotnet build`를 삭제된 pinned 경로에 실제로 실행해 nonzero exit를 `evidence/build.txt`에 기록한다. CLI는 build failure를 exit 2로 전달하며 결과는 repair 없이 capture할 수 있다.

Pinned start commit 자체에 top-level `.csproj`가 정확히 하나가 아니면 이는 평가 환경 오류이므로 build environment validation이 실패한다.

## 5. Project-state binding

Controlled build 후 `project/`의 모든 non-build-output 파일을 다음 규칙으로 정규화한다.

- 재귀적으로 모든 파일 수집
- `bin`, `obj`, `.vs` 제외
- repository-relative POSIX path 사용
- 파일별 SHA-256 기록
- path 기준 대소문자 독립 정렬 후 원래 path 정렬
- canonical compact JSON으로 직렬화
- 전체 JSON의 SHA-256 계산

`evidence/build.txt`는 다음 항목을 추가로 기록한다.

```text
Harness command
Project state SHA-256
Project file count
```

예시 형태:

```text
Harness command: python scripts/evaluation_harness.py build --packet evaluation/.runs/v2/baseline/connection-settings
Project state SHA-256: <64-character lowercase SHA-256>
Project file count: <integer>
```

`inspect-packet`과 `capture`는 현재 packet project 상태를 다시 계산하여 build evidence의 digest와 file count가 일치하는지 확인한다.

Build 후 non-build-output 파일이 추가, 수정, 삭제되면 다음 오류로 capture-ready가 차단된다.

```text
build: project changed after controlled build
```

Build 후 source 변경이 필요하면 기존 evidence를 재사용하거나 결과를 repair하지 않는다. 해당 scored run은 이미 generation/build sequence가 오염됐으므로 새로운 fresh-context packet에서 다시 시작해야 한다.

`bin`, `obj`, `.vs`는 project-state digest에서 제외된다. build 후 build output만 변한 것은 source 변경으로 취급하지 않는다.

## 6. Harness command binding

Build helper는 실제 packet 경로로 정확한 command를 만든다.

```text
python scripts/evaluation_harness.py build --packet <repository-relative-packet-path>
```

이 command를 `evidence/build.txt`의 `Harness command`에 기록하고 build result object에도 반환한다.

Build가 수행된 run에서 다음 세 값은 정확히 일치해야 한다.

1. helper가 생성한 Harness command
2. `evidence/build.txt`의 Harness command
3. `RUN.md`의 Build command

다른 packet 경로, 축약 command, root-level `dotnet build`, 추가 flag를 기록하면 capture-ready와 capture가 거부된다.

`RUN.md` Build result도 build.txt의 실제 exit code와 정확히 다음 형식으로 일치해야 한다.

```text
exit <code>
```

## 7. Captured result 검증

Capture 전에는 packet의 실제 `project/` 파일 목록으로 build-state digest를 검증한다.

Capture 후 result에는 전체 시작 프로젝트가 복사되지 않고 다음만 보존된다.

- `PACKET.json`의 original `project_files`
- `CAPTURE.json`의 `generated_files`
- `CAPTURE.json`의 `deleted_files`

`validate-results`는 이 세 집합으로 final project-state file list를 재구성하고 build evidence의 project-state digest와 file count를 다시 검증한다.

따라서 capture 시점에는 일치했지만 captured generated/deleted metadata가 나중에 바뀐 경우에도 기존 immutable capture 검증과 build-state 검증이 함께 실패한다.

주의: capture 전 `build.txt`는 암호학적으로 외부 서명된 provenance가 아니다. Helper는 같은 경로를 덮어쓰지 않고 구조와 source-state를 검증하며, capture가 파일 hash를 결과에 고정한다. 운영자는 build evidence를 수동 편집하거나 삭제하지 않아야 한다.

## 8. TDD 증거

### RED — build 후 source 변경

테스트:

```text
test_capture_refuses_project_changed_after_controlled_build
```

절차:

1. generated XAML 변경
2. controlled build
3. RUN/verification 완성
4. XAML을 다시 변경
5. capture 시도

기존 구현에서는 capture가 성공할 수 있었다. 새 구현은 `ValueError`로 거부한다.

### RED — 다른 packet command

테스트:

```text
test_capture_refuses_build_command_for_another_packet
```

기존 구현은 command prefix만 검사해 다른 packet path를 허용했다. 새 구현은 exact command mismatch를 거부한다.

### RED — pinned project 삭제

테스트:

```text
test_build_missing_pinned_project_is_preserved_as_failure
```

기존 구현은 top-level `.csproj`가 0개라며 `ValueError`로 중단했다. 새 구현은 actual dotnet failure evidence를 만들고 capture-ready/capture를 허용한다.

### RED — alternate project 추가

테스트:

```text
test_build_targets_pinned_project_when_alternate_project_is_added
```

기존 구현은 top-level `.csproj`가 2개라며 중단했다. 새 구현은 pinned original project만 build하고 alternate project를 generated artifact로 유지한다.

### GREEN

새 테스트 4개와 기존 evaluation harness 테스트 전체 29개가 통과했다.

## 9. 현재 전체 검증 증거

현재 working tree에서 기능 커밋 전 실행:

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
- Python tests: **51 passed**
- evaluation harness tests: **29 passed**
- Python compile: pass
- JSON parse: pass
- fixture selected SDK: **9.0.313**
- fixture build: warning 0, error 0
- whitespace check: pass

검증으로 생성된 fixture `bin`, `obj`, Python `__pycache__`는 제거했다.

완료 보고 전에는 최종 handover commit이 반영된 정확한 최종 SHA에서 같은 검증을 새로 실행해야 한다.

## 10. 현재 packet/result 상태

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

## 11. Fresh-context 실행 차단 상태

비밀값을 출력하지 않고 존재 여부만 확인한 상태는 이전과 같다.

```text
OPENAI_API_KEY_PRESENT=False
AZURE_OPENAI_API_KEY_PRESENT=False
AZURE_OPENAI_ENDPOINT_PRESENT=False
OPENAI_BASE_URL_PRESENT=False
Python openai package installed=True
```

현재 대화는 LazyDesign reference와 harness 내용을 이미 읽었으므로 baseline fresh context가 아니다.

프로젝트 지침상 다음을 사용하지 않는다.

- local Codex CLI
- subagent
- parallel agent

따라서 baseline/guided fresh-context model generation 6회는 실행하지 않았고 결과를 합성하지 않았다.

## 12. 실제 run 순서

동일 model/reasoning의 독립 fresh-context 실행기가 확보된 경우에만 다음 절차를 실행한다.

1. 새 v2 packet 하나를 prepare한다.
2. `inspect-packet`에서 `ready`를 확인한다.
3. fresh context에서 generation을 실행한다.
4. prompt 변경, 추가 지시, repair를 하지 않는다.
5. generation이 끝난 뒤 controlled build를 정확히 한 번 실행한다.
6. `evidence/build.txt`의 pinned target, SDK, harness command, source-state digest, exit code를 확인한다.
7. build 후 `project/` source를 수정하지 않는다.
8. RUN Build command/result와 verification build 항목을 evidence와 일치시킨다.
9. 실제로 수행한 render/theme/scaling/input/accessibility evidence를 작성한다.
10. `inspect-packet`에서 `capture_ready`를 확인한다.
11. repair 없이 capture한다.
12. 다음 새 packet으로 이동한다.

예시:

```powershell
python scripts/evaluation_harness.py prepare --condition baseline --scenario connection-settings --destination evaluation/.runs/v2/baseline/connection-settings
python scripts/evaluation_harness.py inspect-packet --packet evaluation/.runs/v2/baseline/connection-settings --condition baseline --scenario connection-settings
python scripts/evaluation_harness.py build --packet evaluation/.runs/v2/baseline/connection-settings
python scripts/evaluation_harness.py inspect-packet --packet evaluation/.runs/v2/baseline/connection-settings --condition baseline --scenario connection-settings
python scripts/evaluation_harness.py capture --packet evaluation/.runs/v2/baseline/connection-settings --destination evaluation/baseline/connection-settings
```

Pinned project가 삭제된 경우 build CLI는 exit 2이며, verification build status는 `fail`, RUN Build result는 실제 dotnet exit code를 기록한다. helper JSON 출력의 `exit_code` 값을 사용한다.

6개 capture 완료 후:

```powershell
python scripts/evaluation_harness.py validate-results --root evaluation
```

이 명령이 pass하기 전에는 scoring을 시작하지 않는다.

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
