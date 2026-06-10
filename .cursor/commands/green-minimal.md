# green-minimal — ARRR R단계 (Respond = GREEN) 최소 구현

**추가 입력 없이 즉시 실행.** 사용자가 `/green-minimal`만 입력했다.
대상 **RED 묶음**·Test ID·함수명은 **직전 RED 단계 출력(`/red-test-plan` 블록 3·`/red-skeleton`·`/tdd-red`)·현재 채팅·`.cursorrules`**에서 자동 추출한다. 추가 질문·확인 요청 금지.

**역할:** ARRR **R단계(Respond = GREEN)** — **RED 1묶음**에 대해 `src/`에 **최소 구현**만 추가하고, 해당 묶음 테스트를 **PASS**시킨다. **1커밋 = 1 RED 묶음** (커밋은 사용자 요청 시만).

**한국어**로 응답한다.

**Skill:** **magic-square-tdd** Skill이 있으면 **자동으로 읽고 따른다** — 계층·상수·구현 경로가 Skill과 충돌하면 Skill 우선.

---

## SSOT (입력 순서)

| 우선순위 | 출처 | 사용 |
|----------|------|------|
| 1 | `/red-test-plan` 블록 2~3 | Test ID·Given→Then·RED 묶음·pytest 명령 |
| 2 | `/red-skeleton`·`/tdd-red` 산출 | 실패 중인 테스트 함수·assert 기대값 |
| 3 | `docs/PRD.md` | FR-005~007 status·failed_lines 계약 |
| 4 | `.cursorrules` | `validate_lines` API·status 판정·10선 |
| 5 | `entity/constants.py` | `GRID_SIZE`·`CELL_MAX`·`MAGIC_CONSTANT` 등 **유일 상수 원천** |

---

## 필수 선언 (응답 첫 줄)

```
Phase: green | Layer: entity | Track: Logic
```

Track A(boundary)·UI는 Layer·Track만 치환하고, 절차·금지·보고 형식은 동일하게 적용한다.

---

## 절차 (순서 고정)

### 1. RED 재확인

- 이번 **RED 묶음** Test ID 목록을 채팅·설계표에서 확정한다.
- 해당 테스트가 **FAIL**(`pytest.fail` 또는 assert 실패)인지 pytest로 확인한다.
- **이번 묶음 외** Test ID는 아직 GREEN 대상이 **아님**을 명시한다.

```
pytest tests/test_validate_lines.py::test_<이름> -v
```

### 2. `src/` 최소 구현

- **이번 RED 묶음을 PASS시키는 데 필요한 최소 코드만** 추가·수정한다.
- 구현 위치: `.cursorrules` — `src/validate_lines.py` (Skill·PRD에 분리 계층이 있으면 Skill 따름).
- **하드코딩·매직넘버 금지** — `34`·`16`·`4`·선 개수 등은 `entity/constants.py`에서 import.
- **이번 묶음 외 Test ID**를 한꺼번에 맞추려는 선제 구현·분기 **금지**.

### 3. `pytest.fail` 제거 · assert 교체

- 스켈레톤의 `pytest.fail("RED: …")`를 **설계표 Then**에 맞는 **assert**로 교체한다.
- AAA 주석(`# Given` / `# When` / `# Then`) 유지.
- `/tdd-red`에서 이미 assert가 있으면 **기대값 변경 없이** 구현만 맞춘다.

### 4. PASS 확인

- **묶음 내** 모든 Test ID: **PASS**
- **기존 녹색** 테스트: **회귀 없음** (파일 전체 pytest)

회귀 실패 시 **즉시 수정** — assert 완화가 아니라 구현·상수 import를 고친다.

---

## ECB · 상수 · E001~E005

| 규칙 | 내용 |
|------|------|
| **상수 SSOT** | `entity/constants.py` — 구현·테스트 모두 import; 리터럴 `34`·`16`·`4` 금지 |
| **Entity 계층** | `boundary`·`control` 패키지 **import 금지** — 도메인 상수·순수 자료만 |
| **Control** | 검증 로직; Entity 상수만 사용 |
| **Boundary** | `validate_lines` 공개 API·반환 dict 스키마 |
| **E001~E005** | 구현·테스트에서 **raise·return·emit 금지** — ECB 오류 코드는 문서 전용, 런타임에 쓰지 않음 |

E001 Entity 혼입 · E002 Control 누락 · E003 Boundary 침범 · E004 Mock 오용 · E005 계층 순서 위반 — **코드에 등장시키지 않는다.**

---

## pytest 명령

**단일 테스트** (이번 RED 묶음 1건):

```
pytest tests/test_validate_lines.py::test_d_loc_01_blank_coords_row_major -v
```

**파일 전체** (회귀·묶음 전체 확인):

```
pytest tests/test_validate_lines.py -v
```

GREEN 성공 기준: 대상 Test ID **PASSED**, 파일 전체 **0 failed**.

---

## git commit

- **사용자가 명시적으로 요청할 때만** 커밋한다.
- 권장: **1커밋 = 1 RED 묶음** — 메시지에 Test ID 나열.
- 사용자가 요청하지 않았으면 커밋 **하지 않음** (`.cursorrules`).

예시 (사용자 요청 시):

```
green: T-D-LOC-01 — incomplete when line contains blank
```

---

## 보고 형식 (PASS 확인 후)

```
Phase: green | Layer: entity | Track: Logic

- PASS: T-D-LOC-01 (test_d_loc_01_blank_coords_row_major)
- pytest: N passed — 회귀 없음
- 변경: src/validate_lines.py, tests/test_validate_lines.py
```

| 항목 | 내용 |
|------|------|
| **PASS Test ID** | 이번 묶음에서 녹색이 된 ID 목록 |
| **변경 파일** | `src/`·`tests/` 실제 수정 경로 |
| **회귀** | 실패 시 `FAIL — <한 줄>` 후 **즉시 수정**했다고 보고 |

Test ID가 여러 개면 PASS bullet을 ID마다 반복한다.

---

## 금지

| 금지 | 이유 |
|------|------|
| **이번 RED 묶음 외** Test ID 동시 해결 | 1 GREEN = 1 묶음 |
| **REFACTOR** | 별도 Phase; GREEN은 최소 통과만 |
| **assert 완화** (`==`→`in`, 조건 삭제, `pytest.fail` 유지) | TDD 우회 |
| `@pytest.mark.skip`, `xfail`, 통과 더미 | TDD 우회 |
| 하드코딩·매직넘버 | `entity/constants.py` SSOT |
| Entity가 boundary/control import | ECB 계층 |
| E001~E005 `raise`·`return`·emit | 런타임 ECB 코드 아님 |
| 사용자 미요청 **git commit** | `.cursorrules` |
| UI·솔버·범위 밖 기능 | `.cursorrules` Boundary |

---

## 이전·다음 Command

| Command | 역할 |
|---------|------|
| `/red-test-plan` | RED ③ — 설계표 |
| `/red-skeleton` | RED ④ — `pytest.fail` 스켈레톤 |
| `/tdd-red` | assert RED 추가·FAIL 확인 |
| **`/green-minimal`** | **GREEN — 최소 구현 + PASS** |
| `/golden-master` | golden 스냅샷 고정 |
| `/refactor-smell` | Refine ⑦ — 스멜 탐지 |

---

## 참고

- API: `validate_lines(grid) -> {"status": "pass"|"fail"|"incomplete", "failed_lines": [...]}`
- 규칙: `.cursorrules` Entity / Control / Boundary / TDD 루프
- RED 설계: `.cursor/commands/red-test-plan.md`
- assert 패턴: `.cursor/commands/tdd-red.md`
