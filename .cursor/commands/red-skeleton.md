# red-skeleton — ARRR A단계 (RED ④) pytest.fail 스켈레톤

**추가 입력 없이 즉시 실행.** 사용자가 `/red-skeleton`만 입력했다.
Test ID·함수명·격자·파일 경로는 **직전 `/red-test-plan` 출력(블록 1~3)·현재 채팅·`.cursorrules`**에서 자동 추출한다. 추가 질문·확인 요청 금지.

**역할:** ARRR **A단계(RED ④)** — `/red-test-plan` 설계표 기준으로 `tests/`에 **pytest.fail 스켈레톤만** 작성한다. `assert` 본문·구현 호출 결과 검증은 **다음 `/tdd-red`**에서 채운다.

**한국어**로 응답한다.

**Skill:** 프로젝트에 **magic-square-tdd** Skill(`.cursor/skills/` 또는 동등 경로)이 있으면 **자동으로 읽고 따른다** — 격자 명명·픽스처·import·Test ID 규칙이 Skill과 충돌하면 Skill 우선.

---

## SSOT (입력 순서)

| 우선순위 | 출처 | 사용 |
|----------|------|------|
| 1 | 직전 `/red-test-plan` 블록 3 | 파일 경로·함수명·Test ID·RED 묶음 |
| 2 | `/red-test-plan` 블록 2 | Given→Then·Invariant·Expected RED Failure |
| 3 | `docs/PRD.md` | FR·AC (Test ID·Then 정합) |
| 4 | `.cursorrules` | 도메인·API·TDD 금지 |
| 5 | magic-square-tdd Skill | TDD 관례·픽스처·상수 경로 |

`/red-test-plan`이 채팅에 없으면 `.cursorrules`·채팅에서 **Test ID 1건**만 추론해 스켈레톤 1개를 작성한다.

---

## 필수 선언 (응답 첫 줄)

```
Phase: red | Layer: entity | Track: Logic
```

Track A(boundary)·UI는 `/red-test-plan`에서 Layer·Track를 바꾼 뒤, 본 Command에서도 동일하게 선언한다.

---

## 스켈레톤 규칙

| 항목 | 규칙 |
|------|------|
| **AAA 주석** | `# Given` · `# When` · `# Then` (대소문자·슬래시 그대로) |
| **Then** | `pytest.fail("RED: {Test ID} — …")` **한 줄만** — 기대 동작·Then 요약을 메시지에 포함 |
| **Assert** | **금지** — `assert`, `pytest.approx`, 결과 dict 검증 없음 |
| **우회** | `@pytest.mark.skip`, `xfail`, `pass`(통과 더미), 빈 `def` 금지 |
| **상수** | `34`·`16`·`4` 리터럴 금지 — `entity/constants.py`에서 import (픽스처·Arrange 데이터 조립용만) |
| **대상 호출** | `# When`에서 `validate_lines(grid)` 호출 **허용** (stub·미구현이어도 됨). **Then은 항상 `pytest.fail`로 종료** |
| **변경 범위** | `tests/`만 — `src/`·`entity/` **수정 금지** (`entity/constants.py`는 이미 있어야 함) |
| **RED 묶음** | `/red-test-plan` 블록 3의 Test ID 목록과 **1:1** — 한 번에 설계된 묶음만 추가 |

---

## conftest — `tests/conftest.py`

블록 3에 `grid_g1`이 명시되었거나 Skill·설계표에 없으면 **아래 기본 픽스처**를 사용한다.

- **`grid_g1`**: 4×4 격자, **빈칸 `0` 두 개**, row-major(G1) 부분 마방진
- 상수는 `entity.constants` import로 격자 길이·범위 검증에만 사용 (로직 assert 아님)

```python
import pytest

from entity.constants import CELL_MAX, GRID_SIZE, MAGIC_CONSTANT


@pytest.fixture
def grid_g1():
    """G1: row-major 4×4, blanks at (1,2) and (3,2) — two 0s."""
    grid = [
        [16,  3,  2, 13],
        [ 5, 10,  0,  8],
        [ 9,  6,  7, 12],
        [ 4, 15,  0,  1],
    ]
    assert len(grid) == GRID_SIZE
    assert all(len(row) == GRID_SIZE for row in grid)
    assert sum(cell == 0 for row in grid for cell in row) == 2
    assert MAGIC_CONSTANT == 34 and CELL_MAX == 16
    return grid
```

`tests/conftest.py`가 없으면 생성한다. 이미 있으면 **`grid_g1`만 추가**(기존 픽스처 덮어쓰기 금지).

---

## 템플릿 예시 — `test_d_loc_01_blank_coords_row_major`

Test ID `T-D-LOC-01` · 블록 3 함수명 `test_d_loc_01_blank_coords_row_major` · 파일 `tests/test_validate_lines.py`.

```python
import pytest

from entity.constants import GRID_SIZE
from src.validate_lines import validate_lines


def test_d_loc_01_blank_coords_row_major(grid_g1):
    # Given
    grid = grid_g1
    assert len(grid) == GRID_SIZE

    # When
    result = validate_lines(grid)

    # Then
    pytest.fail("RED: T-D-LOC-01 — blank cell coords (row-major G1) → incomplete + failed_lines")
```

- `result`는 When에서만 바인딩 (Then에서 사용하지 않음 — lint 경고 시 `_ = result` 또는 `# noqa` 대신 **변수명 `_result`** 사용 가능).
- 메시지 `"RED: {Test ID} — …"`는 블록 2 **Given→Then**과 일치시킨다.

---

## 절차

1. magic-square-tdd Skill이 있으면 **먼저 읽는다**.
2. `/red-test-plan` 블록 3에서 파일·함수명·Test ID·pytest 명령·RED 묶음을 확정한다.
3. `tests/conftest.py`에 `grid_g1`(또는 설계표 명시 픽스처)을 준비한다.
4. 설계된 **각 Test ID**마다 AAA + `pytest.fail` 스켈레톤 함수를 `tests/`에 추가한다.
5. 블록 3의 **pytest 명령**으로 실행해 **FAIL**을 확인한다.
6. 아래 **보고 형식**으로 응답한다.

---

## pytest 실행

블록 3 명령을 그대로 실행한다. 예:

```
pytest tests/test_validate_lines.py::test_d_loc_01_blank_coords_row_major -v
```

묶음 전체:

```
pytest tests/test_validate_lines.py -v -k "d_loc_01 or ent_001"
```

(실제 `-k`는 이번 RED 묶음 함수명에 맞게 조정)

**RED 성공 기준:** `FAILED` + `pytest.fail` 메시지에 `RED: {Test ID}` 포함. `PASSED`이면 스켈레톤 오류 — `pytest.fail` 누락·우회 의심.

---

## 보고 형식 (pytest 실행 후)

```
Phase: red | Layer: entity | Track: Logic

- Test ID: T-D-LOC-01
- pytest: FAIL — RED: T-D-LOC-01 — …
- 변경: tests/conftest.py, tests/test_validate_lines.py
```

Test ID가 여러 개면 bullet을 Test ID마다 반복한다.

---

## 금지

| 금지 | 이유 |
|------|------|
| `src/` 수정 | GREEN 단계 |
| `entity/constants.py` **생성·수정** | Entity Harness 범위; 스켈레톤은 import만 |
| `assert`로 status·failed_lines 검증 | `/tdd-red`에서 assert RED |
| `@pytest.mark.skip`, `xfail`, 통과 `pass` | TDD 우회 |
| `34`·`16`·`4` **리터럴** in 테스트 본문 | `entity.constants` import |
| Domain Mock (`patch`, `MagicMock` on `validate_lines`) | ECB·red-test-plan 블록 4 |
| GREEN / REFACTOR | RED ④는 스켈레톤만 |

---

## 이전·다음 Command

| Command | 역할 |
|---------|------|
| `/red-test-plan` | RED ③ — C2C·테스트 플랜 (코드 없음) |
| **`/red-skeleton`** | **RED ④ — pytest.fail 스켈레톤 (`tests/`만)** |
| `/tdd-red` | assert 본문 RED + pytest FAIL 확인 |

---

## 참고

- 설계표: `.cursor/commands/red-test-plan.md`
- assert RED: `.cursor/commands/tdd-red.md`
- API: `validate_lines(grid) -> {"status", "failed_lines"}` (`.cursorrules`)
- 상수: `entity/constants.py` — `GRID_SIZE`, `CELL_MAX`, `MAGIC_CONSTANT` (Skill·Harness와 동일 명명)
