# Transcript Template — `Prompting/{NN}.Export-Transcript.md`

SSOT 형식: `Prompting/05.Export-Transcript.md` 스타일.

```markdown
# MagicSquare_xx — 세션 {NN} Export Transcript

{세션 주제 한 줄 — Report와 동일}

**관련 보고서:** [Report/{NN}.REPORT.md](../Report/{NN}.REPORT.md)

---

## 메타

| 항목 | 값 |
|------|-----|
| 세션 | {NN} |
| Phase | {red \| green \| refactor \| repeat} |
| _Exported on_ | {YYYY-MM-DD HH:MM TZ} |
| _Source_ | {uuid — agent transcript jsonl id, 없으면 「미확보」} |

---

## 프롬프트 (재실행용)

\```
/export-session
\```

또는:

\```
Report Export — 세션 {NN} ARRR {Phase} 사이클 정리
\```

---

## 대화 요약 (User / Cursor)

### Turn 1 — User

{사용자 요청·Command 원문 요약}

### Turn 2 — Cursor

{응답·Phase 선언·산출 요약}

### Turn 3 — User

{…}

### Turn N — Cursor

{최종 보고·pytest 실측}

> 전체 대화 복붙이 아닌 **재현 가능한 요약**. Command·Test ID·파일 경로는 **원문 유지**.

---

## 기대 산출물

| 경로 | 용도 |
|------|------|
| `Report/{NN}.REPORT.md` | 세션 보고서 |
| `Prompting/{NN}.Export-Transcript.md` | 본 파일 |

---

## 확장 프롬프트 (선택)

\```
MagicSquare_xx 세션 {NN}을 재현한다.

Phase: {phase}
Command: {목록}
Test ID: {목록}
산출: Report/{NN}.REPORT.md + Prompting/{NN}.Export-Transcript.md
금지: git commit, UPDATE_GOLDEN, 추측 pytest
\```

---

## Command·Phase 타임라인

| 순서 | Command / 작업 | Phase | 결과 |
|------|----------------|-------|------|
| 1 | `/red-test-plan` | red | 설계표 |
| 2 | `/red-skeleton` | red | pytest.fail |
| 3 | `/green-minimal` | green | PASS |
| 4 | `/refactor-smell` | refactor | 스멜 표 |
| 5 | `/refactor-safe` | refactor | safe 1건 |
| 6 | `/golden-master` | green | golden 고정 |
| 7 | `/export-session` | repeat | 본 Export |

{실제 실행된 행만 기입}

---

*Exported for MagicSquare_xx session {NN}. _Source: {uuid}*
```

## _Source uuid 확보

1. Cursor agent transcript 경로에 uuid가 있으면 기록.
2. 채팅에 없으면 `_Source: 미확보` — **추측 금지**.

## User / Cursor 규칙

- 턴 헤더: `### Turn N — User` / `### Turn N — Cursor`
- Cursor 턴에 `Phase:` 선언이 있으면 **인용**
- pytest는 **실행 로그 인용**만
