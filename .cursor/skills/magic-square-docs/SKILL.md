---
name: magic-square-docs
description: >-
  MagicSquare_xx session documentation: numbered Report and Export Transcript
  after ARRR TDD cycles. Use for Report Export, Transcript, /export-session,
  Phase repeat, ARRR 1-cycle completion reports, or session N reports.
disable-model-invocation: true
---

# magic-square-docs

MagicSquare_xx **세션 보고서·Transcript Export** Skill.

**Export 요청 시 magic-square-docs Skill 로드 후 [phase-checklist.md](phase-checklist.md) 수행.**

**언어:** 한국어.

**SSOT:** `.cursorrules` → `docs/PRD.md` → 채팅 실측. **형식:** `Report/{NN}.REPORT.md`, `Prompting/{NN}.Export-Transcript.md`

레거시 `Report/STEP*_*.md`, `Prompt/STEP*_*.md`는 유지·링크만. 신규 Export는 **NN 번호 체계** 우선.

---

## 연동 Command

| Command | 역할 |
|---------|------|
| `/export-session` | 본 Skill + checklist → Report + Transcript 2건 |
| `/export-report` | 레거시 Report/Prompt (STEP 명명) — NN 체계와 병행 가능 |

`/export-session` 실행 시: **magic-square-docs 로드 → phase-checklist A~F**.

---

## 워크플로 (Step A → F)

### Step A — 입력 수집

터미널·채팅에서 **실측·확정**만 수집.

| 입력 | 수집 방법 |
|------|-----------|
| git status | `git status` 실행 |
| pytest | `python -m pytest tests/ -v` 실행 |
| Phase | 채팅 `Phase:` 첫 줄 (`red`/`green`/`refactor`/`repeat`) |
| Test ID | `/red-test-plan`·보고 블록·`T-*` |
| Command | `/red-test-plan`, `/red-skeleton`, `/green-minimal`, … |
| 세션 주제 | 대화 핵심 작업 한 줄 |

**금지:** 채팅·터미널에 없는 pytest 결과 기재.

### Step B — NN 할당

```
NN = max(Report/, Prompting/ 의 \d{2}. 접두 파일 번호) + 1
```

- 예: `04.REPORT.md` + `04.Export-Transcript.md` 존재 → **NN = 05**
- 번호 파일 없음 → **NN = 01**
- 산출 경로:
  - `Report/{NN}.REPORT.md`
  - `Prompting/{NN}.Export-Transcript.md`
- **동일 NN 덮어쓰기 금지** — 충돌 시 NN 증가

NN 파싱 예 (PowerShell):

```powershell
Get-ChildItem Report, Prompting -ErrorAction SilentlyContinue |
  Where-Object { $_.Name -match '^\d{2}\.' } |
  ForEach-Object { [int]$_.Name.Substring(0,2) } |
  Measure-Object -Maximum
```

### Step C — Report

[report-template.md](report-template.md)를 채워 `Report/{NN}.REPORT.md` 생성.

**Phase별 STEP** (해당만):

| Phase | STEP |
|-------|------|
| `red` | STEP RED — C2C, RED 묶음, FAIL pytest |
| `green` | STEP GREEN — 묶음 PASS, 최소 구현 |
| `refactor` | STEP REFACTOR — 스멜, safe, golden |
| `repeat` | STEP REPEAT — ARRR 1사이클 완료 요약 |

섹션 **0. 게이트**에 Step A의 git·pytest **실측** 필수.

### Step D — Transcript

[transcript-template.md](transcript-template.md)로 `Prompting/{NN}.Export-Transcript.md` 생성.

- **User / Cursor** 턴 요약 (`### Turn N — User|Cursor`)
- **`_Exported on`**: Export 시각 (오늘 날짜·시간)
- **`_Source`**: agent transcript uuid (있을 때만; 없으면 `미확보`)
- Report와 **상호 링크**

### Step E — README 문서 표 갱신

`Prompting/README.md` (없으면 생성) 세션 표에 행 추가:

```markdown
| {NN} | [{NN}.REPORT.md](../Report/{NN}.REPORT.md) | [{NN}.Export-Transcript.md](./{NN}.Export-Transcript.md) | {주제} | {Phase} |
```

`Report/README.md` 동일 NN 행 추가 (선택·권장).

레거시 `Prompt/README.md`는 **삭제하지 않음** — NN 체계 섹션 링크만 추가 가능.

### Step F — 완료 보고

응답 **반드시 경로 2개**:

```
Report/{NN}.REPORT.md
Prompting/{NN}.Export-Transcript.md
```

+ 세션 주제 한 줄 + Phase.

예:

```
세션 05 Export 완료 — ARRR 1사이클 (red→green→refactor)

- Report/05.REPORT.md
- Prompting/05.Export-Transcript.md
```

---

## ARRR 1사이클 완료 보고 (Phase: repeat)

`Phase: repeat` 또는 사용자가 「ARRR 1사이클 완료」 시:

1. Step A에서 **사이클 전체** Command·Test ID 수집
2. Report **STEP REPEAT** + RED/GREEN/REFACTOR **요약 표** 1개
3. Transcript **Command·Phase 타임라인** 표 채움
4. 다음 사이클 첫 Command 제안 (대화 확정만)

---

## 세션 N 보고서

「세션 N 보고서」= `Report/{NN}.REPORT.md` (NN은 Step B 규칙).  
N을 사용자가 지정했으면 해당 NN이 **비어 있을 때만** 작성; occupied면 `-v2` 대신 **다음 NN** 사용.

---

## 금지

| 금지 | 이유 |
|------|------|
| **git commit** (사용자 미요청) | `.cursorrules` |
| **`UPDATE_GOLDEN=1`** (사용자 미요청) | golden 정책 |
| 채팅에 없는 **pytest 결과** | 실측만 |
| 기존 NN 파일 **덮어쓰기** | 세션 이력 |
| `src/`·`tests/`·`.cursorrules` 수정 | Export 범위 밖 |
| 대화 없는 내용 **추측** | SSOT |

---

## 템플릿·체크리스트

| 파일 | 용도 |
|------|------|
| [report-template.md](report-template.md) | `Report/{NN}.REPORT.md` |
| [transcript-template.md](transcript-template.md) | `Prompting/{NN}.Export-Transcript.md` |
| [phase-checklist.md](phase-checklist.md) | Export 전 체크 |

---

## TDD Skill 교차 참조

TDD 세션 Report에 Phase·Test ID·pytest가 있으면 [.cursor/skills/magic-square-tdd/SKILL.md](../magic-square-tdd/SKILL.md) 보고 형식과 **정합** 유지.

| TDD Phase | Report STEP |
|-----------|---------------|
| red | STEP RED |
| green | STEP GREEN |
| refactor | STEP REFACTOR |

---

## 레거시 vs NN 체계

| 체계 | Report | Export |
|------|--------|--------|
| **NN (본 Skill)** | `Report/05.REPORT.md` | `Prompting/05.Export-Transcript.md` |
| **레거시** | `Report/STEP3_*_Report.md` | `Prompt/STEP3_*_Export.md` |

신규 `/export-session` → **NN 체계**. `/export-report` → 레거시 명명 허용.

---

## Quick Reference — Phase 선언

```
Phase: red | Layer: entity | Track: Logic
Phase: green | Layer: entity | Track: Logic
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI
Phase: repeat | Session: {NN} | Track: Logic+UI
```

Export Report 메타 테이블에 **인용**.
