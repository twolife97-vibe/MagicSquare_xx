# golden-master — ARRR R단계 (Respond = GREEN ②) Golden 스냅샷 고정

**추가 입력 없이 즉시 실행.** 사용자가 `/golden-master`만 입력했다.
대상 **RED 묶음**·Test ID·`validate_lines` 기대 출력은 **직전 GREEN(`/green-minimal`)·채팅·`docs/PRD.md` FR**에서 자동 추출한다. 추가 질문·확인 요청 금지.

**역할:** ARRR **R단계(Respond)** — GREEN으로 PASS된 묶음의 **golden 마스터 스냅샷**을 `tests/golden/`에 고정한다. **동작 변경 없음** — 회귀·리팩터 앵커용.

**한국어**로 응답한다.

**Skill:** **magic-square-tdd** Skill이 있으면 **자동으로 읽고 따른다**.

---

## SSOT

| 우선순위 | 경로 | 용도 |
|----------|------|------|
| 1 | 직전 `/green-minimal` 보고 | PASS Test ID·격자·기대 dict |
| 2 | `docs/PRD.md` FR-006~007 | pass/fail/incomplete 계약 |
| 3 | `.cursorrules` | API 스키마·10선 ID |
| 4 | 채팅 | RED 묶음·pytest **실측** |

---

## 필수 선언 (응답 첫 줄)

```
Phase: green | Layer: entity | Track: Logic | Golden: master
```

---

## 전제 (게이트)

1. `python -m pytest tests/ -v` — **전부 PASS**. 아니면 중단 → `/green-minimal`.
2. 이번 **RED 묶음** Test ID가 모두 녹색임을 확인.

---

## 절차

### 1. 대상 확정

- PASS된 Test ID·입력 `grid`·기대 `{"status", "failed_lines"}`를 채팅·테스트에서 확정한다.

### 2. Golden 파일 작성 (`tests/golden/`)

| 항목 | 규칙 |
|------|------|
| 경로 | `tests/golden/{test_id_slug}.json` (예: `T-ENT-001` → `t_ent_001.json`) |
| 내용 | `grid`, `expected` (status·failed_lines), `test_id`, `fr` (PRD FR 인용) |
| 마커 | golden 테스트는 `@pytest.mark.golden` |

예시 스냅샷:

```json
{
  "test_id": "T-ENT-001",
  "fr": "FR-006",
  "grid": [[16,3,2,13],[5,10,11,8],[9,6,7,12],[4,15,14,1]],
  "expected": {"status": "pass", "failed_lines": []}
}
```

### 3. Golden 테스트 추가 (`tests/test_golden_validate_lines.py` 또는 Skill convention)

- 스냅샷 로드 → `validate_lines(grid)` → `expected`와 **전부 일치** assert.
- **Domain Mock 금지.**

### 4. 검증

```
pytest tests/ -v -m golden
python -m pytest tests/ -v
```

**기본:** `UPDATE_GOLDEN` **사용하지 않음** — 파일을 직접 작성·갱신.

`UPDATE_GOLDEN=1`은 사용자가 **명시적으로 스냅샷 재생성을 요청**할 때만 (의도적 계약 변경·ISS 문서화 후).

---

## 보고 형식

```
Phase: green | Layer: entity | Track: Logic | Golden: master

- Test ID: T-ENT-001
- pytest: N passed (golden N/N)
- golden: tests/golden/t_ent_001.json 신규
- 변경: tests/golden/, tests/test_golden_validate_lines.py
```

---

## 금지

| 금지 | 이유 |
|------|------|
| `src/validate_lines.py` **동작 변경** | golden은 관측만 |
| **`UPDATE_GOLDEN=1` 임의 실행** | 사용자 요청·ISS 후만 |
| PASS 안 된 묶음 golden 고정 | 게이트 |
| Domain Mock | ECB |
| assert·기대값 **완화**로 golden 맞추기 | TDD 우회 |
| **git commit** (사용자 미요청) | `.cursorrules` |

---

## 이전·다음 Command

| Command | 역할 |
|---------|------|
| `/green-minimal` | 최소 구현 + PASS |
| **`/golden-master`** | **golden 스냅샷 고정** |
| `/refactor-smell` | 스멜 탐지 (golden matched 게이트) |
| `/export-session` | ARRR 1사이클 Report |

---

## 참고

- PRD: `docs/PRD.md`
- REFACTOR golden: `.cursor/commands/refactor-safe.md`
- TDD Skill: `.cursor/skills/magic-square-tdd/SKILL.md`
