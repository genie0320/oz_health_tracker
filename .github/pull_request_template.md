<!--
CONTRIBUTING.md §4 규칙: 제목은 [T-ID] 작업 내용 요약 형식으로.
예) [T-MED-1] 알약 사진 업로드 + 후보 리스트 UI
-->

## 무엇을 했는지

- 관련 T-ID:
- TRD 성공요건 중 충족한 것 (체크리스트로):
  - [ ]
  - [ ]

## 어떻게 테스트했는지

- [ ] 새/변경된 기능에 대한 테스트를 같은 PR에 포함했다 (`CODING_RULES.md` §4, `CLAUDE.md` 완료 체크리스트 — 테스트 없는 기능 코드는 미완성)
- [ ] 로컬에서 `ruff check` / `ruff format --check` / `pytest` (백엔드) 또는 `npm run lint` / `npm run format:check` / `npm run build` (프론트)를 통과했다
- 스크린샷/GIF (UI 변경이 있다면):

## 영향 범위

- [ ] 이 PR은 한 도메인/스쿼드 범위 안에서만 파일을 수정했다 (파일명 접두어 기준, `CODING_RULES.md` 2번)
- [ ] `services/`의 공통모듈(safety/user_health_context/recognition/notification) 또는 프론트 공통모듈(`api/client.ts`, `hooks/useAuth.ts` 등)을 수정했다면 `[공통모듈]` 태그를 제목에 붙이고 담당자/다른 스쿼드에게 리뷰를 요청했다
- [ ] PR은 200~300줄 이내로 작게 유지했다 (또는 왜 더 큰지 설명)
