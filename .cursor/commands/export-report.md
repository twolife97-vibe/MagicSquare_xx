# export-report — Report 보고서 + Prompt Export 저장

**추가 입력 없이 즉시 실행.** 사용자가 `/export-report`만 입력했다.
세션 주제·산출물·대화 내용은 **현재 채팅 전체**에서 자동 추출한다. 추가 질문·확인 요청 금지.

**한국어**로 Report·Prompt를 작성하고, 응답도 한국어로 짧게 보고한다.

## 자동 추출 (사용자에게 묻지 말 것)

- **세션 주제**: 이번 대화의 핵심 작업 (예: Mom Test, STEP 3 워크북, TDD RED, Harness, Cursor Rule)
- **단계·맥락**: STEP 1 / STEP 3 / TDD / 기타 — 대화에서 추론
- **산출물**: 생성·수정된 파일 목록
- **핵심 결정·다음 단계**: 대화에서 확정된 내용만 (추측 금지)

## 파일명 규칙

1. `Report/`·`Prompt/`의 기존 `STEP*`·`*_Report*` 파일을 확인한다.
2. 이번 세션이 **기존 STEP과 동일**하면 해당 패턴을 따른다.
   - 예: STEP 1 Mom Test → `Report/STEP1_MomTest_Report.md`, `Prompt/STEP1_MomTest_Report_Export.md`
   - 예: STEP 3 워크북 → `Report/STEP3_Session_Workbook_Report.md`, `Prompt/STEP3_Session_Report_Export.md`
3. **새 주제**면 `{주제Slug}_Report.md` / `{주제Slug}_Report_Export.md` 형식을 쓴다.
   - `주제Slug`: PascalCase 또는 STEP 스타일 (예: `TDD_Harness`, `CursorRules`)
4. **같은 경로 파일이 이미 있으면 덮어쓰지 않는다.** `-v2`, `-v3` 접미사를 붙인다.

## 생성 파일 (반드시 2개)

| 파일 | 설명 |
|------|------|
| `Report/{이름}_Report.md` | 세션 요약 **보고서** (대화·산출물 정리) |
| `Prompt/{이름}_Report_Export.md` | 동일 세션을 **재실행**할 때 쓸 Export 프롬프트 |

## Report 형식 (`Report/…_Report.md`)

```markdown
# MagicSquare_xx — {세션 주제}

| 항목 | 내용 |
|------|------|
| 프로젝트 | MagicSquare_xx (4×4 부분 마방진) |
| 단계 | {자동 추출} |
| 작성일 | {오늘 날짜 YYYY-MM-DD} |
| 근거 | {선행 Report·대화 — 없으면 「본 세션 대화」} |

---

## 1. 요약
{2~4문장}

## 2. 핵심 결정·산출물
- {결정·파일·규칙 — bullet}

## 3. 세션별 상세
{STEP 1: Mom Test / STEP 3: 워크북·8계층 / TDD: Phase·테스트 등 — 대화에 맞는 섹션만}

## 4. 다음 단계
- {bullet}

---

*본 보고서는 {파일 경로} — {세션 주제} 세션 정리본이다.*
```

- Mom Test 세션: 페르소나, 진짜 문제, 증거, 표면 문제 포함
- STEP 3 세션: R-G-I-O, 성공 기준, 8계층(Rule·Command·Skill·Test Loop) 포함
- TDD 세션: Phase(RED/GREEN/REFACTOR), 대상 함수, pytest 결과 포함

## Prompt Export 형식 (`Prompt/…_Report_Export.md`)

```markdown
# MagicSquare_xx {단계} — 보고서보내기

{한 줄 설명 — 언제 이 프롬프트를 쓰는지}

---

## 프롬프트

\```
Report 폴더와 Prompt 폴더에 보고서와 프롬프트 저장
\```

---

## 기대 산출물

| 경로 | 용도 |
|------|------|
| `Report/…` | {보고서 설명} |
| `Prompt/…` | 본 파일 (보내기 프롬프트) |

---

## Report 포함 섹션

1. …
2. …

---

## 확장 프롬프트 (선택)

\```
{이번 세션을 재현하는 구체적 한 블록 프롬프트}
\```
```

- **프롬프트** 블록: `/export-report` 없이도 붙여 넣을 수 있는 **한 줄** 지시
- **확장 프롬프트**: 섹션·금지·범위를 명시한 **재현용** 상세 프롬프트

## 절차

1. `Report/`, `Prompt/` 기존 파일을 확인해 **파일명**을 정한다.
2. 현재 대화에서 주제·내용·산출물을 추출한다.
3. Report 파일을 **직접 생성**한다.
4. Prompt Export 파일을 **직접 생성**한다 (Report와 상호 링크).
5. 짧게 보고:
   - Report 경로
   - Prompt 경로
   - 세션 주제 한 줄

## 금지

- 사용자에게 세션 주제·번호·형식 **추가 질문**
- Report만 만들고 Prompt Export **생략** (또는 그 반대)
- 기존 파일 **무단 덮어쓰기**
- 대화에 없는 내용 **추측**하여 Report에 기록
- `src/`·`tests/`·`.cursorrules` 등 **무관 파일** 수정 (Export는 `Report/`·`Prompt/`만)

## 참고

- 프로젝트 프롬프트索引: `Prompt/README.md`
- 도메인·TDD 규칙: `.cursorrules`
