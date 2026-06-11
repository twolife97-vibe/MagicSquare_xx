# MagicSquare_1004

4×4 **부분 마방진**(빈칸 2개, 1~16, 합 34) 학습자가 빈칸을 채운 뒤 **행·열·대각선 10선**의 합이 34인지 빠르게 확인하고, 틀렸을 때 **어느 줄**인지 바로 짚을 수 있게 하는 검증 도구입니다.

> **한 줄 요약:** 빈칸을 채운 직후, 10선 합 34 여부를 한 번에 판정하고 실패 줄을 명시한다.

---

## 빠른 시작

```bash
# 의존성 (개발)
pip install -e ".[dev]"

# 전체 테스트 (현재 4 passed)
python -m pytest tests/ -v

# PyQt6 검증 GUI (선택)
pip install -e ".[ui]"
python -m src.boundary.validation_app
```

| 명령 | 설명 |
|------|------|
| `python -m pytest tests/ -v` | Logic + Boundary 회귀 테스트 |
| `python -m pytest tests/entity/ -v` | Track B — D-LOC-01 Golden |
| `UPDATE_GOLDEN=1 python -m pytest tests/entity/test_d_loc_01.py -v` | Golden 기준 갱신 |

---

## 배경

Mom Test 인터뷰에서 확인된 실제 문제:

> "지난주 OO 과제에서 빈칸 2개 넣고 행·열·대각선 합 맞췄는데 **대각선 하나를 빼먹어서 20분 날렸다.**"

학습자의 고통은 **풀기**보다 **맞는지 확인**하는 데 있습니다. 10줄 검산을 4~5회 반복하며 10분 이상 소요되고, "34가 아니다"는 알지만 **어느 줄**인지 한 번에 보기 어렵습니다.

---

## 이번 릴리스 범위

### 세션 3 — validate_lines

| 포함 | 설명 |
|------|------|
| **Rule** | R1~R5 — 10선 합 34 검증 규칙 |
| **Command** | `validate_lines(grid)` — 10선 검사 + pass/fail + 실패 줄 반환 |
| **Test Loop** | Red/Green 테스트로 성공·실패 재현 |

### 세션 4 — ARRR · Dual-Track TDD

| 포함 | 설명 |
|------|------|
| **ARRR** | Ask=RED → Respond=GREEN → Refine=REFACTOR → Repeat |
| **Track B (Logic)** | Entity — `FR-LOC-01` `find_blank_coords` (D-LOC-01) · Golden Master |
| **Track A (UI)** | Boundary — `InputHandler` 입력 검증 (U-IN-01·02) |
| **Skill** | `magic-square-tdd`, `magic-square-docs` |
| **Command** | `/red-test-plan` ~ `/refactor-safe`, `/export` |

### 세션 6 — PyQt 검증 GUI (프로토타입)

| 포함 | 설명 |
|------|------|
| **GridUI** | 4×4 `QSpinBox` 격자 — `set_grid` / `get_grid` |
| **ResultDisplay** | pass / fail / incomplete + `failed_lines` 표시 |
| **validation_app** | `InputHandler` → `validate_lines` 파이프라인 GUI |

#### Dual-Track

| Track | Layer | Test ID | Mock | 테스트 경로 |
|-------|-------|---------|------|-------------|
| **B — Logic** | entity | `D-*` | Domain Mock **금지** | `tests/entity/` |
| **A — UI** | boundary | `U-*` | Domain Mock **허용** | `tests/boundary/` |

| 제외 (의도적) | 이유 |
|---------------|------|
| Solver (`solution`) | 표면 솔루션 — 후속 세션 |
| 1~16 중복·누락 검증 | 합 34·좌표 탐색에 집중 |
| PyQt UI 자동화 테스트 | GUI 프로토타입만 GREEN — UI 신규 pytest 없음 |

---

## 도메인 규칙

| 규칙 | 설명 |
|------|------|
| 격자 | 4×4 정수 배열 |
| 값 | `0` = 빈칸, `1~16` = 채워진 칸 |
| 빈칸 | 정확히 2개 (0) |
| 마법 상수 | **34** |
| 10선 | 행 4 + 열 4 + 주대각(main) 1 + 부대각(anti) 1 |

### 검증 Rule (R1~R5)

| ID | Rule | 실패 조건 |
|----|------|-----------|
| R1 | 각 **행** 합 = 34 | `sum(row[i]) ≠ 34` |
| R2 | 각 **열** 합 = 34 | `sum(col[j]) ≠ 34` |
| R3 | **주대각선** 합 = 34 | `sum(main_diag) ≠ 34` |
| R4 | **부대각선** 합 = 34 | `sum(anti_diag) ≠ 34` |
| R5 | 빈칸(0) 존재 시 완성 검증 불가 | `0 in grid` → `incomplete` |

---

## 핵심 API

```python
def validate_lines(grid: list[list[int]]) -> ValidationResult: ...
```

### 입력

```text
grid: list[list[int]]  # 4×4, 값 0 또는 1~16
```

**예시 (과제 정답):**

```python
grid = [
    [16,  3,  2, 13],
    [ 5, 10, 11,  8],
    [ 9,  6,  7, 12],
    [ 4, 15, 14,  1],
]
```

### 출력

```python
ValidationResult = TypedDict(
    status: str,           # "pass" | "fail" | "incomplete"
    failed_lines: list[str]  # fail 시만 채움, pass/incomplete 시 []
)
```

| status | failed_lines | 의미 |
|--------|--------------|------|
| `"pass"` | `[]` | 10선 모두 합 34 |
| `"fail"` | `["R2", "C2", ...]` | 합 ≠ 34인 줄 ID 목록 |
| `"incomplete"` | `[]` | 빈칸(0) 존재 — R1~R4 검증 생략 |

**줄 ID:** `R1`~`R4`(행), `C1`~`C4`(열), `D1`(주대각), `D2`(부대각)

**예시 (T2 — R2·C2 교차 셀 10→11):**

```python
{"status": "fail", "failed_lines": ["R2", "C2"]}
```

### Entity API (세션 4 · Track B)

```python
def find_blank_coords(grid: list[list[int]]) -> list[tuple[int, int]]: ...
```

- **FR-LOC-01:** 4×4 격자에서 빈칸(0) 좌표를 **1-index row-major** 순으로 반환
- **Test ID:** D-LOC-01 — G1 → `[(2, 3), (4, 4)]`
- **ECB:** entity는 boundary/control import 금지, **E001~E005 emit 금지**

### Boundary API (Track A)

```python
class InputHandler:
    def validate(self, grid: list[list[int]] | None) -> InputResult: ...

class GridUI(QWidget):
    def set_grid(self, grid: list[list[int]]) -> None: ...
    def get_grid(self) -> list[list[int]]: ...

class ResultDisplay(QWidget):
    def show_input_error(self, error_code: str) -> None: ...
    def show_validation(self, result: ValidationResult) -> None: ...
```

| Test ID | Given | Then |
|---------|-------|------|
| U-IN-01 | `grid=None` | `error_code == "E003"` |
| U-IN-02 | 4×4, 셀 값 `17` | `error_code == "E002"` |

**GUI 파이프라인:** `GridUI.get_grid()` → `InputHandler.validate()` → `validate_lines()` → `ResultDisplay.show_*()`

### G1 격자 SSOT (`tests/conftest.py` → `grid_g1`)

```text
[[16,  3,  2, 13],
 [ 5, 10,  0,  8],
 [ 9,  6,  7, 12],
 [ 4, 15, 14,  0]]
```

| 항목 | 값 |
|------|-----|
| 빈칸 0-index | `(1, 2)`, `(3, 3)` |
| 빈칸 1-index row-major | `(2, 3)`, `(4, 4)` |
| 상수 | `src/entity/constants.py` (`MAGIC_CONSTANT`, `GRID_SIZE`, `MAX_CELL_VALUE`, `BLANK_CELL`, `BLANK_COUNT`) |

---

## 사용 시나리오

1. 학습자가 4×4 격자에 빈칸 2칸을 1~16 값으로 채운다.
2. `validate_lines(grid)` 한 번으로 10선 합을 검사한다.
3. **통과** → 완료. **실패** → 반환된 줄 ID로 해당 칸만 수정한다.
4. Test Loop로 같은 실패·성공을 재현한다 (Red → Green).

### 예시 격자 (과제 기준, 빈칸 위치: (1,3), (2,2))

| | | | |
|---|---|---|---|
| 16 | 3 | 2 | 13 |
| 5 | 10 | 11 | **?** |
| 9 | 6 | **?** | 12 |
| 4 | 15 | 14 | 1 |

---

## 성공 기준

| # | 기준 |
|---|------|
| AC1 | 단일 Command로 **10선** 합 검증 완료 |
| AC2 | 합 ≠ 34 → `status=fail`, 최소 1개 틀린 줄 ID 명시 |
| AC3 | 정답 완성 격자 → `status=pass`, `failed_lines=[]` |
| AC4 | 빈칸(0) 포함 → `status=incomplete`, `failed_lines=[]` |
| AC5 | Test Loop: Red·Green 케이스 자동 재현 |
| AC6 | 실패 시 **어느 줄**이 34가 아닌지 명시 (`R*`/`C*`/`D1`/`D2`, 10선 누락 없음) |

---

## 테스트 케이스

### 세션 3 — validate_lines

| ID | 유형 | 설명 | 기대 | 구현 |
|----|------|------|------|------|
| T1 | Green | 과제 정답 4×4 (빈칸 7, 8) | `status=pass`, `failed_lines=[]` | *(후속)* |
| T2 | Red | R2·C2 교차 셀 10→11 | `status=fail`, `"R2"`·`"C2"` ∈ `failed_lines` | **GREEN** |
| T3 | Red | 빈칸(0) 1개 이상 | `status=incomplete`, `failed_lines=[]` | *(후속)* |
| T4 | Red | 대각선만 ≠ 34 | `"D1"` 또는 `"D2"` ∈ `failed_lines` | *(후속)* |
| T5 | Red | 여러 줄 동시 실패 | 모든 틀린 줄 ID 반환 | *(후속)* |

### 세션 4 — Dual-Track (참고)

| ID | Track | 설명 | 기대 | 구현 |
|----|-------|------|------|------|
| D-LOC-01 | B | G1 빈칸 좌표 | `[(2,3), (4,4)]` Golden | **GREEN** |
| D-MIS-01 | B | G1 미존재 숫자 | `[7, 10]` | *(후속)* |
| D-SOL-01 | B | G1 솔버 Step A | 성공 | *(후속)* |
| U-IN-01 | A | `grid=None` | `E003` | **GREEN** |
| U-IN-02 | A | 셀 값 범위 위반 | `E002` | **GREEN** |

---

## ARRR ↔ Cursor 8계층

| ARRR | 개발 활동 | Cursor | Command | 모드 |
|------|-----------|--------|---------|------|
| **A — Ask** | RED 설계·스켈레톤 | Command + Skill | `/red-test-plan` → `/red-skeleton` | Ask → Agent |
| **R — Respond** | GREEN·Golden | Command + Skill | `/green-minimal` → `/golden-master` | Agent |
| **R — Refine** | REFACTOR | Command + Skill | `/refactor-smell` → `/refactor-safe` | Ask → Agent |
| **R — Repeat** | 문서화 | Skill + Command | `/export` · `magic-square-docs` | Agent |

## 슬래시 Command 목록

| Command | ARRR | 모드 |
|---------|------|------|
| `/red-test-plan` | RED ③ 설계표 | Ask |
| `/red-skeleton` | RED ④ 스켈레톤 | Agent |
| `/green-minimal` | GREEN | Agent |
| `/golden-master` | Golden Master | Agent |
| `/refactor-smell` | REFACTOR ⑦ 스멜 | Ask |
| `/refactor-safe` | REFACTOR ⑧ 실행 | Agent |
| `/export` · `/export-session` | Repeat | Agent |
| `/tdd-red` | RED (세션 3 단순) | Agent |
| `/pytest-validate` | Test Loop | Agent |
| `/review-rules` | Rule 리뷰 | Ask |

## 브랜치 전략 (ARRR)

```
main → staging → spec → red → green → refactoring → new_features
```

| 브랜치 | ARRR | 수정 범위 |
|--------|------|-----------|
| `spec` | 준비 | docs, .cursor/, Harness |
| `red` | Ask=RED | `tests/`만 |
| `green` | Respond | `src/` + 해당 tests |
| `refactoring` | Refine | 구조 개선 (계약 불변) |

## 프로젝트 구조

```
MagicSquare_1004/
├── .cursor/
│   ├── commands/              # 슬래시 Command (ARRR)
│   └── skills/                # magic-square-tdd, magic-square-docs
├── docs/PRD.md
├── src/
│   ├── validate_lines.py      # 10선 검증 (세션 3)
│   ├── entity/
│   │   ├── constants.py       # MAGIC_CONSTANT, GRID_SIZE, BLANK_CELL …
│   │   └── find_blank_coords.py
│   └── boundary/
│       ├── input_handler.py   # E002/E003 입력 검증
│       ├── grid_ui.py         # 4×4 QSpinBox 격자
│       ├── result_display.py  # 검증 결과 표시
│       └── validation_app.py  # PyQt GUI 진입점
├── tests/
│   ├── conftest.py            # GRID_G1 · grid_g1 (G1 SSOT)
│   ├── _approval.py           # Golden Master harness
│   ├── golden/                # Approval 기준 파일
│   ├── test_validate_lines.py # T2
│   ├── entity/                # Track B (D-*)
│   └── boundary/              # Track A (U-*)
├── Report/
├── Prompting/
└── pyproject.toml             # [dev]=pytest, [ui]=PyQt6
```

---

## 문서

| 문서 | 설명 |
|------|------|
| [docs/PRD.md](docs/PRD.md) | 제품 요구사항 (Rule · Command · Test Loop) |
| [Report/01.REPORT.md](Report/01.REPORT.md) | Mom Test 인터뷰 (7.5/10) |
| [Report/02.REPORT.md](Report/02.REPORT.md) | 역할 분리 시뮬레이션 (8.5/10) |
| [Report/03.REPORT.md](Report/03.REPORT.md) | 세션 3 워크북 (R-G-I-O) |
| [Report/04.REPORT.md](Report/04.REPORT.md) | Cursor 실습 가이드 (8계층 → 4그룹 단순화) |
| [Report/08.REPORT.md](Report/08.REPORT.md) | Track B GREEN — D-LOC-01 `find_blank_coords` |
| [Report/09.REPORT.md](Report/09.REPORT.md) | Track B Golden — D-LOC-01 Approval Test |
| [Report/11.REPORT.md](Report/11.REPORT.md) | Track A GREEN — PyQt6 검증 GUI (`GridUI`, `ResultDisplay`) |
| [Report/12.REPORT.md](Report/12.REPORT.md) | REFACTOR Ask — `/refactor-smell` + README REFACTOR To-Do |
| [Report/13.REPORT.md](Report/13.REPORT.md) | Repeat — magic-square-docs SSOT(01) + ARRR 1사이클 Export |

---

## ARRR 실습 순서 (복붙)

```
/red-test-plan          # Ask — 설계표만
/red-skeleton           # Agent — pytest.fail 스켈레톤
/green-minimal          # Agent — 최소 구현 (green 브랜치)
/golden-master          # Agent — Golden (PASS 후)
/refactor-smell         # Ask — 스멜 표
/refactor-safe          # Agent — 스멜 1개
/export                 # Agent — Report + Transcript
```

### RED 설계 프롬프트 예시

**Track B — Entity (현재 SSOT)**

```
/red-test-plan
Phase: red | Layer: entity | Track: Logic
이번 RED 묶음: D-LOC-01 (FR-LOC-01)
(표 4블록 작성, tests/·src/ 만들지 마)
```

**Track A — Boundary (Layer만 바꿔 재사용 · 워크북)**

```
/red-test-plan
Phase: red | Layer: boundary | Track: UI
이번 RED 묶음: U-IN-01, U-IN-02
(표 4블록 작성, tests/·src/ 만들지 마)
```

| 단계 | Track B | Track A |
|------|---------|---------|
| RED 설계 | Ask + `/red-test-plan` | 동일 (Layer·Track만 변경) |
| RED 스켈레톤 | Agent + `/red-skeleton` | `tests/boundary/test_u_in_*.py` |
| GREEN | `/green-minimal` → `src/entity/` | `/green-minimal` → `src/boundary/` |

## REFACTOR To-Do

> `/refactor-smell` (Ask) 결과 · Change Budget: **파일≤3 · 클래스≤1 · 메서드≤3**

### 스멜 표

| 우선순위 | 스멜 | 위치(파일:함수) | 근거 | Change Budget 내 리팩터 후보 |
|----------|------|-----------------|------|------------------------------|
| P0 | Duplicated Code (10선 합 반복) | validate_lines.py:validate_lines (L21–33) | 행·열·D1·D2 검증이 동일 패턴 4회 | `_collect_failed_line_ids(grid)` 추출 (파일 1 · 메서드 ≤2) |
| P1 | Long Method | validate_lines.py:validate_lines (L13–38) | 본문 ~26줄, 책임 3+ | P0 헬퍼 추출과 연계 (파일 1 · 메서드 1) |
| P1 | Duplicated Code | validation_app.py:GRID_G1 ↔ conftest.py:GRID_G1 | G1 격자 이중 정의 | entity 공유 모듈로 단일화 (파일 ≤3) |
| P2 | Magic Number | conftest.py:grid_g1 (L23) | cell == 0 리터럴 | BLANK_CELL 교체 (파일 1 · 1줄) |
| P2 | Mysterious Name | validate_lines.py:validate_lines | i/j 변수명 | row_idx/col_idx rename (파일 1) |

### `/refactor-safe` 후보 (Budget 내)

| # | 우선순위 | 대상 | 작업 | Budget |
|---|----------|------|------|--------|
| 1 | **P0** | `validate_lines.py:validate_lines` | `_collect_failed_line_ids(grid)` 헬퍼 추출 — 행·열·D1·D2 4회 반복 제거 | 파일 1 · 메서드 ≤2 |
| 2 | P1 | `validate_lines.py:validate_lines` | P0 헬퍼와 연계해 Long Method 분해 | 파일 1 · 메서드 1 |
| 3 | P1 | `validation_app.py` ↔ `conftest.py:GRID_G1` | G1 격자 entity 공유 모듈로 단일화 | 파일 ≤3 |

### 다음 단계

1. **P0 1개** — 후보 #1 (`_collect_failed_line_ids` 추출)을 선택
2. `/refactor-safe` 실행 (Agent) — 계약·Golden 불변, pytest 4 passed 유지
3. 완료 후 `/refactor-smell` 재실행 → 잔여 P1·P2 순차 처리

## 후속 (예정)

| 우선순위 | 항목 | Test ID | 상태 |
|----------|------|---------|------|
| — | `validate_lines` 10선 검증 | T2 | **완료** |
| — | `find_blank_coords` + Golden | D-LOC-01 | **완료** |
| — | `InputHandler` 입력 검증 | U-IN-01·02 | **완료** |
| — | PyQt 검증 GUI 프로토타입 | — | **완료** (Report 11) |
| P0 | `validate_lines` T1·T3~T5 | T1, T3~T5 | RED 대기 |
| P1 | `find_not_exist_nums`, `solution` | D-MIS-01, D-SOL-01 | RED 대기 |
| P2 | PRD §10.5 `FR-IN-01` 공식화 | U-IN-* | 문서화 |
| P2 | `validate_lines` 10선 합 중복 리팩터 | — | `/refactor-safe` 후보 |

---

## 버전

- **버전:** 0.3
- **근거:** 세션 3~6 — validate_lines · D-LOC-01 · U-IN · PyQt GUI 프로토타입

*PRD v0.2 + Track A/B GREEN — `validate_lines`, `find_blank_coords`, `InputHandler`, `GridUI`/`ResultDisplay`/`validation_app`.*
