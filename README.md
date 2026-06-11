# MagicSquare_xx

4×4 **부분 마방진** 10선 검증 — Logic Track (STEP 3).

행·열·대각선 **10항**을 빠짐없이 확인하는 `validate_lines(grid)` 함수와 TDD 기반 단위 테스트.

---

## 빠른 시작

```bash
# 전체 테스트 (게이트)
python -m pytest tests/ -v

# ENT/BND RED 묶음만
python -m pytest tests/test_validate_lines.py -v
```

**요구:** Python 3.x, [pytest](https://docs.pytest.org/). `pyproject.toml`에 `pythonpath = ["."]` 설정됨.

---

## API

```python
from src.validate_lines import validate_lines

result = validate_lines(grid)
# {"status": "pass" | "fail" | "incomplete", "failed_lines": ["R1", "D2", ...]}
```

| 항목 | 규칙 |
|------|------|
| 격자 | 4×4, `0`=빈칸, 채움 `1~16` |
| 마법상수 | **34** |
| 10선 ID | `R1`~`R4`, `C1`~`C4`, `D1`(좌하→우상), `D2`(우하→좌상) |
| 판정 | `pass` — 10선 모두 합 34·빈칸 없음 / `fail` — 빈칸 없는데 합≠34 / `incomplete` — 빈칸 포함 선 존재 |

상세 FR·좌표·판정 우선순위는 [docs/PRD.md](docs/PRD.md)를 본다.

---

## 저장소 구조

```
src/validate_lines.py          # 공개 API (Control + Boundary)
tests/test_validate_lines.py   # T-ENT-*, T-BND-* (ENT/BND RED 묶음)
tests/conftest.py              # grid_pass, grid_fail_*, grid_incomplete_r3
tests/entity/                  # T-D-LOC-* (설계·RED 예정)
tests/boundary/                # U-IN-* (설계·RED 예정)
docs/PRD.md                    # FR·AC·Test ID SSOT
.cursorrules                   # ECB·TDD 실행 규칙
```

---

## 테스트 플랜 (Test ID)

Test ID 레지스트리 SSOT: [PRD §10](docs/PRD.md#10-테스트-전략).

### 명명 규칙

| Layer | 접두 | 예시 |
|-------|------|------|
| Entity (판정) | `T-ENT-` | `T-ENT-001` |
| Entity (좌표·G1) | `T-D-LOC-` | `T-D-LOC-01` |
| Entity (입력 스모크) | `T-BND-` | `T-BND-001` |
| Boundary (입력 계약) | `U-IN-` | `U-IN-01` |

### 현재 상태

| 구분 | Test ID | 파일 | 상태 |
|------|---------|------|------|
| ENT/BND | T-ENT-001 ~ 005, T-BND-001 | `tests/test_validate_lines.py` | RED 완료, GREEN 대기 |
| D-LOC | T-D-LOC-01 ~ 03 | `tests/entity/test_d_loc_01.py` | 설계만 (`grid_g1` 필요) |
| U-IN | U-IN-01 ~ 02 | `tests/boundary/test_u_in_*.py` | 설계만 |

`validate_lines`는 현재 **stub** (`pass` 본문). ENT RED 6건은 `pytest.fail("RED: …")`로 실패 예상.

### ENT/BND RED 묶음 (`tests/test_validate_lines.py`)

| 묶음 | Test ID | FR | 픽스처 | Then (요지) |
|------|---------|-----|--------|-------------|
| 1 | **T-ENT-001** | FR-006, FR-002 | `grid_pass` | `status=="pass"`, `failed_lines==[]` |
| 2 | **T-ENT-002** | FR-007 | `grid_fail_multi` | `status=="fail"`, `failed_lines==["R3","C3","D2"]` |
| 3 | **T-ENT-003** | FR-004 | `grid_fail_d2` | D1∉failed_lines, D2∈failed_lines, `status!="pass"` |
| 4 | **T-ENT-004** | FR-005 | `grid_incomplete_r3` | `status=="incomplete"`, failed_lines ⊇ {R3,C2,D1} |
| 5 | **T-ENT-005** | FR-003 | `grid_fail_multi` | `failed_lines==["R3","C3","D2"]` (LINE_IDS 순) |
| 6 | **T-BND-001** | FR-001 | `grid_pass` | dict 반환, `status`·`failed_lines` 키 존재 |

**권장 GREEN 순서:** 묶음 1 → 2 → 3 → 4 → 5 → 6 (1 묶음 = 1 GREEN 목표).

### D-LOC RED 묶음 (`tests/entity/test_d_loc_01.py` — 예정)

픽스처 `grid_g1`: 빈칸 `(1,2)`, `(3,2)`.

| Test ID | FR | Then (요지) |
|---------|-----|-------------|
| **T-D-LOC-01** | FR-005 | `status=="incomplete"` |
| **T-D-LOC-02** | FR-005 | failed_lines ⊇ {R2,R4,C3,D1} |
| **T-D-LOC-03** | FR-003 | `failed_lines==["R2","R4","C3","D1"]` |

### Boundary RED 묶음 (`tests/boundary/` — 예정)

| Test ID | Given | Then |
|---------|-------|------|
| **U-IN-01** | `grid=None` | `TypeError`, dict 반환 금지 |
| **U-IN-02** | 3행×4열 | `ValueError`, dict 반환 금지 |

### FR → Test ID 매핑

| FR | Test ID |
|----|---------|
| FR-001 | T-BND-001, U-IN-01, U-IN-02 |
| FR-002 | T-ENT-001 |
| FR-003 | T-ENT-005, T-D-LOC-03 |
| FR-004 | T-ENT-003 |
| FR-005 | T-ENT-004, T-D-LOC-01, T-D-LOC-02 |
| FR-006 | T-ENT-001 |
| FR-007 | T-ENT-002 |

### TDD 루프

| Phase | 수정 범위 | 금지 |
|-------|-----------|------|
| **RED** | `tests/`만 | `src/` 수정, skip/xfail, assert 완화 |
| **GREEN** | `src/` (+ 필요 시 `tests/`) | 다음 묶음 선해결 |
| **REFACTOR** | 구조만 | 동작·API 변경 |

ARRR Command: `/red-test-plan` → `/red-skeleton` → `/green-minimal` → …

---

## 문서

| 경로 | 용도 |
|------|------|
| [docs/PRD.md](docs/PRD.md) | 제품 요구서 (FR·AC·Test ID SSOT) |
| [docs/README.md](docs/README.md) | 문서索引·SSOT 계층 |
| [Report/STEP1_MomTest_Report.md](Report/STEP1_MomTest_Report.md) | Mom Test — 10선 검증 배경 |
| `.cursorrules` | Entity·Control·Boundary, TDD 규칙 |

**SSOT 계층:** `docs/PRD.md` → `.cursorrules` → Command·Skill

---

## 범위 밖 (Non-Goals)

UI, 솔버, 자동 채우기, ECB 슬라이드 런타임 코드.
