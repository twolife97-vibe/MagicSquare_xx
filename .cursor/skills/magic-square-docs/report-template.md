# Report Template — `Report/{NN}.REPORT.md`

SSOT 형식: `Report/05.REPORT.md` 스타일. `{NN}` = 두 자리 세션 번호.

```markdown
# MagicSquare_xx — 세션 {NN}: {세션 주제}

| 항목 | 내용 |
|------|------|
| 프로젝트 | MagicSquare_xx (4×4 부분 마방진) |
| 세션 | {NN} |
| Phase | {red \| green \| refactor \| repeat} |
| ARRR | {Ask \| Respond \| Refine \| Repeat} |
| Track | {Logic \| UI \| Logic+UI} |
| 작성일 | {YYYY-MM-DD} |
| Command | {/red-test-plan, /green-minimal, …} |
| Test ID | {T-… 또는 N/A} |
| Transcript | [Prompting/{NN}.Export-Transcript.md](../Prompting/{NN}.Export-Transcript.md) |
| 근거 | {선행 Report · `docs/PRD.md` FR — 없으면 「본 세션 대화」} |

---

## 0. 게이트 (실측)

| 항목 | 결과 |
|------|------|
| git status | {요약 — Step A 실측} |
| pytest | `{python -m pytest tests/ -v}` → {N passed, M failed} |

> 채팅·터미널에 없는 pytest 결과는 **기록하지 않는다**.

---

## 1. 요약

{2~4문장 — 세션 목표·결과·다음 한 줄}

---

## 2. 핵심 결정·산출물

| 구분 | 내용 |
|------|------|
| 결정 | {bullet} |
| 생성·수정 파일 | `{path}` — {용도} |

---

## 3. Phase별 상세 (해당 STEP만)

### STEP RED (Phase: red)

| 항목 | 내용 |
|------|------|
| C2C Rule1~3 | {FR 인용 → To-Do → Test ID G/W/T} |
| RED 묶음 | {Test ID 목록} |
| pytest (RED) | {FAIL — 한 줄, 실측} |
| 변경 | `tests/` only |

### STEP GREEN (Phase: green)

| 항목 | 내용 |
|------|------|
| RED 묶음 | {Test ID} |
| 구현 요약 | {최소 구현 한 줄} |
| pytest (GREEN) | {PASS — 실측} |
| 변경 | `src/` + `tests/` |

### STEP REFACTOR (Phase: refactor)

| 항목 | 내용 |
|------|------|
| 스멜 | {#N P0 …} |
| Safe 변경 | {한 줄} |
| pytest | {N passed — 실측} |
| golden | {matched \| N/A} |
| 변경 | {파일} |

### STEP REPEAT (Phase: repeat)

| 항목 | 내용 |
|------|------|
| ARRR 1사이클 | Ask → Respond → Refine 요약 |
| 누적 Test ID | {목록} |
| 다음 사이클 | {한 줄} |

---

## 4. 다음 단계

- {bullet — 추측 금지, 대화 확정만}

---

## 5. 8계층·워크북 (해당 시만)

| 계층 | 이번 세션 |
|------|-----------|
| Rule | |
| Command | |
| Skill | |
| Test Loop | |

---

*본 보고서는 Report/{NN}.REPORT.md — 세션 {NN} {세션 주제} 정리본이다.*
```

## Phase → 포함 STEP

| Phase | 포함 섹션 |
|-------|-----------|
| `red` | STEP RED |
| `green` | STEP GREEN (+ 선행 RED 1줄 요약 가능) |
| `refactor` | STEP REFACTOR |
| `repeat` | STEP REPEAT (+ 위 3종 요약 표) |
