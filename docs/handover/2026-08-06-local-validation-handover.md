# LazyDesign 로컬 검증 및 평가 작업 Handover

작성 시각: 2026-08-06 16:12 KST

## 1. 작업 목적

이 저장소는 AI 에이전트가 WinUI 3 XAML을 생성할 때 반복적으로 발생하는 작은 UI 결함을 줄이기 위한 source-backed 컴포넌트 레퍼런스다.

현재 목표는 전체 정밀 버전을 바로 확장하는 것이 아니라, 먼저 8개 대표 컴포넌트와 5개 공통 foundation으로 구성된 `v0.1-candidate`가 실제 에이전트 출력 품질을 개선하는지 통제된 baseline/guided 실험으로 검증하는 것이다.

전체 정밀 범위 확장은 품질 게이트를 통과한 뒤에만 진행한다.

## 2. 저장소와 작업 위치

- GitHub 저장소: `lazyant91/LazyDesign`
- 로컬 작업공간: `Z:\workspace\LazyDesign`
- 기본 브랜치: `main`
- 작업 브랜치: `docs/initial-reference-design`
- 작업 브랜치의 handover 작성 전 SHA: `c2973bb06caec2a85bec0400f75a80dd96aa8731`
- Draft PR: `#1` — `docs: prepare WinUI component reference v0.1 candidate`
- PR base: `main`
- PR 상태: open, Draft, handover 작성 전 `mergeable: true`
- 기본 브랜치 기준 시작 SHA: `98429e86192e96e9a30afc97361d03b7adf5242a`

다음 세션은 위 SHA를 맹목적으로 checkout하지 말고, 실제 원격 branch head와 로컬 상태를 먼저 확인해야 한다. 이 handover 파일 추가로 원격 head는 위 SHA보다 한 커밋 앞선다.

## 3. 반드시 먼저 읽을 규칙

Remote를 통한 로컬 작업을 시작하기 전에 다음 파일을 실제 디스크에서 직접 읽는다.

1. `C:\Users\lky57\.wgpt\AGENTS.md`
2. `Z:\workspace\LazyDesign\AGENTS.md`
3. 작업 대상 하위 디렉터리에 추가 `AGENTS.md`가 있는지 확인하고, 있으면 해당 파일도 읽는다.

과거 세션에서 읽었다는 사실이나 저장소에 파일이 존재한다는 사실만으로 규칙을 적용했다고 간주하지 않는다.

주요 전역 제한:

- 로컬 Codex CLI를 직접 또는 우회 실행하지 않는다.
- 사용자가 명시적으로 승인하지 않은 subagent나 병렬 에이전트를 사용하지 않는다.
- GitHub Actions를 추가하지 않는다.
- `git reset --hard`, `git clean`, 강제 checkout/restore, 강제 push를 하지 않는다.
- 기존 변경과 추적되지 않은 파일을 임의 삭제하거나 덮어쓰지 않는다.
- 기본 브랜치에 직접 커밋하지 않는다.
- Pull Request를 사용자 승인 없이 병합하지 않는다.
- 임시 파일, 캐시, 평가 프로젝트, 로그는 `Z:\workspace\LazyDesign` 내부에 둔다.

## 4. 로컬 시작 절차

### 4.1 작업공간 존재 여부 확인

```powershell
Test-Path 'Z:\workspace\LazyDesign'
Get-ChildItem 'Z:\workspace\LazyDesign' -Force -ErrorAction SilentlyContinue
```

기존 디렉터리가 있으면 그 내용을 보존한다. 출처가 불분명한 파일이 있거나 Git 저장소가 아닌 경우 임의 삭제하거나 그 위에 clone하지 않는다.

디렉터리가 없을 때만 다음처럼 clone한다.

```powershell
git clone https://github.com/lazyant91/LazyDesign.git Z:\workspace\LazyDesign
```

### 4.2 규칙 파일 직접 읽기

```powershell
Get-Content 'C:\Users\lky57\.wgpt\AGENTS.md' -Raw
Set-Location 'Z:\workspace\LazyDesign'
Get-Content '.\AGENTS.md' -Raw
Get-ChildItem -Path . -Filter AGENTS.md -Recurse -Force
```

### 4.3 Git 상태 보호 점검

```powershell
Set-Location 'Z:\workspace\LazyDesign'
git remote -v
git remote show origin
git symbolic-ref refs/remotes/origin/HEAD
git branch --show-current
git rev-parse HEAD
git status --short --branch
git worktree list
git log --oneline --decorate -12
```

확인할 내용:

- 실제 원격 저장소가 `lazyant91/LazyDesign`인지
- `origin/HEAD`가 실제로 어떤 브랜치를 가리키는지
- 현재 브랜치와 upstream
- 현재 HEAD SHA
- 기존 변경과 추적되지 않은 파일
- 다른 worktree 또는 다른 세션의 작업 흔적

작업 트리가 깨끗하고 충돌 가능성이 없을 때만 원격 상태를 갱신하고 작업 브랜치로 이동한다.

```powershell
git fetch origin --prune
git switch docs/initial-reference-design
git pull --ff-only origin docs/initial-reference-design
```

기존 변경이 있으면 switch, pull, stash, restore를 자동 수행하지 않는다. 상태를 보존하고 충돌 가능성을 먼저 보고한다.

## 5. 현재까지 완료된 범위

### Task 1 — Source lock

`sources/manifest.yaml`에 다음을 기록했다.

- Microsoft Learn 공통 및 8개 컨트롤 문서
- WinUI 3 Gallery `v2.9.3`
- Gallery commit `14a4a1a2b8ddc527dc4a7d5f7e743d7c2bc97db7`
- Gallery 환경: .NET 9, Windows App SDK `2.0.1`, target Windows SDK `10.0.22621.756`
- Windows Design Kit Community file identity `1440832812269040007`

Windows Design Kit은 파일 identity만 확인됐다. component-level inspection은 아직 수행되지 않았으며, 현재 모든 `ui-kit` evidence는 비활성이다.

### Task 2 — 문서 계약 및 구조 검사기

- `docs/templates/component-reference.md`
- `docs/templates/source-note.md`
- `scripts/check_reference.py`
- component/foundation 인덱스

구조 검사기는 8개 component, 5개 foundation, 필수 섹션, source ID, 미해결 authoring marker를 검사하도록 작성됐다.

### Task 3 — 공통 foundation 5개

- `foundations/text-and-localization.md`
- `foundations/sizing-and-spacing.md`
- `foundations/icons.md`
- `foundations/states-and-themes.md`
- `foundations/accessibility-basics.md`

### Tasks 4–7 — 컴포넌트 8개

- `components/button.md`
- `components/textbox.md`
- `components/toggleswitch.md`
- `components/combobox.md`
- `components/commandbar.md`
- `components/listview.md`
- `components/infobar.md`
- `components/contentdialog.md`

모든 컴포넌트와 foundation의 현재 상태는 `v0.1-candidate`다. 이는 문서 후보가 준비됐다는 의미이며 build, render, theme, keyboard, accessibility 검증을 통과했다는 의미가 아니다.

### Task 8 — 고정 평가 하네스

- `evaluation/README.md`
- `evaluation/rubric.md`
- `evaluation/prompts/connection-settings.md`
- `evaluation/prompts/device-list.md`
- `evaluation/prompts/failure-confirmation.md`

평가 규칙:

- baseline과 guided는 같은 모델 계열과 reasoning level 사용
- 각 실행은 fresh context
- 동일 prompt bytes
- 동일 시작 프로젝트 SHA
- 동일 tool/network 조건
- 실행 중 prompt 수정이나 결과 수리 금지
- 실패 결과도 보존
- static/build/render/theme/input/accessibility 증거를 분리 기록

## 6. 로컬에서 가장 먼저 실행할 검증

다음 명령은 이전 세션에서 실제 현재 branch checkout을 대상으로 실행하지 못했다. 이번 세션에서 가장 먼저 실행한다.

```powershell
Set-Location 'Z:\workspace\LazyDesign'
python scripts/check_reference.py
python -m py_compile scripts/check_reference.py
git diff --check
git grep -n "TBD\|TODO\|<RULE-ID>\|<SOURCE-ID>\|<ControlName>" -- components foundations sources evaluation
```

예상 결과:

- `python scripts/check_reference.py`: exit code 0
- `python -m py_compile scripts/check_reference.py`: exit code 0
- `git diff --check`: exit code 0
- placeholder grep: 출력 없음

예상과 다르면 결과를 숨기거나 우회하지 않는다. 원인을 조사하고 필요한 최소 수정만 같은 작업 브랜치에서 수행한다.

추가 수동 검토:

```powershell
git grep -n "ControlTemplate" -- components foundations
```

`ControlTemplate`은 설명이나 common failure에서만 나타나야 하며 minimal native XAML 예제에 실제 custom template이 들어가면 안 된다.

## 7. 다음 핵심 작업: Tasks 9–11

상세 절차의 기준 문서는 다음 파일이다.

`docs/superpowers/plans/2026-08-06-winui3-component-reference-v0.1.md`

계획서 내용을 임의 단축하거나 실험 조건을 변경하지 않는다.

### Task 9 — Baseline 조건 생성

1. 최소 WinUI 3 평가 프로젝트를 만든다.
2. 정확한 시작 프로젝트 snapshot SHA를 기록한다.
3. LazyDesign 파일을 평가 프로젝트나 baseline context에 넣지 않는다.
4. 세 prompt를 각각 fresh context에서 원문 그대로 실행한다.
5. 실행 중 prompt 보완, 코드 수정, 빌드 오류 수리 금지.
6. 생성 결과가 실패해도 그대로 보존한다.
7. 각 시나리오에 `PROMPT.md`, `RUN.md`, 생성물을 저장한다.

필수 `RUN.md` 정보:

- 실행 날짜와 시각
- 모델 식별자
- reasoning level
- 시작 프로젝트 SHA
- tool 및 network 접근 조건
- 개입 없이 생성이 끝났는지
- 생성 파일 목록
- build 명령과 결과
- 실제 수행한 render/theme/input/accessibility 검증

경로:

- `evaluation/baseline/connection-settings/`
- `evaluation/baseline/device-list/`
- `evaluation/baseline/failure-confirmation/`

### Task 10 — Guided 조건 생성

동일한 시작 프로젝트 SHA와 prompt를 사용한다. 유일한 실험 차이는 관련 LazyDesign 문서 제공 여부다.

Scenario A 제공 파일:

```text
DESIGN.md
foundations/text-and-localization.md
foundations/sizing-and-spacing.md
foundations/states-and-themes.md
foundations/accessibility-basics.md
components/button.md
components/textbox.md
components/toggleswitch.md
components/combobox.md
```

Scenario B 제공 파일:

```text
DESIGN.md
foundations/text-and-localization.md
foundations/sizing-and-spacing.md
foundations/icons.md
foundations/states-and-themes.md
foundations/accessibility-basics.md
components/button.md
components/commandbar.md
components/listview.md
```

Scenario C 제공 파일:

```text
DESIGN.md
foundations/text-and-localization.md
foundations/sizing-and-spacing.md
foundations/icons.md
foundations/states-and-themes.md
foundations/accessibility-basics.md
components/button.md
components/infobar.md
components/contentdialog.md
```

관련 없는 component 문서를 추가로 제공하지 않는다.

경로:

- `evaluation/guided/connection-settings/`
- `evaluation/guided/device-list/`
- `evaluation/guided/failure-confirmation/`

### Task 11 — 점수와 게이트

`evaluation/rubric.md`의 10개 카테고리를 각 0, 1, 2점으로 채점한다.

각 점수는 다음 중 하나를 반드시 포함한다.

- 파일과 줄 번호
- 실제 렌더링 관찰
- build 또는 runtime 증거

생성 파일:

- `evaluation/results/scores.md`
- `evaluation/results/findings.md`
- `evaluation/results/gate-decision.md`

게이트 조건:

1. Guided 총점이 baseline보다 최소 20% 개선
2. clipping/content-overflow 결함이 최소 50% 감소
3. anatomy와 accessibility 누락 감소
4. 불필요한 `ControlTemplate` 교체 증가 없음
5. 무관한 XAML 또는 복잡성의 유의미한 증가 없음
6. 개선이 구체적인 LazyDesign rule ID에 추적 가능

여섯 조건이 모두 통과해야 전체 결과가 `PASS`다.

- PASS: `DESIGN.md` 상태를 `validated-v0.1`로 변경하고 precision expansion 승인 상태를 README에 기록
- FAIL: 상태를 `v0.1-candidate`로 유지하고 정확히 어떤 페이지나 retrieval behavior를 수정해야 하는지 기록

게이트 전에는 새 컨트롤 범위를 추가하지 않는다.

## 8. Windows 로컬 검증 매트릭스

각 baseline/guided 결과에 대해 가능한 검증을 구분해서 기록한다.

### Build

- 실제 WinUI 프로젝트 build 명령
- exit code
- warning/error 요약
- build한 현재 branch와 프로젝트 SHA

### Render와 폭

- Connection Settings: 420 DIP content width
- Device List: 520 DIP content width
- 고정된 한국어와 영어 장문 문자열 clipping/wrapping
- popup, overflow, dialog, InfoBar action 영역

### Theme

- Light
- Dark
- contrast theme / High Contrast

Light/Dark 확인을 contrast theme 확인으로 대체하지 않는다.

### Text scaling과 localization

- text scaling을 실제로 변경한 결과
- 한국어와 영어 문자열
- fixed width/height로 인한 clipping

### Input

- 키보드 탐색
- focus visual
- Enter/Space/Escape 동작
- ComboBox popup, CommandBar overflow, ListView selection, ContentDialog default/close action

### Accessibility

가능한 경우 Accessibility Insights와 Narrator를 사용한다.

확인 항목:

- accessible name
- role
- value/state
- focus order
- selected/checked/expanded/severity 전달
- 색상 외 상태 단서

실행하지 못한 항목은 `not run`으로 기록한다. build 성공을 rendered/accessibility 검증 성공으로 표현하지 않는다.

## 9. Task 12 — 최종 리뷰 및 PR 준비

Tasks 9–11이 끝난 뒤에만 수행한다.

검토 항목:

- 모든 source ID가 manifest에 존재하며 규칙 문구를 실제로 뒷받침하는지
- 모든 `derived` 규칙이 추론임을 설명하는지
- WPF, UWP, MAUI, Qt, web, Android, iOS 규칙이 들어오지 않았는지
- resolver, adapter, custom control library, static analyzer가 추가되지 않았는지
- Gallery source tree나 Microsoft 문서/이미지를 대량 복사하지 않았는지
- GitHub Actions가 추가되지 않았는지

최종 명령:

```powershell
python scripts/check_reference.py
python -m py_compile scripts/check_reference.py
git diff --check
git grep -n "TBD\|TODO" -- README.md DESIGN.md components foundations evaluation sources
git status --short
git log --oneline --decorate -12
```

모든 결과를 실제 current SHA에서 실행하고 읽은 뒤에만 완료 또는 통과를 주장한다.

PR은 계속 Draft로 유지한다. 사용자 승인 없이 Ready 전환, merge, branch 삭제를 하지 않는다. 병합 승인을 받은 경우에만 Ready로 바꾸고 squash merge를 사용한다.

## 10. 알려진 제한과 위험

- Windows Design Kit component-level inspection 미완료
- `ui-kit` evidence 비활성
- 이전 세션에서는 Remote developer MCP 접근 불가
- public GitHub clone도 DNS 제한으로 실패해 실제 branch에서 Python checker를 실행하지 못함
- baseline/guided 생성물과 점수는 아직 없음
- WinUI build/render/theme/accessibility 결과도 아직 없음
- PR의 많은 작은 커밋은 GitHub Contents API 작업에서 생긴 것이며 최종 병합 시 squash merge가 적절함

## 11. 완료 보고 형식

로컬 작업 완료 보고에 반드시 포함한다.

- 저장소와 로컬 작업공간
- 작업 브랜치
- 시작 SHA와 최종 SHA
- 주요 변경 파일과 목적
- 실행한 명령
- build/test/static/render/theme/input/accessibility별 결과
- 실패하거나 건너뛴 검증
- baseline/guided 모델, reasoning level, 시작 프로젝트 SHA
- 시나리오별 점수와 총점
- 게이트 6개 조건별 pass/fail
- 알려진 제한과 남은 위험
- 최종 `git status --short`
- PR 상태

## 12. 다음 세션 시작 요청 예시

```text
@Remote
Z:\workspace\LazyDesign에서 LazyDesign v0.1 작업을 이어서 진행해줘.
먼저 C:\Users\lky57\.wgpt\AGENTS.md와 저장소 AGENTS.md를 실제 파일에서 읽고,
remote, origin/HEAD, 현재 브랜치, HEAD SHA, status, worktree를 확인해.
docs/handover/2026-08-06-local-validation-handover.md와
v0.1 실행 계획을 읽은 뒤, 기존 변경을 보존하면서 로컬 구조 검증부터 실행하고 Tasks 9–12를 순서대로 진행해.
GitHub Actions, subagent, 로컬 Codex CLI는 사용하지 말고 PR은 병합하지 마.
```
