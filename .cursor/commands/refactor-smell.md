# refactor-smell — ARRR R단계 (Refine ⑦) 코드 스멜 탐지

**추가 입력 없이 즉시 실행.** 사용자가 `/refactor-smell`만 입력했다.
분석 대상은 **`src/`·`tests/`·`entity/`** 현재 코드와 **`.cursorrules`**이다. 추가 질문·확인 요청 금지.

**역할:** ARRR **R단계(Refine ⑦)** — 코드 스멜을 **탐지·분류·우선순위화**만 한다. **코드 수정·git commit 금지.**

**한국어**로 응답한다.

**Skill:** **magic-square-tdd** Skill이 있으면 **자동으로 읽고 따른다** — ECB·상수·명명 규칙 판단 시 Skill 우선.

---

## SSOT

| 우선순위 | 경로 | 용도 |
|----------|------|------|
| 1 | `.cursorrules` | API·ECB·TDD |
| 2 | `docs/PRD.md` | FR 계약 |
| 3 | `entity/constants.py` | Magic Number 판단 |
| 4 | `/golden-master` 산출 | golden harness 유무 |

---

## 필수 선언 (응답 첫 줄)

```
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI
```

---

## 전제 (게이트) — 미충족 시 **즉시 중단**

1. 아래 명령을 **실행**한다.

```
python -m pytest tests/ -v
```

2. **전부 PASS**가 아니면 스멜 분석을 **하지 않고** 중단한다.

```
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI

pytest: N failed — Refine ⑦ 중단. GREEN(/green-minimal) 후 재실행.
```

3. PASS일 때만 스멜 표·후보를 출력한다.

---

## 절차

1. `python -m pytest tests/ -v` 실행 → PASS 확인.
2. `src/`·`tests/`·`entity/` 소스를 읽고 스멜 후보를 수집한다.
3. 아래 **스멜 표**를 채운다 (발견 없으면 「없음」 행 1개).
4. **Change Budget** 이내로 `/refactor-safe`에 넘길 후보 **1~3개**를 선정한다.
5. 다음 안내 문구를 출력한다 (코드 수정 없음).

---

## 스멜 표 (출력 필수)

| 우선순위 | 스멜 유형 | 위치 (파일:행·심볼) | 근거 (한 줄) | Change Budget 적합 |
|----------|-----------|---------------------|--------------|-------------------|
| P0 / P1 / P2 | Long Method | | | 파일≤3 · 클래스≤1 · 메서드≤3 |
| | Duplicated Code | | | |
| | Mysterious Name | | | |
| | Magic Number | | | |
| | ECB 위반 | | | |
| | Feature Envy | | | |

### 우선순위 기준

| 등급 | 기준 | 예 |
|------|------|-----|
| **P0** | 테스트·ECB·상수 SSOT를 **직접 위협** | `entity`가 `control` import, `34` 리터럴, 50줄+ 단일 함수 |
| **P1** | 가독성·중복 — 동작은 녹색 유지 가능 | 동일 합산 루프 2회, 불명확 변수명 |
| **P2** | 미미·선택적 | 주석 부족, 사소한 명명 |

### 스멜 유형 정의

| 유형 | 탐지 기준 |
|------|-----------|
| **Long Method** | 한 함수·메서드가 **한 가지 일** 이상 담당하거나 과도한 길이 (MagicSquare: ~25줄 이상 경고) |
| **Duplicated Code** | 동일·유사 로직이 2곳 이상 (행/열/대각 합산 등) |
| **Mysterious Name** | `x`, `tmp`, `data` 등 의도 불명; 도메인 용어(`line_id`, `grid`) 미사용 |
| **Magic Number** | `entity/constants.py` 밖 리터럴 `34`·`16`·`4`·`10` |
| **ECB 위반** | Entity↔Control↔Boundary import·책임 침범 (`.cursorrules`·Skill) |
| **Feature Envy** | 한 모듈이 다른 계층 데이터·로직에 과도하게 의존 |

---

## Change Budget (후보 선정 상한)

`/refactor-safe` 한 번에 넘길 리팩터는 아래를 **동시에** 넘지 않는다.

| 항목 | 상한 |
|------|------|
| **파일** | ≤ 3 |
| **클래스** | ≤ 1 |
| **메서드** | ≤ 3 |

후보 표에 각 항목의 예상 소비(파일 N, 클래스 N, 메서드 N)를 적는다.

---

## `/refactor-safe` 후보 (1~3개)

스멜 표에서 Change Budget에 맞는 항목만 골라 **별도 표**로 출력한다.

| # | 우선순위 | 스멜 | 대상 | 예상 Budget (파일/클래스/메서드) | refactor-safe 지시 한 줄 |
|---|----------|------|------|----------------------------------|--------------------------|
| 1 | P0 | Magic Number | `src/validate_lines.py` | 1 / 0 / 1 | `MAGIC_CONSTANT` import로 치환 |
| 2 | | | | | |
| 3 | | | | | |

발견이 없으면:

```
후보 없음 — 녹색 유지, Refine 생략 가능.
```

---

## 다음 안내 (응답 마지막)

**P0가 있으면 1개만** 골라 `/refactor-safe`를 실행하라고 안내한다.

```
다음: P0 후보 #1 만 골라 /refactor-safe 실행 (한 번에 1건).
```

P0가 없으면 P1 1개, P1도 없으면 「후보 없음」 또는 P2 1개(선택)를 안내한다.

---

## 보고 형식 (PASS·분석 완료 시)

```
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI

- pytest: N passed — 게이트 통과
- 스멜: P0=n, P1=n, P2=n
- refactor-safe 후보: #1 … (#2, #3)
- 변경: 없음 (탐지만)
```

---

## 금지

| 금지 | 이유 |
|------|------|
| **코드 수정** (`src/`·`tests/`·`entity/`) | Refine ⑦는 탐지만 |
| **git commit** | `/refactor-safe` 이후·사용자 요청 시 |
| pytest **실패 상태**에서 스멜 분석 | 게이트 미통과 |
| Change Budget **초과** 후보를 한꺼번에 추천 | 1 safe 리팩터 = 1건 |
| GREEN·RED 단계 혼합 | Phase 분리 |

---

## 이전·다음 Command

| Command | 역할 |
|---------|------|
| `/green-minimal` | GREEN — 최소 구현·PASS |
| **`/refactor-smell`** | **Refine ⑦ — 스멜 탐지 (수정 없음)** |
| `/refactor-safe` | Refine ⑧ — 후보 1건 안전 리팩터 + pytest 유지 |

---

## 참고

- 도메인·ECB: `.cursorrules`
- 상수 SSOT: `entity/constants.py`
- TDD 금지: assert 완화·skip·xfail (`green-minimal`·`tdd-red`)
