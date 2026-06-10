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

*본 PRD는 MagicSquare_xx Logic Track의 단일 진실 공급원이다.*
