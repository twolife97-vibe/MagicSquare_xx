---
name: magic-square-tdd
description: >-
  MagicSquare_xx Dual-Track TDD (ARRR: Ask/Respond/Refine). Guides RED design,
  pytest.fail skeletons, minimal GREEN, and safe REFACTOR for validate_lines.
  Use when Phase is red, green, or refactor; when running Commands
  /red-test-plan, /red-skeleton, /green-minimal, /golden-master,
  /refactor-smell, /refactor-safe; or when the user mentions TDD, RED, GREEN,
  REFACTOR, Dual-Track, C2C, or pytest.fail.
disable-model-invocation: true
---

# magic-square-tdd

MagicSquare_xx **4×4 부분 마방진** TDD 워크플로. Command 실행 시 본 Skill을 읽고 따른다.

**SSOT:** `.cursorrules` → `docs/PRD.md` (FR·AC) → 채팅 확정 내용. PRD 없으면 `.cursorrules`를 FR 대체.

**언어:** 한국어. **git commit:** 사용자 명시 요청 시만.

---

## 1. ARRR ↔ TDD 매핑

| ARRR | TDD | 단계 | Command | 수정 범위 |
|------|-----|------|---------|-----------|
| **Ask** | **RED** | ③ 설계 | `/red-test-plan` | 없음 (문서만) |
| **Ask** | **RED** | ④ 스켈레톤 | `/red-skeleton` | `tests/` |
| **Ask** | **RED** | assert RED | `/tdd-red` | `tests/` |
| **Respond** | **GREEN** | 최소 구현 | `/green-minimal` | `src/` + `tests/` |
| **Respond** | **GREEN** | golden 고정 | `/golden-master` | `tests/golden/` (있을 때) |
| **Refine** | **REFACTOR** | ⑦ 스멜 | `/refactor-smell` | 없음 |
| **Refine** | **REFACTOR** | ⑧ safe | `/refactor-safe` | `src/`·`entity/`·헬퍼 |

한 Phase·한 목표만. RED → GREEN → REFACTOR 순서를 건너뛰지 않는다.

---

## 2. Phase 선언 (응답 첫 줄)

| Phase | 형식 |
|-------|------|
| RED 설계 | `Phase: red \| Layer: {entity\|boundary} \| Track: {Logic\|UI}` |
| RED 스켈레톤 | `Phase: red \| Layer: entity \| Track: Logic` |
| GREEN | `Phase: green \| Layer: entity \| Track: Logic` |
| REFACTOR smell | `Phase: refactor \| Scope: src/ tests/ \| Track: Logic+UI` |
| REFACTOR safe | `Phase: refactor \| Layer: entity \| Track: Logic` |
| 레거시 tdd-red | `Phase: RED \| Target: validate_lines` |

Track A: `Layer: boundary`, `Track: UI`. Track B: `Layer: entity`, `Track: Logic`.

---

## 3. C2C Rule 1~3 요약

`/red-test-plan` 블록 1. PRD FR → To-Do 1개 → Test ID·Given/When/Then.

| Rule | 내용 |
|------|------|
| **Rule1** | `docs/PRD.md` FR·AC 인용 (없으면 `.cursorrules` Entity/Control) |
| **Rule2** | 이번 RED **행동 1개** — 다음 GREEN과 1:1 |
| **Rule3** | **Test ID** · Given(격자·전제) · When(`validate_lines(grid)`) · Then(`status`, `failed_lines`) |

Test ID: `T-{Layer약자}-{순번}` (예: `T-ENT-001`, `T-D-LOC-01`).

---

## 4. RED 절대 금지

| 금지 | 대안 |
|------|------|
| `src/` 수정 | `/green-minimal` |
| `@pytest.mark.skip`, `xfail`, 통과 `pass` | 명확한 격자·assert |
| assert 완화 (`==`→`in`, 조건 삭제) | 기대값·격자 수정 |
| **Logic Track Domain Mock** | 실제 `grid`·`validate_lines` 호출 |
| E001~E005 emit | 문서 전용 |
| RED 묶음 외 Test ID 선제 구현 | 1묶음씩 |

스켈레톤(`/red-skeleton`): Then은 `pytest.fail("RED: {Test ID} — …")` **한 줄만**. 상수 `34`·`16`·`4` 리터럴 금지 → `entity.constants` import.

---

## 5. GREEN 규칙

- **1커밋 = 1 RED 묶음** (커밋은 사용자 요청 시).
- `src/`에 **묶음 PASS에 필요한 최소 코드**만.
- `pytest.fail` 제거 → 설계표 Then에 맞는 **assert** 교체.
- **상수 SSOT:** `entity/constants.py` — `GRID_SIZE`, `CELL_MAX`, `MAGIC_CONSTANT`, `LINE_IDS` 등. 구현·테스트 모두 import; 매직넘버 금지.
- Entity는 `boundary`·`control` import 금지. E001~E005 raise/return 금지.
- 이번 묶음 외 Test ID 동시 해결·REFACTOR·assert 완화 금지.

---

## 6. REFACTOR 규칙

**게이트:** `python -m pytest tests/ -v` 전부 PASS. 아니면 중단 → GREEN.

**Change Budget** (1 safe = 1 스멜):

| 항목 | 상한 |
|------|------|
| 파일 | ≤ 3 |
| 클래스 | ≤ 1 |
| 메서드 | ≤ 3 |

- 입출력·예외·`validate_lines` 반환 의미 **불변**.
- 기능 추가·버그 수정 금지 → `/green-minimal`.
- **golden:** 기본 `UPDATE_GOLDEN` 없이 matched. 의도적 diff만 ISS 문서 + 사용자 요청 시 `UPDATE_GOLDEN=1`. 비의도 → 롤백.

---

## 7. Track A (UI) vs Track B (Logic)

| | **Track A — UI** | **Track B — Logic** |
|---|------------------|---------------------|
| Layer | `boundary` | `entity` |
| Track | `UI` | `Logic` |
| 검증 대상 | 렌더·이벤트·표시 계약 | `validate_lines`·도메인 |
| Mock | UI·API 응답만 | **Domain Mock 금지** |
| 테스트 데이터 | props·이벤트 실값 | 4×4 `list[list[int]]`·픽스처 |
| Command | Layer만 `boundary`로 치환 | 기본값 |
| 범위 (`.cursorrules`) | UI 본격 구현은 범위 밖 — 계약 테스트만 | `src/validate_lines.py` |

---

## 8. Command 체인

```
/red-test-plan → /red-skeleton → [/tdd-red] → /green-minimal → /golden-master
                                                      ↓
                              /refactor-smell → /refactor-safe → (반복 smell)
```

| Command | 산출 |
|---------|------|
| `/red-test-plan` | C2C·Track B 표·테스트 플랜·ECB 점검 — **코드 없음** |
| `/red-skeleton` | `pytest.fail` 스켈레톤 + `tests/conftest.py` `grid_g1` |
| `/tdd-red` | assert RED (레거시·단건) |
| `/green-minimal` | 최소 구현 + PASS |
| `/golden-master` | golden 스냅샷 고정 (harness 있을 때) |
| `/refactor-smell` | 스멜 표 + safe 후보 1~3 — **수정 없음** |
| `/refactor-safe` | 후보 1건 Safe Refactor |

완료 문구: `/red-test-plan` → `/red-skeleton 으로 넘길 준비됐다`

---

## 9. pytest 명령 패턴

```bash
# 게이트·회귀 (전체)
python -m pytest tests/ -v

# RED 묶음 단건
pytest tests/test_validate_lines.py::test_d_loc_01_blank_coords_row_major -v

# 파일 전체
pytest tests/test_validate_lines.py -v

# golden (harness 있을 때)
pytest tests/ -v -m golden
```

| Phase | 성공 기준 |
|-------|-----------|
| RED 스켈레톤 | `FAILED` + 메시지 `RED: {Test ID}` |
| RED assert | `FAILED` (미구현·stub) |
| GREEN | 대상 `PASSED`, 파일 `0 failed` |
| REFACTOR safe | `0 failed` + golden matched 또는 N/A |

`pyproject.toml`: `pythonpath = ["."]`.

---

## 10. 완료 보고 형식

### RED 설계 (`/red-test-plan`)
4블록 표만. 마지막: `/red-skeleton 으로 넘길 준비됐다`

### RED 스켈레톤
```
Phase: red | Layer: entity | Track: Logic
- Test ID: T-D-LOC-01
- pytest: FAIL — RED: T-D-LOC-01 — …
- 변경: tests/conftest.py, tests/test_validate_lines.py
```

### GREEN
```
Phase: green | Layer: entity | Track: Logic
- PASS: T-D-LOC-01 (test_…)
- pytest: N passed — 회귀 없음
- 변경: src/validate_lines.py, tests/…
```

### REFACTOR smell
```
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI
- pytest: N passed — 게이트 통과
- 스멜: P0=n, P1=n, P2=n
- refactor-safe 후보: #1 …
- 변경: 없음 (탐지만)
```

### REFACTOR safe
```
Phase: refactor | Layer: entity | Track: Logic
- 스멜: #1 P0 Magic Number — …
- 변경 요약: … (Budget: 파일/클래스/메서드)
- pytest: N passed — 0 failed
- golden matched: yes | N/A
- 변경: src/…
```

---

## 도메인·API (`.cursorrules` 요약)

- 4×4 격자, `0`=빈칸, 채워진 칸 `1~16`, 마법상수 **34**.
- 10선: R1~R4, C1~C4, D1(좌하→우상), D2(우하→좌상).
- `validate_lines(grid) -> {"status": "pass"|"fail"|"incomplete", "failed_lines": [...]}`.
- D1·D2 **구분** 합산. 빈칸 있는 선 → `incomplete` 후보.

---

## 파일·픽스처 관례

| 경로 | 용도 |
|------|------|
| `entity/constants.py` | 상수 SSOT |
| `src/validate_lines.py` | Control + Boundary API |
| `tests/test_validate_lines.py` | Logic 테스트 |
| `tests/conftest.py` | `grid_g1` — 0 두 개, row-major |

```python
# conftest grid_g1 요약
@pytest.fixture
def grid_g1():
    return [[16,3,2,13], [5,10,0,8], [9,6,7,12], [4,15,0,1]]
```

---

## ECB · E001~E005

런타임에 사용하지 않는다. 테스트·구현에서 raise/return/emit 금지.

| 코드 | 의미 |
|------|------|
| E001 | Entity 혼입 |
| E002 | Control 누락 |
| E003 | Boundary 침범 |
| E004 | Mock 오용 |
| E005 | 계층 순서 위반 |

---

## Command 상세

- `.cursor/commands/red-test-plan.md`
- `.cursor/commands/red-skeleton.md`
- `.cursor/commands/green-minimal.md`
- `.cursor/commands/golden-master.md`
- `.cursor/commands/refactor-smell.md`
- `.cursor/commands/refactor-safe.md`
- `.cursor/commands/export-session.md`
- `.cursor/commands/tdd-red.md`

## Repeat · Export

ARRR 1사이클 완료 후 `/export-session` — **magic-square-docs** Skill + `Report/{NN}.REPORT.md` + `Prompting/{NN}.Export-Transcript.md`.
