# MagicSquare_xx — STEP 3 TDD Harness·Rule·Command 구축

| 항목 | 내용 |
|------|------|
| 프로젝트 | MagicSquare_xx (4×4 부분 마방진) |
| 단계 | STEP 3 — Test Loop 인프라 (Harness, Cursor Rule, Command) |
| 작성일 | 2026-06-10 |
| 근거 | [STEP3_Session_Workbook_Report.md](./STEP3_Session_Workbook_Report.md), 본 세션 대화 |

---

## 1. 요약

STEP 3 Test Loop를 시작하기 위해 `validate_lines` TDD용 **최소 Harness**를 만들고, **`.cursorrules`**로 도메인·API·ECB·TDD·AI 규칙을 고정했다. Harness는 커서룰에 맞게 Entity 상수(`MAGIC_CONSTANT`, `LINE_IDS`)와 API 시그니처를 반영했으며, **`/tdd-red`**·**`/export-report`** Cursor Command를 추가했다. `validate_lines` 구현과 RED 테스트 본문은 아직 작성하지 않았다.

---

## 2. 핵심 결정·산출물

### 도메인·API (`.cursorrules` + Harness)

- 4×4 격자, `0` = 빈칸, 채워진 칸 `1~16`, 마법상수 **34**
- 검증 **10선**: R1~R4, C1~C4, D1(좌하→우상), D2(우하→좌상)
- API: `validate_lines(grid) -> {"status": "pass"|"fail"|"incomplete", "failed_lines": [...]}`

### TDD 규칙

- RED → GREEN → REFACTOR; **RED은 `tests/`만** 수정
- assert 완화·skip·xfail 금지
- AI: 한국어, TDD 시 첫 줄 `Phase:` 선언, git commit은 사용자 요청 시만

### 생성·수정 파일

| 경로 | 용도 |
|------|------|
| `pyproject.toml` | pytest (`pythonpath = ["."]`) |
| `src/__init__.py` | 패키지 (빈 파일) |
| `src/validate_lines.py` | Entity 상수 + `validate_lines` 스tub |
| `tests/__init__.py` | 패키지 (빈 파일) |
| `tests/test_validate_lines.py` | import만 (테스트 함수 없음) |
| `.cursorrules` | ECB·도메인·API·TDD·AI 규칙 (~47줄) |
| `.cursor/commands/tdd-red.md` | `/tdd-red` — validate_lines RED 전용 |
| `.cursor/commands/export-report.md` | `/export-report` — Report + Prompt Export |

---

## 3. 세션별 상세

### 3.1 Harness (1차 — 골격)

- pytest만 설정한 `pyproject.toml`
- `validate_lines(grid)` 시그니처만 (`pass`)
- 테스트 파일은 import 줄만

### 3.2 `.cursorrules` (ECB)

| 계층 | 내용 |
|------|------|
| **Entity** | 격자·빈칸·마법상수·10선 ID |
| **Control** | `status` 판정 규칙, D1·D2 구분 |
| **Boundary** | API 스키마, 파일 경로, 범위 밖(UI·솔버 등) |
| **TDD / AI** | Phase 루프, RED 제약, 한국어·commit 규칙 |

### 3.3 Harness (2차 — 커서룰 반영)

`src/validate_lines.py`에 ECB 주석 구역:

- `MAGIC_CONSTANT = 34`
- `LINE_IDS` (R1~R4, C1~C4, D1, D2)
- `validate_lines(grid) -> dict` + 반환 스키마 docstring

### 3.4 Command

**`/tdd-red`**

- Phase 선언, AAA 절차, pytest 예시(pass / incomplete), 보고 형식
- 금지: `src/` 수정, assert 완화, RED당 테스트 1개 초과

**`/export-report`**

- 현재 채팅에서 주제·산출물 자동 추출
- `Report/{이름}_Report.md` + `Prompt/{이름}_Report_Export.md` 2개 생성
- 기존 파일 덮어쓰기 금지 (`-v2` 접미사)

### 3.5 8계층 연결 (STEP 3 워크북 대비)

| 계층 | 이번 세션 산출 | 상태 |
|------|----------------|------|
| **Rule** | `.cursorrules` | ✅ 초안 |
| **Command** | `tdd-red`, `export-report` | ✅ RED·Export |
| **(Skill)** | — | 미작성 |
| **Test Loop** | Harness + `tdd-red` | ⏳ RED 테스트 미작성 |

---

## 4. 다음 단계

- `/tdd-red`로 `validate_lines` **첫 RED** 테스트 추가 (예: 완성 마방진 `pass`)
- GREEN: `src/validate_lines.py` 최소 구현
- Command 보완: `green-minimal`, `/export` 별칭 (선택)
- STEP 3 워크북의 `/verify-magic-square` Command (미착수)

---

*본 보고서는 Report/STEP3_TDD_Harness_Report.md — STEP 3 TDD Harness·Rule·Command 구축 세션 정리본이다.*
