# MagicSquare_xx — PRD (Product Requirements Document)

| 항목 | 내용 |
|------|------|
| 프로젝트 | MagicSquare_xx |
| 제품 | 4×4 **부분 마방진** 10선 검증 (`validate_lines`) |
| 단계 | STEP 3 — Test Loop (Logic Track) |
| 작성일 | 2026-06-10 |
| 근거 | [STEP1 Mom Test](../Report/STEP1_MomTest_Report.md) · [STEP3 워크북](../Report/STEP3_Session_Workbook_Report.md) · `.cursorrules` |

**SSOT 계층:** 본 PRD(FR·AC·성공 기준) → `.cursorrules`(ECB·TDD 실행 규칙) → Command·Skill.

---

## 1. 배경 · 문제

### 1.1 페르소나

4×4 **부분 마방진**(빈칸 2개, 숫자 1~16, 행·열·대각 합 34)을 손 계산 또는 코드로 다루는 **학습자**.

### 1.2 진짜 문제 (Mom Test)

행·열·대각선 **하나만** 맞춰도 「끝」이라고 느끼지만, 마방진이 요구하는 검증 항목(특히 **두 번째 대각선 D2**)을 처음부터 빠짐없이 돌리지 못해, 틀린 답을 확신한 채 시간을 쓰고 나중에 교차 대각선을 짚을 때까지 원인을 찾지 못한다.

### 1.3 제품 주제 (솔루션 최소화)

> 4×4 부분 마방진을 풀 때, 행·열·대각선 하나만 맞춘 상태에서 「끝」이라고 느끼기 전에, 마방진이 요구하는 **검증 10항**(행 4·열 4·대각 2)을 빠짐없이 확인할 수 있어야 한다.

본 PRD의 **최소 솔루션**은 공개 함수 `validate_lines(grid)` 하나다. UI·솔버·자동 채우기는 범위 밖이다.

---

## 2. 목표 · 성공 기준

| ID | 성공 기준 | Mom Test 연결 | PRD 매핑 |
|----|-----------|---------------|----------|
| **S1** | 「완료」 전 **10항**을 명시적으로 각각 확인 (한 대각선만 보고 끝내지 않음) | ①③ 조기 확신 / 전부 재계산 | FR-003, FR-004, FR-006 |
| **S2** | D1(좌하→우상)·D2(우하→좌상)를 **구분**해 각각 합산 | ①③ 교차 두 줄 | FR-004 |
| **S3** | 미통과 시 **어떤 선**이 문제인지 목록으로 반환 (`failed_lines`) | ② 같은 패턴 반복 → 항목 목록 | FR-003, FR-005~007 |

---

## 3. R-G-I-O

| | 내용 |
|---|------|
| **Role** | 부분 마방진 과제를 푸는 학습자 — 손·코드·제출 직전 검증 |
| **Goal** | 조기 확신 없이 10선을 빠짐없이 확인한 뒤에만 완료 판단 |
| **Input** | 4×4 `grid` (`0`=빈칸, `1~16` 채움) |
| **Output** | `status` + `failed_lines` (선 ID 목록) |

---

## 4. 범위

### 4.1 In Scope (Logic Track)

- `validate_lines(grid)` 구현 및 단위 테스트
- 10선 합산·`pass` / `fail` / `incomplete` 판정
- ARRR TDD Command·Skill 기반 개발 루프
- Golden 스냅샷·세션 Report (문서·테스트 인프라)

### 4.2 Out of Scope (Non-Goals)

| 항목 | 사유 |
|------|------|
| 매직스퀘어 **앱/UI** | STEP 3 Logic 우선 |
| 빈칸 **자동 채우기·솔버·힌트** | 검증만 다룸 |
| ECB 슬라이드 본문·E001~E005 **런타임 코드** | 문서·분류 전용 |
| 격자 형식 오류에 대한 **표준 예외 계약** | 테스트가 정의 (Boundary) |

Track A(UI)는 Layer=`boundary`로 **계약 테스트만** 확장 가능; 본 PRD v1은 Track B(Logic)를 정의한다.

---

## 5. 도메인 (Entity)

### 5.1 격자

| 항목 | 규칙 |
|------|------|
| 크기 | 4×4 (`GRID_SIZE = 4`) |
| 빈칸 | `0` |
| 채워진 칸 | `1` ~ `16` (`CELL_MAX = 16`) |
| 마법상수 | `MAGIC_CONSTANT = 34` |
| 인덱스 | 행·열 **0-based** (테스트·구현). 선 ID는 **1-based** (`R1`…`R4`) |

### 5.2 검증 10선 · 선 ID

| ID | 정의 | 0-based 좌표 (row, col) |
|----|------|-------------------------|
| **R1** ~ **R4** |第 n 행 전체 | 행 `n-1`, 열 `0~3` |
| **C1** ~ **C4** |第 n 열 전체 | 행 `0~3`, 열 `n-1` |
| **D1** | 좌하 → 우상 | `(3,0)(2,1)(1,2)(0,3)` |
| **D2** | 우하 → 좌상 | `(3,3)(2,2)(1,1)(0,0)` |

`LINE_IDS` 순서: `R1,R2,R3,R4,C1,C2,C3,C4,D1,D2`.

### 5.3 빈칸과 incomplete

한 선에 `0`이 **하나라도** 있으면 그 선은 합 34로 **확정할 수 없음** → `incomplete` 판정 후보. 해당 선 ID는 `failed_lines`에 포함될 수 있다.

---

## 6. 기능 요구 (FR) · Acceptance Criteria

| ID | 요구 | Acceptance Criteria (AC) | 성공 기준 |
|----|------|--------------------------|-----------|
| **FR-001** | 4×4 격자; 빈칸 `0`, 채움 `1~16` | 유효 입력은 4행×4열; 셀 값 `0` 또는 `1~16` | — |
| **FR-002** | 마법상수 34 | 완전히 채워진 선의 합 기준값은 34 | S1 |
| **FR-003** | 검증 **10선**; 선 ID 문자열 | `failed_lines` 요소는 `R1`…`R4`,`C1`…`C4`,`D1`,`D2` | S1, S3 |
| **FR-004** | D1·D2 **각각** 합산 | D1만 맞고 D2가 틀린 격자에서 `pass` 불가 | S2 |
| **FR-005** | 빈칸 있는 선 → incomplete 후보 | 해당 선 ID ∈ `failed_lines`, `status`는 `incomplete` (다른 선만 fail이면 규칙에 따름) | S3 |
| **FR-006** | 10선 모두 합 34·빈칸 없음 → **pass** | `status=="pass"`, `failed_lines==[]` | S1 |
| **FR-007** | 빈칸 없는데 합≠34인 선 존재 → **fail** | `status=="fail"`, `failed_lines`에 미통과 선만 | S3 |

### 6.1 판정 우선순위 (Control)

1. 선별로 빈칸(`0`) 존재 여부 확인 → incomplete 후보 선 집합
2. 빈칸 없는 선의 합 vs 34 → fail 후보 선 집합
3. **status**
   - incomplete 후보가 **1개 이상** → `"incomplete"`
   - 없고 fail 후보만 → `"fail"`
   - 둘 다 없음 → `"pass"`
4. `failed_lines`: `pass`이면 `[]`; 그 외 미통과 선 ID 목록 (구현에서 순서·중복 규칙은 테스트가 고정)

---

## 7. API (Boundary)

### 7.1 공개 함수

```python
def validate_lines(grid) -> dict:
    """
    4×4 격자의 10선(행·열·대각) 합을 검증한다.

    Args:
        grid: 길이 4인 2차원 시퀀스. 각 행 길이 4.

    Returns:
        {
            "status": "pass" | "fail" | "incomplete",
            "failed_lines": list[str],  # pass이면 []
        }
    """
```

### 7.2 파일 · 패키지

| 계층 | 경로 | 책임 |
|------|------|------|
| Entity 상수 (계획) | `entity/constants.py` | `GRID_SIZE`, `CELL_MAX`, `MAGIC_CONSTANT`, `LINE_IDS` SSOT |
| Control + Boundary | `src/validate_lines.py` | `validate_lines` 구현·공개 API |
| 테스트 | `tests/test_validate_lines.py` | Logic Track RED/GREEN |
| 픽스처 | `tests/conftest.py` | `grid_g1` 등 순수 격자 데이터 |
| Golden (계획) | `tests/golden/*.json` | PASS 묶음 스냅샷 |

현재 구현 상태: `validate_lines`는 **스tub**(`pass` 본문). 테스트 파일은 **import만** 존재.

---

## 8. Dual-Track

| | **Track B — Logic** (본 PRD) | **Track A — UI** (확장) |
|---|------------------------------|-------------------------|
| Layer | `entity` | `boundary` |
| 검증 | `validate_lines`·격자 | 렌더·이벤트·표시 |
| Mock | **Domain Mock 금지** | UI·API 응답만 |
| Command | `/red-test-plan` 기본 | Layer=`boundary` 치환 |

---

## 9. 개발 · 품질 (TDD · ARRR)

### 9.1 TDD 루프

**RED → GREEN → REFACTOR**. Phase마다 한 목표.

| Phase | 수정 범위 | 금지 |
|-------|-----------|------|
| RED | `tests/`만 | `src/` 수정, skip/xfail, assert 완화 |
| GREEN | `src/` + `tests/` | 묶음 외 ID 선해결, REFACTOR |
| REFACTOR | 구조만 | 동작·API 변경, 기능 추가 |

### 9.2 ARRR Command 체인

```
/red-test-plan → /red-skeleton → /green-minimal → /golden-master
       → /refactor-smell → /refactor-safe → /export-session
```

### 9.3 C2C · Test ID

`/red-test-plan` **Rule1**은 본 문서 **FR-00N** 인용. **Rule2** To-Do 1개 = GREEN 1묶음. **Rule3** Given/When/Then.

- Test ID: `T-{Layer약자}-{순번}` (예: `T-ENT-001`, `T-D-LOC-01`)
- RED 스켈레톤 Then: `pytest.fail("RED: {Test ID} — …")` 한 줄
- GREEN: **1커밋 = 1 RED 묶음** (commit은 사용자 요청 시)

### 9.4 상수 · ECB

- `34`·`16`·`4` 리터럴 금지 → `entity/constants.py` import
- Entity는 `boundary`·`control` import 금지
- E001~E005: 문서 전용, **raise/return/emit 금지**

---

## 10. 테스트 전략

| 유형 | 위치 | 목적 |
|------|------|------|
| 단위 | `tests/test_validate_lines.py` | FR별 RED/GREEN |
| 픽스처 | `tests/conftest.py` | `grid_g1`: 0 두 개, row-major |
| Golden | `tests/test_golden_*.py`, `-m golden` | GREEN 후 회귀 앵커 |
| 게이트 | `python -m pytest tests/ -v` | REFACTOR·Export 전 PASS |

### 10.1 대표 시나리오 (테스트 설계 참고)

| 시나리오 | 기대 `status` | `failed_lines` 요지 |
|----------|---------------|---------------------|
| 완성 마방진 (1~16 배치) | `pass` | `[]` |
| R3에 빈칸 1개 | `incomplete` | `R3`, `C3` 등 빈칸 포함 선 |
| D2만 합≠34 (나머지 OK) | `fail` | `D2` 포함 |
| 빈칸 2개 부분 격자 G1 | `incomplete` | 빈칸 지나는 선들 |

---

## 11. 인프라 · 문서

| 경로 | 용도 |
|------|------|
| `.cursorrules` | ECB·TDD·AI 실행 규칙 |
| `docs/PRD.md` | 본 문서 (FR·AC SSOT) |
| `.cursor/commands/` | ARRR slash Command |
| `.cursor/skills/magic-square-tdd/` | TDD Skill |
| `.cursor/skills/magic-square-docs/` | Report·Transcript Export |
| `Report/`, `Prompting/` | 세션 NN 보고서 |
| `pyproject.toml` | pytest (`pythonpath = ["."]`) |

---

## 12. 변경 이력

| 날짜 | 버전 | 내용 |
|------|------|------|
| 2026-06-10 | 1.0 | Mom Test·STEP3 워크북·`.cursorrules`·Harness 기준 초안 |

---

*본 PRD는 MagicSquare_xx Logic Track의 단일 진실 공급원이다. `/red-test-plan` Rule1은 FR-00N을 인용하며, FR에 없는 동작은 RED에 넣지 않는다.*
