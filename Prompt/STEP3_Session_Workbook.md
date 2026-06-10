# STEP 3 세션 워크북 — MagicSquare_xx

STEP 1 Mom Test 결과를 바탕으로 세션 3 워크북을 채운다.  
8계층 중 이번 세션: **Rule, Command, (Skill), Test Loop** 만.

---

## 프롬프트 (워크북 채우기)

```
Mom Test 결과:
- 페르소나: [...]
- 진짜 문제 (한 문장): [...]
- Mom Test 증거 3줄: [...]
MagicSquare_xx 세션 3 워크북을 채워줘:
1) 주제 한 문장 (Mom Test 기반, 솔루션 최소화)
2) R-G-I-O (Role/Goal/Input/Output)
3) 성공 기준 3개 (Mom Test 증거와 연결)
4) 표면 문제 — 이번 프로젝트에서 하지 않을 것
8계층 중 이번 세션에서 만드는 것만: Rule, Command, (Skill), Test Loop
```

Mom Test가 이미 `Report/STEP1_MomTest_Report.md`에 있으면:

```
Report/STEP1_MomTest_Report.md를 근거로 MagicSquare_xx 세션 3 워크북을 채워줘.
```

---

## Mom Test 결과 (입력)

### 페르소나:

### 진짜 문제 (한 문장):

### Mom Test 증거 3줄:

1.
2.
3.

---

## 세션 3 워크북

### 1) 주제 한 문장 (Mom Test 기반, 솔루션 최소화)

> 

### 2) R-G-I-O

| | 내용 |
|---|------|
| **Role** | |
| **Goal** | |
| **Input** | |
| **Output** | |

### 3) 성공 기준 3개 (Mom Test 증거와 연결)

| # | 성공 기준 | 연결 증거 |
|---|-----------|-----------|
| **S1** | | |
| **S2** | | |
| **S3** | | |

### 4) 표면 문제 — 이번 프로젝트에서 하지 않을 것

- ~~
- ~~

---

## 8계층 — 이번 세션에서 만드는 것만

| 계층 | 이번 세션 산출물 | Mom Test 연결 |
|------|------------------|---------------|
| **Rule** | | |
| **Command** | | |
| **(Skill)** | | |
| **Test Loop** | | |

### 이번 세션에서 만들지 않음

Entity, Control, Boundary, UI, Solver, ECB 문서화 등.

---

## 작성 규칙

| 항목 | 쓰는 것 | 쓰지 말 것 |
|------|---------|------------|
| **주제** | Mom Test **진짜 문제**에서 파생, 검증·행동 중심 | 앱·TDD·ECB·Validator 등 솔루션 |
| **R-G-I-O** | 학습자 **Role**, 검증 **Goal**, 격자·조건·실패 패턴 **Input**, 체크 결과 **Output** | 제품 기능 명세 |
| **성공 기준** | 측정·관찰 가능, Mom Test **증거 번호**와 1:1 연결 | 「좋을 것 같다」「의향 있다」 |
| **표면 문제** | 이번 세션 **범위 밖** + STEP 1 금지 목록 | — |
| **8계층** | Rule·Command·(Skill)·Test Loop **만** | Entity·UI·Solver 등 |

---

## 권장 순서

1. **STEP 1** — [STEP1_MomTest_Report.md](../Report/STEP1_MomTest_Report.md) 확인
2. **Workbook** — 위 프롬프트로 워크북 채우기
3. **Report Export** — [STEP3_Session_Report_Export.md](./STEP3_Session_Report_Export.md)로 `Report/` 저장
