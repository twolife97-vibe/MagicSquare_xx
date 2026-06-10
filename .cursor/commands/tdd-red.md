# TDD RED — validate_lines 실패 테스트

`validate_lines(grid)`의 새 동작을 검증하는 **실패 테스트**를 `tests/`에만 작성한다.

## 필수 선언 (응답 첫 줄)

```
Phase: RED | Target: validate_lines
```

## AAA 절차

1. **Arrange** — 4×4 `grid`와 기대 `status`·`failed_lines`를 확정한다.
   - `0` = 빈칸, 채워진 칸 `1~16`, 마법상수 **34**
   - 선 ID: R1~R4, C1~C4, D1(좌하→우상), D2(우하→좌상)
2. **Act** — `result = validate_lines(grid)` 호출.
3. **Assert** — `result["status"]`, `result["failed_lines"]`를 명시적으로 검증.
4. **Confirm** — `pytest`로 **FAIL**을 확인한다. 통과시키려 하지 않는다.

## pytest 예시

```python
def test_pass_when_all_ten_lines_sum_to_34():
    # Arrange
    grid = [
        [16,  3,  2, 13],
        [ 5, 10, 11,  8],
        [ 9,  6,  7, 12],
        [ 4, 15, 14,  1],
    ]
    # Act
    result = validate_lines(grid)
    # Assert
    assert result["status"] == "pass"
    assert result["failed_lines"] == []


def test_incomplete_when_line_contains_blank():
    # Arrange — R3·C3에 0(빈칸) 포함
    grid = [
        [16,  3,  2, 13],
        [ 5, 10, 11,  8],
        [ 9,  6,  0, 12],
        [ 4, 15, 14,  1],
    ]
    # Act
    result = validate_lines(grid)
    # Assert
    assert result["status"] == "incomplete"
    assert set(result["failed_lines"]) >= {"R3", "C3"}
```

실행:

```
pytest tests/test_validate_lines.py -v
```

RED 성공 기준: 새 테스트가 **FAIL** (구현 `pass` 또는 미구현).

## 보고 형식

```
Phase: RED | Target: validate_lines

- 테스트: test_<이름>
- Arrange: grid 요약 (또는 핵심 칸), 검증 의도 한 줄
- Assert: status=<값>, failed_lines=<값>
- pytest: FAIL — <실패 이유 한 줄>
- 변경: tests/test_validate_lines.py 만
```

## 금지

- `src/` 수정 (Entity·Control·Boundary 구현은 GREEN)
- assert 완화 (`==` → `in`, 범위 넓히기, 조건 삭제)
- `@pytest.mark.skip`, `xfail`, `pass`로 테스트 우회
- RED 한 번에 **테스트 1개**만 추가 (다음 RED는 GREEN 이후)

## 참고

- API: `validate_lines(grid) -> {"status": "pass"|"fail"|"incomplete", "failed_lines": [...]}`
- 규칙: `.cursorrules` Entity / Control / Boundary / TDD 루프
