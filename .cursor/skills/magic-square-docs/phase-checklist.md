# Phase Checklist — magic-square-docs Export

**Export 요청 시 magic-square-docs Skill 로드 후 본 checklist 수행.**

`/export-session` 또는 Report Export 요청 시 **순서대로** 체크. 미충족 시 해당 Step에서 중단.

**SSOT:** `.cursorrules`, `docs/PRD.md`, `.cursor/commands/export-session.md`

## Step A — 입력 수집

- [ ] `git status` 실행 (또는 채팅에 이미 있는 결과 사용)
- [ ] `python -m pytest tests/ -v` 실행 — **채팅에 없는 결과는 추측 기록 금지**
- [ ] 채팅에서 **Phase** 선언 추출 (`red` / `green` / `refactor` / `repeat`)
- [ ] **Test ID**·RED 묶음 (TDD 세션일 때)
- [ ] 실행된 **Command** 목록 (`/red-test-plan`, `/green-minimal` 등)
- [ ] 세션 주제·산출물 파일 (대화 확정만)

## Step B — 세션 번호 NN

- [ ] `Report/`에서 `^\d{2}\.` 파일 최대값 확인
- [ ] `Prompting/`에서 `^\d{2}\.` 파일 최대값 확인
- [ ] `NN = max(Report, Prompting) + 1` (없으면 `01`)
- [ ] 동일 NN 경로 **덮어쓰기 금지** — 충돌 시 NN 재계산

## Step C — Report

- [ ] [report-template.md](report-template.md) 기준 `Report/{NN}.REPORT.md` 생성
- [ ] Phase에 맞는 STEP 섹션만 포함 (RED / GREEN / REFACTOR / repeat)
- [ ] pytest·git은 **Step A 실측값**만
- [ ] 레거시 `Report/STEP*_*.md`는 링크만 (삭제·덮어쓰기 금지)

## Step D — Transcript

- [ ] [transcript-template.md](transcript-template.md) 기준 `Prompting/{NN}.Export-Transcript.md` 생성
- [ ] User / Cursor 턴 요약
- [ ] `_Exported on` · `_Source` uuid (채팅·transcript에서 확보 가능할 때만)
- [ ] Report와 상호 링크

## Step E — README 갱신

- [ ] `Prompting/README.md` 표에 NN 행 추가
- [ ] `Report/README.md` 있으면 동일 NN 행 추가 (없으면 생성)

## Step F — 완료 보고

- [ ] 응답에 **경로 2개** 명시:
  - `Report/{NN}.REPORT.md`
  - `Prompting/{NN}.Export-Transcript.md`
- [ ] 세션 주제 한 줄

## 금지 (전 Step 공통)

- [ ] git commit (사용자 미요청)
- [ ] `UPDATE_GOLDEN=1` (사용자 미요청)
- [ ] 채팅·터미널에 없는 pytest 결과 기재
- [ ] `src/`·`tests/`·`.cursorrules` 무관 수정
