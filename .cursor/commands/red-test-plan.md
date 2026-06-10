# red-test-plan — ARRR A단계 (Ask = RED ③) C2C 설계표·테스트 플랜

**추가 입력 없이 즉시 실행.** 사용자가 `/red-test-plan`만 입력했다.
세션 주제·Test ID·대상 함수는 **현재 채팅·`docs/PRD.md`·`.cursorrules`**에서 자동 추출한다. 추가 질문·확인 요청 금지.

**역할:** ARRR **A단계(Ask = RED ③)** — C2C 설계표와 테스트 플랜 **문서만** 작성한다. `tests/`·`src/`에 **파일을 생성·수정하지 않는다.**

**한국어**로 응답한다.

**Skill:** **magic-square-tdd** Skill이 있으면 **자동으로 읽고 따른다**.

---

## SSOT (단일 진실 공급원)

| 우선순위 | 경로 | 용도 |
|----------|------|------|
| 1 | `docs/PRD.md` | FR(기능 요구)·Acceptance Criteria 인용 |
| 2 | `.cursorrules` | Entity·Control·Boundary·TDD 루프 |
| 3 | 현재 채팅 | 세션 주제·이미 논의된 Test ID·격자 예시 |

PRD에 FR 번호가 없으면 `.cursorrules` 조항을 `FR-대체`로 인용하고, 채팅에서 확정된 내용만 사용한다 (추측 금지).

---

## 필수 선언 (응답 첫 줄)

```
Phase: red | Layer: {entity|boundary} | Track: {Logic|UI}
```

| 필드 | 기본값 (MagicSquare_xx Logic) | Track A 재사용 시 |
|------|-------------------------------|-------------------|
| `Layer` | `entity` | `boundary` 로만 변경 |
| `Track` | `Logic` | `UI` (Boundary·화면 검증) |

**Track A(boundary):** 본 Command는 Track B(Logic·`entity`) 기준이지만, **Layer만 `boundary`로 바꾸면** 동일 4블록·금지 목록을 그대로 재사용할 수 있다. 대상 함수·파일 경로·Mock 규칙만 Boundary·UI에 맞게 치환한다.

---

## 자동 추출 (사용자에게 묻지 말 것)

- **세션 주제**: 이번 RED가 검증하려는 동작 한 줄 (예: `validate_lines` 10선 pass 판정)
- **대상 함수**: 채팅·PRD·`.cursorrules`의 공개 API (예: `validate_lines`)
- **Test ID**: `T-{Layer약자}-{순번}` 또는 채팅에 이미 쓰인 ID 유지 (예: `T-ENT-001`)
- **RED 묶음 범위**: 이번 Ask에서 설계할 테스트 1건(또는 채팅에서 명시된 묶음)
- **격자·상수**: 4×4, `0`=빈칸, `1~16`, 마법상수 **34**, 선 ID R1~R4·C1~C4·D1·D2

---

## 출력 — 4블록 (표 형식, 순서 고정)

응답 본문은 아래 **4개 블록만** 출력한다. 코드 파일 생성 없음.

### 블록 1 — C2C (Rule1~3)

PRD FR → 할 일 1개 → Test ID·Given/When/Then을 한 행으로 연결한다.

| Rule | 항목 | 내용 |
|------|------|------|
| **Rule1** | PRD FR 인용 | `docs/PRD.md`의 FR 문장 또는 AC (없으면 `.cursorrules` Entity/Control 조항 인용) |
| **Rule2** | To-Do 1개 | 이번 RED에서 검증할 **행동 1개**만 (다음 GREEN 범위와 1:1) |
| **Rule3** | Test ID · Given / When / Then | Test ID, Given(격자·전제), When(`validate_lines` 호출), Then(기대 `status`·`failed_lines`) |

예시 (Logic·entity):

| Rule | 내용 |
|------|------|
| Rule1 | FR: 10선 모두 합 34·빈칸 없으면 `pass` (`.cursorrules` Control) |
| Rule2 | 완성 마방진 격자 1개로 `status=="pass"`, `failed_lines==[]` 검증 |
| Rule3 | **T-ENT-001** · Given: 4×4 완성 격자 · When: `validate_lines(grid)` · Then: `pass`, `[]` |

---

### 블록 2 — Track B 표 (Logic) / Track 표 (UI)

Logic Track(`entity`)일 때 **Track B** 표. UI Track일 때 동일 열로 UI 대상(컴포넌트·핸들러)을 기입한다.

| Test ID | 대상 함수 | Given → Then | Invariant | Expected RED Failure |
|---------|-----------|--------------|-----------|----------------------|
| T-ENT-001 | `validate_lines` | Given: 완성 4×4 격자 → Then: `pass`, `failed_lines==[]` | `MAGIC_CONSTANT==34`; 10선 ID 집합 고정; 빈칸 없음 | `NotImplementedError` / `assert status == "pass"` 실패 (stub·미구현) |

- **Invariant**: 테스트가 깨지면 안 되는 도메인 상수·ID·입력 형식 (Entity 고정값)
- **Expected RED Failure**: pytest FAIL 시 **한 줄** (import 오류·assert 메시지·`pass` 본문 등)

---

### 블록 3 — 테스트 플랜

| 항목 | 값 |
|------|-----|
| **파일 경로** | `tests/test_validate_lines.py` (또는 PRD·채팅에 명시된 경로) |
| **함수명** | `test_<동작_요약>` (블록 2 Test ID와 1:1 매핑) |
| **conftest 픽스처** | 없음 — 또는 `grid_pass`, `grid_incomplete_r3` 등 **순수 데이터** 픽스처만 (이름·용도 명시) |
| **pytest 명령** | `pytest tests/test_validate_lines.py::test_<이름> -v` |
| **RED 묶음 범위** | 이번 Ask 설계: Test ID 목록 (예: `T-ENT-001` 단독) — **다음 `/red-skeleton`에서 구현** |

import·AAA 주석 패턴은 `.cursor/commands/tdd-red.md`와 정합을 맞춘다.

---

### 블록 4 — ECB · Mock 점검

| 점검 항목 | Logic Track (`entity`) | UI Track (`boundary`) |
|-----------|------------------------|------------------------|
| **계층** | Entity·Control만 테스트; Boundary는 입출력 dict 스키마만 | Boundary·표시 계약; Entity 내부 mock 금지 |
| **Domain Mock** | **금지** — `validate_lines`·격자·상수를 mock/patch하지 않음 | UI는 도메인 대신 **렌더 결과·API 응답**만 검증 |
| **픽스처** | 4×4 `list[list[int]]` 실값만 | 사용자 이벤트·props 실값 |
| **ECB emit** | **E001~E005 문서·슬라이드·코드 emit 금지** (설계 단계 산출 아님) | 동일 |

**E001~E005 emit 금지** — ECB 분류 오류 코드(E001 Entity 혼입, E002 Control 누락, E003 Boundary 침범, E004 Mock 오용, E005 계층 순서 위반)를 본 단계에서 **생성·출력·파일 기록하지 않는다.** 점검은 통과/해당 없음 한 줄로만 표기한다.

| 체크 | 결과 |
|------|------|
| Domain Mock 없음 | ✅ / 해당 없음 |
| E001~E005 emit 없음 | ✅ |
| `src/` 미참조 구현 | ✅ (플랜만) |

---

## 절차

1. `docs/PRD.md`·`.cursorrules`·채팅에서 세션 주제·FR·대상 함수를 추출한다.
2. 응답 **첫 줄**에 `Phase: red | Layer: … | Track: …` 를 선언한다.
3. **블록 1~4**를 표 형식으로 채운다 (빈 칸·「TBD」 금지 — 채팅·SSOT로 채울 수 없으면 해당 FR을 명시적으로 `미정의`로 표기).
4. 마지막 줄에 완료 문구를 **정확히 한 줄** 출력한다.

---

## 완료 (응답 마지막 줄)

```
/red-skeleton 으로 넘길 준비됐다
```

---

## 금지

| 금지 | 이유 |
|------|------|
| `src/` 수정 | GREEN 단계 |
| GREEN / REFACTOR 단계 진행 | Ask(RED ③)는 설계만 |
| `@pytest.mark.skip`, `xfail`, assert 완화 | TDD 우회 |
| `tests/`·`src/` **파일 생성·수정** | `/red-skeleton`에서 수행 |
| 사용자에게 세션 주제·Test ID **추가 질문** | 자동 추출 |
| E001~E005 ECB 오류 코드 **emit** | 설계 범위 밖 |
| Logic Track에서 **Domain Mock** | 실격자·격자로 검증 |

---

## 다음 Command

| Command | 역할 |
|---------|------|
| `/red-skeleton` | 블록 3 플랜대로 `tests/`에 RED 테스트 골격·본문 작성 |
| `/tdd-red` | 단일 RED 테스트 즉시 추가 (AAA·pytest FAIL 확인) |

---

## 참고

- 도메인·API: `.cursorrules` — `validate_lines(grid) -> {"status", "failed_lines"}`
- RED AAA 예시: `.cursor/commands/tdd-red.md`
- PRD: `docs/PRD.md` (FR·AC 인용 원본)
