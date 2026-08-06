# LazyDesign 평가 packet v2 및 preflight Handover

작성 시각: 2026-08-06 20:53 KST

## 1. 저장소 상태

- GitHub 저장소: `lazyant91/LazyDesign`
- 로컬 작업공간: `Z:\workspace\LazyDesign`
- 작업 브랜치: `docs/initial-reference-design`
- 이 문서 작성 직전 HEAD: `a1630ee748a2fe6953566589d5f41d0e1be59022`
- upstream: `origin/docs/initial-reference-design`
- 기본 브랜치: `origin/main`
- 시작 프로젝트 snapshot commit: `b73babad19d0153707a49e5ba1ed9fb0a42c33ef`
- prompt/reference input commit: `7d01aae3cdc0241a7aa7ede7ee09738a6d5ee7cc`
- Draft PR: `#1`
- PR base/head: `main <- docs/initial-reference-design`

다음 세션은 위 HEAD를 가정하지 말고 remote, `origin/HEAD`, branch, upstream, HEAD, status, worktree를 실제로 다시 확인한다. 기존 변경과 추적되지 않은 파일은 보존하고 switch, stash, restore, reset, clean을 자동 수행하지 않는다.

이번 세션에서는 `C:\Users\lky57\.wgpt\AGENTS.md`를 실제 파일에서 읽었다. 내용은 Stitch 작업용 공용 규칙이며 현재 평가 harness 작업에는 추가 Stitch 절차가 필요하지 않았다. 저장소 `AGENTS.md`도 다시 읽었고 하위 `AGENTS.md`는 없었다.

## 2. 이번 세션의 커밋

### a1630ee — packet v2 및 preflight

변경 파일:

- `scripts/evaluation_harness.py`
- `tests/test_evaluation_harness.py`
- `evaluation/README.md`
- `docs/superpowers/plans/2026-08-06-winui3-component-reference-v0.1.md`

### 계약 버전

- `PACKET.json` contract: `schema_version: 2`
- `CAPTURE.json` contract: `schema_version: 2`

Packet v2는 다음 필드를 정확히 요구한다.

```text
schema_version
condition
scenario
input_commit
start_project_commit
start_project_path
content_width_dip
prompt_path
prompt_sha256
references
project_files
```

Capture v2는 다음 필드를 정확히 요구한다.

```text
schema_version
condition
scenario
prompt_sha256
packet_sha256
run_sha256
generated_files
deleted_files
evidence_files
```

Packet 필드 집합 또는 schema version이 현재 계약과 다르면 깊은 검증을 진행하지 않고 명확한 contract 오류만 반환한다.

## 3. Packet preflight

단일 packet 검사:

```powershell
python scripts/evaluation_harness.py inspect-packet --packet <packet-path> --condition baseline|guided --scenario connection-settings|device-list|failure-confirmation
```

전체 root 검사:

```powershell
python scripts/evaluation_harness.py inspect-packets --root <packet-root>
```

상태:

- `missing`: 예상 packet directory가 없음
- `stale`: schema, 필드, 고정 입력 또는 template 계약이 무효
- `ready`: 현재 계약의 clean packet이며 실행 흔적 없음
- `in_progress`: 계약은 유효하지만 generated change, build artifact, RUN metadata 또는 evidence가 아직 capture-ready가 아님
- `capture_ready`: `RUN.md`와 `verification.json`이 완전하고 capture 조건을 충족

단일 검사는 `stale` 또는 `missing`일 때 exit 1, 그 외 exit 0이다. 전체 검사는 하나라도 `stale` 또는 `missing`이면 exit 1이다. 두 명령 모두 packet을 수정하지 않는다.

Inspection은 다음 activity도 기록한다.

- project files changed
- build artifacts present
- RUN.md present
- verification.json present
- additional evidence present

## 4. 현재 보존 중인 v1 packet

현재 ignored 경로에 이전 세션에서 생성된 6개 v1 packet이 존재한다.

```text
evaluation/.runs/baseline/connection-settings
evaluation/.runs/baseline/device-list
evaluation/.runs/baseline/failure-confirmation
evaluation/.runs/guided/connection-settings
evaluation/.runs/guided/device-list
evaluation/.runs/guided/failure-confirmation
```

실행 결과:

```powershell
python scripts/evaluation_harness.py inspect-packets --root evaluation/.runs
```

요약:

```text
ready: 0
in_progress: 0
capture_ready: 0
stale: 6
missing: 0
exit: 1
```

모든 packet은 다음 이유로 stale이다.

```text
packet must contain exactly the current contract fields
packet schema_version must be 2
```

추가 activity:

- baseline/connection-settings: project files changed, build artifacts present
- 나머지 5개: project files changed

이 packet들은 사용자 또는 이전 세션 작업 흔적일 수 있으므로 삭제, 이동, 수정, migration하지 않았다. 실제 평가에 재사용하지 않는다.

## 5. 다음 실제 packet root

실제 6개 fresh-context 실행은 새 root를 사용한다.

```text
evaluation/.runs/v2
```

각 run 직전에 해당 packet 하나만 새로 만든다. 예시:

```powershell
python scripts/evaluation_harness.py prepare --condition baseline --scenario connection-settings --destination evaluation/.runs/v2/baseline/connection-settings
python scripts/evaluation_harness.py inspect-packet --packet evaluation/.runs/v2/baseline/connection-settings --condition baseline --scenario connection-settings
```

생성 전 inspection은 `ready`여야 한다. 생성과 검증을 완료한 뒤 다시 실행했을 때 `capture_ready`여야 capture한다.

```powershell
python scripts/evaluation_harness.py capture --packet evaluation/.runs/v2/baseline/connection-settings --destination evaluation/baseline/connection-settings
```

Guided run도 동일하게 `evaluation/.runs/v2/guided/<scenario>`를 사용한다.

v1 packet을 v2로 수동 변환하거나 누락 필드를 추가해 재사용하지 않는다. v2 packet은 `prepare` 명령으로 pinned Git objects에서 새로 생성한다.

## 6. 현재 실행기 상태

비밀값은 출력하지 않고 환경변수 존재 여부만 확인했다.

```text
OPENAI_API_KEY_PRESENT=False
AZURE_OPENAI_API_KEY_PRESENT=False
AZURE_OPENAI_ENDPOINT_PRESENT=False
OPENAI_BASE_URL_PRESENT=False
PYTHON_OPENAI_INSTALLED=True
```

`openai` Python package는 설치되어 있지만 인증 정보와 endpoint가 없다. 현재 대화는 LazyDesign reference를 이미 읽었으므로 baseline fresh context로 사용할 수 없다. 로컬 Codex CLI, subagent, 병렬 agent도 프로젝트 지침상 금지되어 있다.

따라서 실제 baseline/guided 결과는 생성하지 않았다.

## 7. 현재 검증 증거

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
- Python tests: **43 passed**
- Python compile: pass
- JSON parse: pass
- WinUI fixture build: warning 0, error 0
- whitespace check: pass

추가 확인:

- fresh v2 packet: `ready`
- source change가 있는 v2 packet: `in_progress`
- 완성된 metadata/evidence가 있는 v2 packet: `capture_ready`
- v1 packet: `stale`
- 단일 inspect CLI: exit 0 및 JSON `ready`
- 전체 matrix root: 정확히 6개 상태 반환

검증 중 생성한 fixture `bin`, `obj`, Python `__pycache__`는 제거했다. 기존 `evaluation/.runs` 아래 v1 packet의 build 산출물은 보존했다.

## 8. 아직 수행되지 않은 핵심 작업

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

실제 결과 6개가 없으므로 `validate-results`는 계속 exit 1이어야 한다.

## 9. 다음 세션 시작 순서

1. agent-home 및 저장소 `AGENTS.md`를 실제 파일에서 읽는다.
2. remote, `origin/HEAD`, branch, upstream, HEAD, status, worktree를 확인한다.
3. 이 handover와 이전 artifact-integrity handover를 읽는다.
4. 현재 SHA에서 static, tests, JSON, build를 다시 실행한다.
5. `python scripts/evaluation_harness.py inspect-packets --root evaluation/.runs`로 v1 packet이 stale인지 재확인하되 수정하지 않는다.
6. 동일 model/reasoning의 fresh-context 실행기를 확보한 경우에만 `evaluation/.runs/v2` 아래에서 run 하나씩 준비한다.
7. 각 packet을 생성 전 `ready`, capture 전 `capture_ready`로 확인한다.
8. 모든 run을 repair 없이 capture한다.
9. `validate-results`를 통과시킨다.
10. 실제 `metrics.json`을 작성하고 세 보고서를 생성한다.
11. gate 결과에 따라 README와 DESIGN 상태를 갱신한다.
12. PR은 Draft로 유지하고 사용자 승인 없이 Ready 전환 또는 merge하지 않는다.

## 10. 범위와 환경 제한

- Windows Design Kit component-level inspection 미완료
- `ui-kit` evidence 비활성
- gate 전 신규 component 범위 추가 금지
- GitHub Actions 추가 금지
- resolver, adapter, custom control library, static analyzer 추가 금지
- 기존 v1 packet 삭제 또는 migration 금지
- 현재 reference 문서를 UI-kit evidence로 승격하지 않음

Narrator 실행 파일은 이전 세션에서 발견됐지만 실제 Narrator 검증은 수행하지 않았다. Accessibility Insights는 일반 설치 경로에서 발견되지 않았다. 실제 run에서는 해당 항목을 `not_run`과 구체적인 사유로 기록한다.
