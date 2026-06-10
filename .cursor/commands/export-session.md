# export-session — ARRR 세션 Report + Transcript Export

**추가 입력 없이 즉시 실행.** 사용자가 `/export-session`만 입력했다.
세션 주제·Phase·Command·산출물은 **현재 채팅 전체**에서 자동 추출한다. 추가 질문·확인 요청 금지.

**역할:** ARRR **Repeat** 단계 — `Report/{NN}.REPORT.md`와 `Prompting/{NN}.Export-Transcript.md` **2건**을 생성한다.

**한국어**로 작성·보고한다.

**Skill:** **magic-square-docs** Skill(`.cursor/skills/magic-square-docs/`)을 **먼저 읽고** [phase-checklist.md](../skills/magic-square-docs/phase-checklist.md) **A~F를 수행**한다.

---

## SSOT

| 우선순위 | 경로 | 용도 |
|----------|------|------|
| 1 | `.cursor/skills/magic-square-docs/` | Export 워크플로·템플릿·체크리스트 |
| 2 | `.cursorrules` | 도메인·TDD·commit 규칙 |
| 3 | `docs/PRD.md` | FR·AC (TDD 세션 인용) |
| 4 | 현재 채팅 | Phase·Test ID·Command·pytest **실측** |

---

## 필수 선언 (응답 첫 줄)

```
Phase: repeat | Session: {NN} | Track: Logic+UI
```

`NN`은 Step B에서 할당. 미할당 시 보고 본문에 확정 NN을 명시한다.

---

## 절차 (magic-square-docs 위임)

Export 요청 시 **magic-square-docs Skill 로드 후 checklist 수행**.

| Step | 내용 |
|------|------|
| **A** | `git status`, `python -m pytest tests/ -v`, Phase, Test ID, Command 수집 |
| **B** | `NN = max(Report/, Prompting/의 \d{2}.) + 1` |
| **C** | [report-template.md](../skills/magic-square-docs/report-template.md) → `Report/{NN}.REPORT.md` |
| **D** | [transcript-template.md](../skills/magic-square-docs/transcript-template.md) → `Prompting/{NN}.Export-Transcript.md` |
| **E** | `Prompting/README.md`·`Report/README.md` 표 갱신 |
| **F** | 경로 2개 + 세션 주제 한 줄 보고 |

Phase별 Report STEP: **RED** / **GREEN** / **REFACTOR** / **repeat** — 채팅 Phase에 맞게만.

---

## 생성 파일 (반드시 2개)

| 파일 | 설명 |
|------|------|
| `Report/{NN}.REPORT.md` | 세션 보고서 (게이트·Phase·산출물) |
| `Prompting/{NN}.Export-Transcript.md` | User/Cursor 요약·재실행 프롬프트 |

**동일 NN 덮어쓰기 금지** — 충돌 시 NN 증가.

---

## 보고 형식

```
Phase: repeat | Session: 01 | Track: Logic+UI

- 주제: {한 줄}
- Report/01.REPORT.md
- Prompting/01.Export-Transcript.md
```

---

## 금지

| 금지 | 이유 |
|------|------|
| 사용자에게 세션 주제·번호 **추가 질문** | 자동 추출 |
| Report·Transcript **한쪽만** 생성 | 2건 필수 |
| 채팅·터미널에 없는 **pytest 결과** | 실측만 |
| **git commit** (사용자 미요청) | `.cursorrules` |
| **`UPDATE_GOLDEN=1`** (사용자 미요청) | golden 정책 |
| `src/`·`tests/`·`.cursorrules` 수정 | Export 범위 밖 |
| 대화 없는 내용 **추측** | SSOT |

---

## 레거시

| Command | 체계 |
|---------|------|
| `/export-session` | `Report/{NN}.REPORT.md` + `Prompting/{NN}.Export-Transcript.md` |
| `/export-report` | `Report/STEP*_*.md` + `Prompt/STEP*_*.md` |

---

## 참고

- Skill: `.cursor/skills/magic-square-docs/SKILL.md`
- TDD 보고 형식: `.cursor/skills/magic-square-tdd/SKILL.md`
- PRD: `docs/PRD.md`
