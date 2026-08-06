# LazyDesign 로컬 런타임 준비 상태 및 SDK 통제 Handover

작성 시각: 2026-08-06 21:53 KST

## 1. 저장소 상태

- GitHub 저장소: `lazyant91/LazyDesign`
- 로컬 작업공간: `Z:\workspace\LazyDesign`
- 작업 브랜치: `docs/initial-reference-design`
- 이 문서 작성 직전 HEAD: `ee9e067f29cc186de1c1766c6de206fcf7d67a00`
- upstream: `origin/docs/initial-reference-design`
- 기본 브랜치: `origin/main`
- 시작 프로젝트 snapshot commit: `b73babad19d0153707a49e5ba1ed9fb0a42c33ef`
- prompt/reference input commit: `7d01aae3cdc0241a7aa7ede7ee09738a6d5ee7cc`
- Draft PR: `#1`
- PR base/head: `main <- docs/initial-reference-design`

다음 세션은 위 HEAD를 가정하지 말고 remote, `origin/HEAD`, branch, upstream, HEAD, status, worktree를 실제로 다시 확인한다. 기존 변경과 추적되지 않은 파일을 보존하고 자동 switch, stash, restore, reset, clean을 수행하지 않는다.

이번 세션에서는 다음 지침을 실제 파일에서 읽었다.

- `C:\Users\lky57\.wgpt\AGENTS.md`
- `Z:\workspace\LazyDesign\AGENTS.md`

Stitch 요청이 아니므로 Stitch 전용 절차는 실행하지 않았다.

## 2. 이번 세션의 핵심 발견

### 저장소 루트 build는 fixture SDK를 사용하지 않음

실제 확인 결과:

```text
저장소 루트 dotnet --version: 10.0.302
저장소 루트에서 project path를 지정한 MSBuild SDK: 10.0.302
fixture 디렉터리 dotnet --version: 9.0.313
fixture 디렉터리 MSBuild SDK: 9.0.313
```

즉 다음 형식은 fixture 아래 `global.json`을 선택하지 않는다.

```powershell
Set-Location Z:\workspace\LazyDesign
dotnet build evaluation\fixtures\winui-start\LazyDesign.EvaluationApp.csproj
```

`dotnet` SDK 선택은 전달한 project path가 아니라 프로세스 작업 디렉터리에서 탐색한 `global.json`의 영향을 받는다. 기존 루트 기준 build 명령을 실제 평가 evidence로 사용하면 시작 프로젝트에 고정된 SDK 9.0.313이 아니라 10.0.302를 사용할 수 있었다.

## 3. ee9e067 — controlled build SDK 통제

변경 파일:

- `scripts/evaluation_harness.py`
- `tests/test_evaluation_harness.py`
- `evaluation/README.md`
- `docs/superpowers/plans/2026-08-06-winui3-component-reference-v0.1.md`

### Pinned build environment

Harness는 시작 프로젝트 commit의 다음 파일을 Git object에서 직접 읽는다.

```text
evaluation/fixtures/winui-start/global.json
evaluation/fixtures/winui-start/LazyDesign.EvaluationApp.csproj
```

고정 값:

```text
.NET SDK: 9.0.313
Microsoft.WindowsAppSDK: 2.0.1
Microsoft.Windows.SDK.BuildTools: 10.0.26100.4948
```

`RUN.template.md`는 이제 다음 값을 자동으로 채운다.

```text
.NET SDK: 9.0.313
Windows App SDK package: 2.0.1
```

사용자가 저장소 루트의 현재 SDK 값으로 바꾸면 `inspect-packet`, `capture`, `validate-results`가 거부한다.

### Controlled build command

실제 run packet build는 다음 명령만 사용한다.

```powershell
python scripts/evaluation_harness.py build --packet evaluation/.runs/v2/baseline/connection-settings
```

Guided 예시:

```powershell
python scripts/evaluation_harness.py build --packet evaluation/.runs/v2/guided/connection-settings
```

동작:

1. packet v2 계약과 고정 prompt/context/template을 검증한다.
2. 시작 commit의 `global.json`을 작업공간 내부 임시 SDK control 디렉터리에 복원한다.
3. 해당 디렉터리에서 `dotnet --version`이 9.0.313인지 확인한다.
4. packet project를 Debug/x64로 build한다.
5. `evidence/build.txt`에 선택 SDK, package 계약, command, exit code, build 출력을 기록한다.
6. 임시 SDK control 디렉터리를 제거한다.
7. 기존 `evidence/build.txt`는 덮어쓰지 않는다.

Exit code:

- `0`: build 성공
- `2`: build가 실행됐지만 실패
- `1`: packet 또는 pinned build 환경이 무효

Build 실패는 유효한 평가 결과다. exit 2 결과를 repair하지 말고 evidence와 generated output을 그대로 capture한다.

### Build evidence 일치성

Build를 수행한 경우:

- `verification.json`의 `build.status`는 `pass` 또는 `fail`이어야 한다.
- `build.evidence`는 `build.txt`를 참조해야 한다.
- `RUN.md`의 Build command는 `python scripts/evaluation_harness.py build --packet ...` 형식이어야 한다.
- `RUN.md`의 Build result는 `build.txt`의 `exit <code>`와 일치해야 한다.
- build.txt의 expected/selected SDK는 모두 9.0.313이어야 한다.
- 시작 Windows App SDK와 BuildTools 값은 pinned 값과 일치해야 한다.

Build를 수행하지 않은 경우:

- verification `build`는 `not_run`이어야 한다.
- `RUN.md` Build command는 `not performed`여야 한다.
- `RUN.md` Build result는 `not performed`여야 한다.
- `evidence/build.txt`가 존재하면 안 된다.

모순되거나 직접 실행한 root-level build metadata는 capture에서 거부된다.

## 4. 실제 SDK 통제 검증

통합 테스트에서는 새 v2 packet의 `project/global.json`을 다음 값으로 의도적으로 바꿨다.

```json
{"sdk":{"version":"10.0.302"}}
```

그 상태에서 controlled build 결과:

```text
Expected .NET SDK: 9.0.313
Selected .NET SDK: 9.0.313
Starting Windows App SDK package: 2.0.1
Exit code: 0
```

즉 generated output이 packet 안의 `global.json`을 변경해도 scored build 환경은 pinned 시작 SDK를 유지한다. 변경된 `global.json` 자체는 generated file로 capture되어 평가 대상에 포함된다.

CLI smoke도 같은 조건에서 실행했고 exit 0과 동일한 SDK evidence를 확인했다. 임시 smoke packet은 제거했다.

## 5. 로컬 Windows 런타임 준비 상태

점검 시각: 2026-08-06 21:13 KST

### 운영체제와 세션

```text
OS: Microsoft Windows 10 Pro
Version/build: 10.0.19045
Architecture: x64
Session: Console
Explorer interactive desktop: running
PowerShell: 5.1.19041.6456
```

GUI를 표시할 수 있는 콘솔 세션과 Explorer desktop은 존재한다. 이번 세션에서는 평가 app, Narrator 또는 다른 GUI 도구를 실행하지 않았다.

### 개발 환경

```text
Fixture-resolved .NET SDK: 9.0.313
MSBuild: 17.14.43
Microsoft.WindowsAppSDK: 2.0.1
Microsoft.Windows.SDK.BuildTools: 10.0.26100.4948
Target framework: net9.0-windows10.0.22621.0
Target platform minimum: 10.0.17763.0
Architecture: x64
Windows App SDK self-contained: true
```

설치된 Visual Studio:

```text
Visual Studio Community 2026 18.8.12023.21
Visual Studio Community 2022 17.14.37216.2
```

Fixture는 pinned SDK로 build 가능하다.

### 표시 환경

현재 display 설정:

```text
System DPI: 96
Display scale: 100%
Text scale: 100%
Apps theme: Dark
System theme: Dark
High Contrast: disabled
```

화면:

```text
DISPLAY1: 1920x1080, working area 1920x1040, non-primary
DISPLAY2: 2560x1440, working area 2560x1400, primary
```

현재 상태로 Dark/100% 기본 검증은 가능하다. 다음 검증은 실제 run 시 별도로 환경을 변경하고 되돌려야 한다.

- Light theme
- Windows High Contrast theme
- text scale greater than 100%

설정을 바꾸거나 복원하는 작업은 이번 세션에서 수행하지 않았다.

### 언어 환경

```text
User culture: ko-KR
System locale: ko-KR
User language: ko
```

한국어 fixture 표시에는 적합하다. 영어 fixture 문자열은 app content로 직접 제공되므로 별도 OS UI language 전환 없이도 content fit을 검증할 수 있다. OS 언어 전환 검증을 수행했다고 주장해서는 안 된다.

## 6. 접근성 및 관찰 도구

### 즉시 사용 가능한 도구

Narrator:

```text
Path: C:\Windows\System32\Narrator.exe
Version: 10.0.19041.4522
Installed: yes
Executed in this session: no
```

Snipping Tool:

```text
Path: C:\Windows\System32\SnippingTool.exe
Version: 10.0.19041.4522
Installed: yes
Executed in this session: no
```

UI Automation client assemblies:

```text
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\WPF\UIAutomationClient.dll
C:\Windows\Microsoft.NET\Framework\v4.0.30319\WPF\UIAutomationClient.dll
```

UI Automation API assembly는 존재하지만 실제 UI Automation 검증을 수행한 것은 아니다.

### 발견되지 않은 도구

다음 실행 파일 또는 설치 항목은 표준 경로와 설치 레지스트리에서 발견되지 않았다.

```text
AccessibilityInsights.exe
inspect.exe
AccScope.exe
UIAVerify.exe
WinAppDriver.exe
```

따라서 현재 상태에서는 Accessibility Insights check를 수행할 수 없다. 실제 run 전에도 설치하지 않는 경우 `not_run`과 구체적인 사유를 기록한다.

도구 설치는 작업공간 밖의 시스템 상태를 변경하므로 사용자 승인 없이 설치하지 않는다.

## 7. Fresh-context 실행기 상태

비밀값은 출력하지 않고 존재 여부만 확인했다.

```text
OPENAI_API_KEY_PRESENT=False
AZURE_OPENAI_API_KEY_PRESENT=False
AZURE_OPENAI_ENDPOINT_PRESENT=False
OPENAI_BASE_URL_PRESENT=False
Python openai package installed=True
```

현재 대화는 LazyDesign reference를 이미 읽었으므로 baseline fresh context로 사용할 수 없다. 프로젝트 지침에 따라 다음도 사용하지 않는다.

- 로컬 Codex CLI
- subagent
- 병렬 agent

따라서 실제 baseline/guided 생성 6회는 여전히 시작하지 않았다.

## 8. 기존 packet과 결과 상태

이전 v1 packet 6개는 보존 중이며 모두 stale이다.

```text
ready: 0
in_progress: 0
capture_ready: 0
stale: 6
missing: 0
```

실제 v2 run은 새 root만 사용한다.

```text
evaluation/.runs/v2
```

실제 scored result는 아직 없다.

```text
baseline/connection-settings: missing
baseline/device-list: missing
baseline/failure-confirmation: missing
guided/connection-settings: missing
guided/device-list: missing
guided/failure-confirmation: missing
```

`validate-results`는 의도대로 exit 1이다.

## 9. 현재 검증 증거

현재 변경에서 실행:

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
- Python tests: **47 passed**
- Python compile: pass
- JSON parse: pass
- fixture selected SDK: **9.0.313**
- fixture build: warning 0, error 0
- whitespace check: pass
- unresolved `TBD|TODO`: none

검증 중 생성한 fixture `bin`, `obj`, Python cache, SDK control temp directory, CLI smoke packet, runtime audit script는 제거했다.

## 10. 아직 수행되지 않은 핵심 작업

- baseline fresh-context 생성 3회
- guided fresh-context 생성 3회
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

시작 fixture build 성공은 generated scenario runtime 검증으로 간주하지 않는다.

## 11. 다음 실제 실행 순서

동일 model/reasoning의 독립 fresh-context 실행기가 확보된 경우에만 다음을 수행한다.

1. 새 v2 packet 하나를 prepare한다.
2. `inspect-packet`에서 `ready`를 확인한다.
3. 한 fresh context에서 generation을 수행한다.
4. prompt 보완, 중간 조언, repair를 하지 않는다.
5. controlled `build` 명령을 실행한다.
6. `evidence/build.txt`를 확인한다.
7. build verification과 RUN metadata를 일치시킨다.
8. 실제 수행한 render/theme/scaling/input/accessibility evidence를 작성한다.
9. `inspect-packet`에서 `capture_ready`를 확인한다.
10. repair 없이 capture한다.
11. 다음 packet으로 이동한다.

예시:

```powershell
python scripts/evaluation_harness.py prepare --condition baseline --scenario connection-settings --destination evaluation/.runs/v2/baseline/connection-settings
python scripts/evaluation_harness.py inspect-packet --packet evaluation/.runs/v2/baseline/connection-settings --condition baseline --scenario connection-settings
python scripts/evaluation_harness.py build --packet evaluation/.runs/v2/baseline/connection-settings
python scripts/evaluation_harness.py inspect-packet --packet evaluation/.runs/v2/baseline/connection-settings --condition baseline --scenario connection-settings
python scripts/evaluation_harness.py capture --packet evaluation/.runs/v2/baseline/connection-settings --destination evaluation/baseline/connection-settings
```

6개 capture 완료 후:

```powershell
python scripts/evaluation_harness.py validate-results --root evaluation
```

이 명령이 pass하기 전에는 scoring을 시작하지 않는다.

## 12. 범위와 승인 경계

- `DESIGN.md` 상태는 `v0.1-candidate` 유지
- precision expansion 차단 유지
- 신규 component 추가 금지
- GitHub Actions 추가 금지
- resolver, adapter, custom control library, static analyzer 추가 금지
- Windows Design Kit component-level inspection 미완료
- `ui-kit` evidence 비활성
- 기존 v1 packet 수정, 삭제, migration 금지
- Accessibility Insights 또는 SDK 도구 설치는 사용자 승인 전 금지
- GUI app, Narrator, theme, High Contrast, text scaling 변경은 실제 run 절차 외에는 수행하지 않음
- PR은 Draft 유지
- 사용자 승인 없이 Ready 전환 또는 merge 금지
