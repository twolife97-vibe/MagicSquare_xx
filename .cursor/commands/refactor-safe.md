# refactor-safe — ARRR R단계 (Refine ⑧) Safe Refactor 1건

**추가 입력 없이 즉시 실행.** 사용자가 `/refactor-safe`만 입력했다.
대상 스멜은 **직전 `/refactor-smell` 후보 표에서 사용자가 고른 1건**(채팅에 번호·지시가 없으면 **P0 후보 #1**)이다. 추가 질문·확인 요청 금지.

**역할:** `/refactor-smell` 표에서 **선택한 스멜 1개만** Safe Refactor로 실행한다. 동작·계약은 유지하고 구조·명명·중복만 개선한다.

**한국어**로 응답한다.

**Skill:** **magic-square-tdd** Skill이 있으면 **자동으로 읽고 따른다** — golden 경로·Budget·ECB 규칙이 Skill과 충돌하면 Skill 우선.

---

## SSOT (입력 순서)

| 우선순위 | 출처 | 사용 |
|----------|------|------|
| 1 | 직전 `/refactor-smell` 후보 #N | 스멜 유형·대상·Budget·지시 한 줄 |
| 2 | `/refactor-smell` 스멜 표 | 위치·근거 |
| 3 | `docs/PRD.md` | FR-006~007 출력 계약 |
| 4 | `.cursorrules` | API·ECB·도메인 불변식 |
| 5 | `entity/constants.py` | 상수 SSOT (Magic Number 리팩터 시) |
| 6 | `/golden-master` | golden 경로·`-m golden` |

**한 번에 1스멜만.** 후보 2·3은 이번 실행 범위 **아님**.

---

## 필수 선언 (응답 첫 줄)

```
Phase: refactor | Layer: entity | Track: Logic
```

Track A(boundary)·UI는 Layer·Track만 치환; Safe Refactor 원칙·게이트는 동일.

---

## Safe Refactor 원칙 (계약 보존)

| 원칙 | 내용 |
|------|------|
| **입출력 불변** | 공개 API 시그니처·반환 dict 스키마·`status`/`failed_lines` 의미 변경 금지 |
| **예외 불변** | 새 예외·삼킨 예외·에러 타입 변경 금지 (리팩터는 녹색 유지) |
| **`int[6]` 1-index** | 좌표·선 인덱스 등 **1-based 계약**이 있으면 변경 금지 (해당 없으면 N/A) |
| **E001~E005** | `raise`·`return`·emit·문서화 **금지** — 런타임 ECB 코드 아님 |
| **기능·버그** | 기능 추가·버그 수정 **금지** — 별도 **GREEN**(`/green-minimal`) |
| **테스트 의미** | assert 기대값·격자 데이터 변경 금지 (구조 리팩터만; 테스트 헬퍼 추출은 Budget 내) |

MagicSquare_xx: `validate_lines(grid) -> {"status", "failed_lines"}` 및 10선 ID·`MAGIC_CONSTANT` 의미는 **불변**.

---

## Change Budget (초과 시 분할)

`/refactor-smell`과 동일 — **이번 1스멜**이 아래를 넘으면 **중단**하고 더 작은 단위로 다시 `/refactor-smell` 요청.

| 항목 | 상한 |
|------|------|
| **파일** | ≤ 3 |
| **클래스** | ≤ 1 |
| **메서드** | ≤ 3 |

---

## 절차 (순서 고정)

### 0. 게이트

```
python -m pytest tests/ -v
```

**전부 PASS**가 아니면 리팩터 **하지 않고** 중단.

### 1. 대상 확정

- `/refactor-smell` 후보 **1건** (스멜 유형·파일·심볼·지시 한 줄)을 응답에 명시한다.

### 2. Safe Refactor 실행

- Budget 이내에서 **스멜 1종류만** 해소 (예: Magic Number → `entity.constants` import).
- `src/`·`entity/`·필요 시 `tests/` **헬퍼만** (assert 의미 불변).

### 3. 검증 — pytest

```
pytest tests/ -v
```

또는:

```
python -m pytest tests/ -v
```

**0 failed** 필수. 실패 시 **롤백** 후 원인 보고 (assert 완화 금지).

### 4. 검증 — golden matched

프로젝트·Skill에 golden 스냅샷이 있으면 실행한다 (경로는 Skill·`tests/` convention 따름). 예:

```
pytest tests/ -v -m golden
```

또는 Skill에 정의된 golden 명령.

| 결과 | 조치 |
|------|------|
| **golden matched** | 완료 — **`UPDATE_GOLDEN` 사용하지 않음** |
| **golden diff — 의도적** | 리팩터 범위를 벗어난 계약 변경 **아님**이 확인되면 **ISS 문서**에 기록 + 사용자 명시 요청 시에만 `UPDATE_GOLDEN=1`로 갱신 |
| **golden diff — 비의도** | **즉시 롤백** — 리팩터 재시도 또는 `/refactor-smell` 재실행 |

golden 테스트가 **아직 없으면**: `golden matched: N/A (no golden harness)` 로 보고하고 pytest만으로 완료.

**본 Command 기본 완료 조건:** `UPDATE_GOLDEN` **없이** golden matched (또는 N/A).

### 5. ISS (의도적 golden diff 시만)

의도적 diff일 때만 `Report/` 또는 Skill이 지정한 **ISS** 경로에 한 줄 기록:

- 스멜 # · 리팩터 요약 · golden 변경 이유 · `UPDATE_GOLDEN=1`은 **사용자 요청 후** 별도 실행

---

## golden diff 판단

| 구분 | 신호 | 조치 |
|------|------|------|
| **의도적** | 리팩터로 **출력 형식·공백·순서**만 바뀌었고 API 의미는 동일; ISS에 사전 합의된 정리 | ISS 문서화 → (사용자 요청 시) `UPDATE_GOLDEN=1` |
| **비의도** | `status`·`failed_lines`·선 ID 집합·예외·인덱스 의미 변경 | **롤백** — GREEN 버그 가능성, `/green-minimal`로 분리 |

---

## 보고 형식 (완료 시)

```
Phase: refactor | Layer: entity | Track: Logic

- 스멜: #1 P0 Magic Number — entity.constants import
- 변경 요약: src/validate_lines.py — 리터럴 34 → MAGIC_CONSTANT (1파일, 0클래스, 1함수)
- pytest: N passed — 0 failed
- golden matched: yes | N/A (no golden harness)
- 변경: src/validate_lines.py
```

| 항목 | 내용 |
|------|------|
| **변경 요약** | 스멜·대상·Budget 소비·한 줄 diff 설명 |
| **pytest** | passed/failed |
| **golden matched** | yes / N/A / rollback (비의도 diff) |

---

## git commit

- **사용자가 명시적으로 요청할 때만** 커밋한다.
- 권장: **1커밋 = 1 safe 리팩터** — 메시지에 스멜 유형·후보 #.

```
refactor: #1 Magic Number — MAGIC_CONSTANT import
```

---

## 금지

| 금지 | 이유 |
|------|------|
| **스멜 2건 이상** 동시 해소 | 1 safe = 1 후보 |
| Change Budget **초과** | 분할 후 재 smell |
| **기능 추가**·**버그 수정** | GREEN |
| 입출력·예외·1-index 계약 **변경** | Safe Refactor 아님 |
| assert 완화·테스트 기대값 변경 | 동작 변경 |
| E001~E005 emit | ECB 문서 전용 |
| **`UPDATE_GOLDEN=1` 기본 사용** | 의도적 diff + 사용자 요청 시만 |
| 사용자 미요청 **git commit** | `.cursorrules` |
| pytest 실패 상태에서 리팩터 계속 | 롤백 우선 |

---

## 이전·다음 Command

| Command | 역할 |
|---------|------|
| `/refactor-smell` | Refine ⑦ — 스멜 탐지 (수정 없음) |
| **`/refactor-safe`** | **Refine ⑧ — 후보 1건 Safe Refactor** |
| `/refactor-smell` | 남은 스멜 재탐지 |
| `/green-minimal` | 동작 변경·버그 수정 필요 시 |

---

## 참고

- 스멜·Budget: `.cursor/commands/refactor-smell.md`
- ECB·API: `.cursorrules`
- 상수: `entity/constants.py`
