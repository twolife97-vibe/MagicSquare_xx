# Docs — MagicSquare_xx

4×4 부분 마방진 **`validate_lines`** Logic Track 제품·요구 문서 모음.

---

## 문서 목록

| 파일 | 용도 |
|------|------|
| [PRD.md](./PRD.md) | **제품 요구서 (SSOT)** — FR·AC·도메인·API·TDD·범위 |

---

## SSOT 계층

요구·설계·구현이 충돌할 때 아래 순서를 따른다.

```
docs/PRD.md  →  .cursorrules  →  Command · Skill · 채팅 확정
   (FR·AC)        (ECB·TDD 실행)
```

| 계층 | 경로 | 역할 |
|------|------|------|
| 1 | `docs/PRD.md` | 무엇을 만들지 — FR-001~007, 성공 기준 S1~S3, API |
| 2 | `.cursorrules` | 어떻게 지킬지 — Entity·Control·Boundary, RED/GREEN/REFACTOR |
| 3 | `.cursor/commands/`, `.cursor/skills/` | ARRR 워크플로 실행 |

`/red-test-plan` C2C **Rule1**은 [PRD.md](./PRD.md)의 **FR-00N**을 인용한다. FR에 없는 동작은 RED에 넣지 않는다.

---

## PRD 요약

| 항목 | 내용 |
|------|------|
| 제품 | `validate_lines(grid) -> {"status", "failed_lines"}` |
| 도메인 | 4×4, `0`=빈칸, `1~16`, 마법상수 **34**, 10선 R1~R4·C1~C4·D1·D2 |
| 판정 | `pass` / `fail` / `incomplete` |
| 범위 밖 | UI, 솔버, 자동 채우기 |

상세·좌표 정의·테스트 시나리오는 [PRD.md](./PRD.md) 본문을 본다.

---

## 관련 문서 (저장소)

| 경로 | 용도 |
|------|------|
| [Report/STEP1_MomTest_Report.md](../Report/STEP1_MomTest_Report.md) | STEP 1 Mom Test — PRD 배경 근거 |
| [Report/STEP3_Session_Workbook_Report.md](../Report/STEP3_Session_Workbook_Report.md) | STEP 3 워크북 — 성공 기준·R-G-I-O |
| [Report/STEP3_TDD_Harness_Report.md](../Report/STEP3_TDD_Harness_Report.md) | Harness·Rule·Command 구축 기록 |
| [Prompt/README.md](../Prompt/README.md) | 레거시 프롬프트·Export索引 |
| `.cursor/skills/magic-square-tdd/` | TDD ARRR Skill |
| `.cursor/skills/magic-square-docs/` | 세션 Report·Transcript Export |

---

## 권장 읽기 순서

1. [Report/STEP1_MomTest_Report.md](../Report/STEP1_MomTest_Report.md) — 왜 10선 검증인가
2. [PRD.md](./PRD.md) — 무엇을 구현하는가 (FR·API)
3. `.cursorrules` — TDD·ECB 실행 규칙
4. `/red-test-plan` — C2C 설계표 (FR 인용)

---

## 변경 이력

| 날짜 | 내용 |
|------|------|
| 2026-06-10 | `docs/README.md` 초안 — PRD v1.0索引 |

PRD 본문 변경 이력은 [PRD.md §12](./PRD.md#12-변경-이력)를 본다.
