# MagicSquare_xx STEP 3 — TDD Harness·Rule·Command보내기

STEP 3 Test Loop용 Harness, `.cursorrules`, Cursor Command(`tdd-red`, `export-report`) 구축 세션 후 Report·Prompt Export를 저장할 때 사용한다.

**관련 보고서:** [Report/STEP3_TDD_Harness_Report.md](../Report/STEP3_TDD_Harness_Report.md)

---

## 프롬프트

```
Report 폴더와 Prompt 폴더에 보고서와 프롬프트 저장
```

---

## 기대 산출물

| 경로 | 용도 |
|------|------|
| `Report/STEP3_TDD_Harness_Report.md` | Harness·Rule·Command 구축 세션 보고서 |
| `Prompt/STEP3_TDD_Harness_Report_Export.md` | 본 파일 (보내기 프롬프트) |

---

## Report 포함 섹션

1. 메타 정보 (프로젝트, 단계, 작성일, STEP 3 워크북 Report 근거)
2. 요약
3. 핵심 결정·산출물 (도메인·API, TDD 규칙, 파일 목록)
4. 세션별 상세 (Harness 1·2차, `.cursorrules` ECB, Command, 8계층 연결)
5. 다음 단계

---

## 확장 프롬프트 (선택)

```
MagicSquare_xx STEP 3 Test Loop용 인프라를 구축한 뒤 Report/Prompt에 저장해줘.

포함할 작업:
- Harness: pyproject.toml(pytest), src/validate_lines.py(스tub), tests/test_validate_lines.py(import만)
- .cursorrules: 4×4·0=빈칸·1~16·34·10선, validate_lines API, ECB, TDD(RED=tests/만), AI(한국어·Phase·commit)
- Harness를 커서룰에 맞게 갱신 (MAGIC_CONSTANT, LINE_IDS, -> dict)
- .cursor/commands/tdd-red.md (RED 전용)
- .cursor/commands/export-report.md (Report+Prompt 범용 Export)

Report: Report/STEP3_TDD_Harness_Report.md
Prompt: Prompt/STEP3_TDD_Harness_Report_Export.md
기존 STEP3_Session_Workbook_Report.md는 덮어쓰지 마.
구현·RED 테스트 본문은 아직 없음으로 명시해.
```
