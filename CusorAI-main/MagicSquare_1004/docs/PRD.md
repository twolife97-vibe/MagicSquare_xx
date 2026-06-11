# MagicSquare_1004 — PRD (Product Requirements Document)

| 항목 | 내용 |
|------|------|
| 프로젝트 | MagicSquare_1004 |
| 버전 | 0.1 (초안) |
| 생성일 | 2026-06-05 |
| 근거 | Mom Test STEP 1 — [Report/01.REPORT.md](../Report/01.REPORT.md), [Report/02.REPORT.md](../Report/02.REPORT.md), [Report/03.REPORT.md](../Report/03.REPORT.md) |
| 세션 | **세션 3~4** — Rule · Command · Skill · Test Loop · ARRR |

---

## 1. 개요

### 1.1 배경

4×4 **부분** 마방진(빈칸 2개, 1~16, 합 34) 학습자는 빈칸을 채운 **직후** **10선**(행 4 + 열 4 + 주대각 1 + 부대각 1) 합이 34인지 확인하는 데 시간이 많이 든다.

**Mom Test 증거 (실제 인터뷰):**

> “지난주 OO 과제에서 빈칸 2개 넣고 행·열·대각선 합 맞췄는데 **대각선 하나를 빼먹어서 20분 날렸다.**”

**보조 증거 (시뮬레이션 — [Report/02.REPORT.md](../Report/02.REPORT.md)):**

- 10줄 검산 **4~5회**, **10분+** 반복
- “**34가 아니다**는 바로 알았는데, **어느 줄**인지는 몰랐어”
- “**10줄 중 어느 줄이 34가 아닌지** 한 번에 보는 방법이 없었다”

### 1.2 진짜 문제

> 4×4 부분 마방진에서 빈칸 2개를 채운 뒤 **행·열·대각선(10선) 합 34 여부를 확인할 때 일부 줄(예: 대각선)을 빼먹어 맞는지 판정하지 못하고**, 같은 시도를 반복하며 **20분** 같은 시간을 잃는다.

**보강 정의 (시뮬레이션 기반):**

> 빈칸을 채운 직후, **10선 합 34 여부를 빠르게 확정하지 못하고**, 틀렸을 때 **어느 줄**인지 바로 짚지 못해 **같은 검산을 4~5회·10분 이상** 반복한다.

### 1.3 이번 릴리스 목표 (세션 3)

**판정·확인 비용**을 줄이기 위해, 10선 합 34 **검증 Rule**, **Command** `validate_lines`, **Test Loop**만 제공한다.

**의도적 배제:** Solver, PyQt UI, BCE 전체 — Mom Test에서 **표면 솔루션**으로 분류됨.

### 1.4 주제 (1문장)

> **4×4 부분 마방진에서 빈칸을 채운 직후, 행·열·대각선 10선이 각각 34인지 빠르게 확정하고, 틀리면 어느 줄인지 바로 짚을 수 있게 검증 규칙과 테스트 루프를 만든다.**

---

## 2. 사용자 및 사용 시나리오

### 2.1 R-G-I-O

| | 내용 |
|---|---|
| **R — Role** | 4×4 **부분** 마방진 학습자. 빈칸 2개(0)를 1~16으로 채운 뒤 **맞았는지 스스로 확인**해야 함 |
| **G — Goal** | 빈칸 채운 후 **10선 합 34 여부를 즉시 판정**하고, 틀리면 **어느 행·열·대각선**인지 식별 *(20분 낭비 → 처음·한 번에)* |
| **I — Input** | 4×4 정수 격자. 셀 값 **0**(빈칸) 또는 **1~16** |
| **O — Output** | **통과/실패** + 실패 시 **실패 줄 목록**(행 i, 열 j, 대각선 main/anti)과 **해당 합 값**(34가 아닌 합) |

### 2.2 페르소나

| 항목 | 내용 |
|------|------|
| 역할 | 4×4 부분 마방진 학습자 |
| 행동 범위 | 손으로 풀기 / 코드(Jupyter, `print`)로 다루기 |
| 도메인 | 4×4 격자, **빈칸 2개(0)**, **1~16**, **합 34** |

### 2.3 예시 격자 (과제 기준)

| | | | |
|---|---|---|---|
| 16 | 3 | 2 | 13 |
| 5 | 10 | 11 | **?** |
| 9 | 6 | **?** | 12 |
| 4 | 15 | 14 | 1 |

*(빈칸 위치: (1,3), (2,2) — 0-index 기준)*

### 2.4 핵심 시나리오

1. 학습자가 4×4 격자에 빈칸 2칸을 1~16 값으로 채운다.
2. **`validate_lines(grid)`** 한 번으로 10선 합을 검사한다.
3. **통과** → 완료. **실패** → **어느 줄**이 34가 아닌지 확인하고 해당 칸만 수정한다.
4. **Test Loop**로 같은 실패·성공을 재현한다 (Red → Green).

---

## 3. 도메인 규칙

### 3.1 MagicSquare 정의

| 규칙 | 설명 |
|------|------|
| 격자 | 4×4 정수 배열 |
| 값 범위 | **0** = 빈칸, **1~16** = 채워진 칸 |
| 빈칸 | 정확히 **2개** (0) — *세션 3 검증 입력 가정* |
| 마법 상수 | **34** |
| 10선 | 행 4 + 열 4 + 주대각(main) 1 + 부대각(anti) 1 |

### 3.2 검증 Rule (세션 3)

| ID | Rule | 실패 조건 |
|----|------|-----------|
| R1 | 각 **행**의 합 = 34 | `sum(row[i]) ≠ 34` |
| R2 | 각 **열**의 합 = 34 | `sum(col[j]) ≠ 34` |
| R3 | **주대각선** `(0,0)(1,1)(2,2)(3,3)` 합 = 34 | `sum(main_diag) ≠ 34` |
| R4 | **부대각선** `(3,0)(2,1)(1,2)(0,3)` 합 = 34 | `sum(anti_diag) ≠ 34` |
| R5 | 격자에 **0(빈칸)** 이 있으면 “완성 검증” 불가 | `0 in grid` → `incomplete` |

---

## 4. 기능 요구사항

### 4.1 In Scope (세션 3)

| ID | 계층 | 요구사항 | 우선순위 |
|----|------|----------|----------|
| F1 | **Rule** | R1~R5를 코드/문서로 정의 | P0 |
| F2 | **Command** | 4×4 격자 입력 → 10선 각 합 계산 | P0 |
| F3 | **Command** | 각 줄 합과 34 비교 → pass/fail | P0 |
| F4 | **Command** | fail 시 **틀린 줄 ID + 실제 합** 반환 (예: `row:2 sum:33`) | P0 |
| F5 | **Test Loop** | 합 ≠ 34 격자 — Red 테스트 (실패 재현) | P0 |
| F6 | **Test Loop** | 과제 정답 격자 — Green 테스트 (통과) | P0 |
| F7 | **(Skill)** | pytest + fixture 반복 실행 *(선택)* | P2 |

**핵심 Command:**

```python
def validate_lines(grid: list[list[int]]) -> ValidationResult: ...
```

### 4.2 Out of Scope (표면 문제 — 하지 않음)

| 제외 | 이유 (Mom Test) |
|------|-----------------|
| `Solver` / 빈칸 자동 채우기 / 힌트 | 학습자 고통은 **풀기**보다 **맞는지 확인** |
| `GridUI`, `InputHandler`, PyQt | UI·입력은 **표면 솔루션** |
| BCE 전체 Entity/Boundary | 설계만으로는 검증·재현 없음 |
| 1~16 중복·누락·범위 검증 | 세션 3 범위 밖 — **합 34 판정**에 집중 |
| Cursor/TDD **방법론 강제** | PRD 범위는 **동작**만 |

---

## 5. 입출력 명세

### 5.1 Input

```text
grid: list[list[int]]  # 4×4, 값 0 또는 1~16
```

**예시 (과제 슬라이드 정답):**

```text
[[16,  3,  2, 13],
 [ 5, 10, 11,  8],
 [ 9,  6,  7, 12],
 [ 4, 15, 14,  1]]
```

### 5.2 Output

```text
ValidationResult {
  ok: bool
  status: "pass" | "fail" | "incomplete"
  lines: [
    { id: "row:0" | "col:1" | "diag:main" | "diag:anti", sum: int, expected: 34 }
  ]  # fail/incomplete 시 틀린 줄만 (10선 전부 검사, 누락 없음)
}
```

**줄 ID 규칙:**

| id | 의미 |
|----|------|
| `row:0` ~ `row:3` | 0-index 행 |
| `col:0` ~ `col:3` | 0-index 열 |
| `diag:main` | 주대각선 |
| `diag:anti` | 부대각선 |

---

## 6. 성공 기준 (Acceptance Criteria)

| # | 기준 | Mom Test 증거 |
|---|------|---------------|
| AC1 | 단일 Command로 **10선** 합 검증 완료 (행 4 + 열 4 + 대각 2) | “행·열·**대각선** 합 맞췄는데 **대각선 하나를 빼먹어서**” |
| AC2 | 합 ≠ 34 격자 → `ok=false`, **최소 1개 틀린 줄** 명시 | “**34가 안 맞아 20분** 날렸다” → 즉시 재현 |
| AC3 | 정답 완성 격자 → `ok=true`, 10선 모두 sum=34 | Green 기준 |
| AC4 | 빈칸(0) 포함 → `status=incomplete`, pass 아님 | 미완성 판정 |
| AC5 | Test Loop: Red·Green 케이스 **자동 재현** | “맞는지 **판정하지 못하고**” 같은 시도 반복 방지 |
| AC6 | 실패 시 **어느 줄**이 34가 아닌지 Output에 명시 (10선 전부 검사, 줄 누락 없음) | “**10줄 중 어느 줄**이 34가 아닌지 한 번에 보는 방법이 없었다” |

---

## 7. 8계층 매핑 (세션 3)

| 계층 | PRD 대응 | 산출물 (예) |
|------|----------|-------------|
| **Rule** | §3.2 R1~R5 | `rules.md` 또는 `validator` docstring |
| **Command** | §4.1 F2~F4 | `validate_lines(grid)` |
| **(Skill)** | §4.1 F7 | pytest 실행 Skill *(선택)* |
| **Test Loop** | §4.1 F5~F6 | `tests/test_validator.py` |

**후속 세션:** Entity (`MagicSquare`, `Cell`), Control (`MissingFinder`, `Solver`), Boundary (`GridUI`, `ResultDisplay`)

---

## 8. 테스트 케이스 (Test Loop)

| ID | 유형 | 설명 | 기대 |
|----|------|------|------|
| T1 | Green | 과제 슬라이드 **정답** 4×4 (빈칸 7, 8) | `ok=true`, `status=pass` |
| T2 | Red | 한 행 합 ≠ 34 (예: 3행 sum=33) | `ok=false`, `row:2` 포함 |
| T3 | Red | 빈칸(0) 1개 이상 | `status=incomplete` |
| T4 | Red | 대각선만 ≠ 34 (행·열은 34) | `diag:main` 또는 `diag:anti` 명시 |
| T5 | Red | 여러 줄 동시 실패 | 모든 틀린 줄 ID + sum 반환 |

---

## 9. 리스크 및 미확정

| 항목 | 상태 | 조치 |
|------|------|------|
| 20분 동안 **구체적 행동** (행·열만 vs 빈칸 값 변경) | 미수집 ([Report/01.REPORT.md](../Report/01.REPORT.md) 추궁 미응답) | Mom Test 추궁 1회 |
| “34 아님” vs “어느 줄” **건수 분리** | 시뮬레이션만 | 추가 인터뷰 또는 Turn 4 |
| 1~16 유일성 검증 | Out of scope | PRD v0.2 |
| 프로젝트 스캐폴딩 (`pyproject.toml`, `src/`) | 삭제됨 | 구현 시 복원 |

---

## 10. 세션 4 — Entity 요구사항 (ARRR · Track B)

### 10.1 FR-LOC-01 — 빈칸 좌표 탐색

| ID | 계층 | 요구사항 | 우선순위 |
|----|------|----------|----------|
| **FR-LOC-01** | Entity | 4×4 격자에서 **빈칸(0) 좌표**를 **1-index row-major** 순으로 반환한다 | P0 |

**판단 문구 (C2C Rule 1):** "격자에 빈칸이 **정확히 2개**일 때, 좌표 목록이 **row-major 오름차순**으로 반환된다."

**대상 함수:** `find_blank_coords(grid: list[list[int]]) -> list[tuple[int, int]]`

**Test ID:** D-LOC-01

### 10.2 G1 격자 SSOT (픽스처·테스트 공통)

| 항목 | 값 |
|------|-----|
| 격자 (0-index `grid[row][col]`) | 아래 4×4 |
| 빈칸 0-index | `(1, 2)`, `(3, 3)` |
| 빈칸 **1-index row-major** | `(2, 3)`, `(4, 4)` |
| 픽스처 | `tests/conftest.py` → `grid_g1` |
| 상수 | `src/entity/constants.py` |

```text
[[16,  3,  2, 13],
 [ 5, 10,  0,  8],
 [ 9,  6,  7, 12],
 [ 4, 15, 14,  0]]
```

### 10.3 Track B RED 설계 (참고)

| Test ID | 대상 함수 | Given→Then | Invariant |
|---------|-----------|------------|-----------|
| D-LOC-01 | `find_blank_coords()` | G1 → `[(2,3),(4,4)]` | I6 row-major |
| D-MIS-01 | `find_not_exist_nums()` | G1 → `[7,10]` 오름차순 | I7, I11 |
| D-VAL-01 | `is_magic_square()` | G0 완전 → True | I1~I5 |
| D-SOL-01 | `solution()` | G1 Step A 성공 | I8 |

### 10.4 ECB (Entity)

- entity는 boundary/control **import 금지**
- **E001~E005** raise/return **금지** (에러 코드는 boundary)

---

## 11. 참고 문서

| 문서 | 설명 |
|------|------|
| [Report/01.REPORT.md](../Report/01.REPORT.md) | STEP 1 Mom Test 인터뷰 (7.5/10) |
| [Report/02.REPORT.md](../Report/02.REPORT.md) | STEP 1 보완 — 역할 분리 시뮬레이션 (8.5/10) |
| [Report/03.REPORT.md](../Report/03.REPORT.md) | STEP 1 + 세션 3 워크북 (R-G-I-O) |
| [Prompting/03.Export-Transcript.md](../Prompting/03.Export-Transcript.md) | 세션 3 워크북 대화 Export |

---

*PRD v0.2 — 세션 3 validate_lines + 세션 4 Entity FR-LOC-01 (ARRR).*
