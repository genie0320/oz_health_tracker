import io

path = "/sessions/busy-laughing-noether/mnt/remedi_mweb_co/docs/api_spec_core_v1.yaml"
with io.open(path, encoding="utf-8") as f:
    text = f.read()

old = """openapi: 3.0.3
info:
  title: ReMedi API — Phase 1 (Core)
  version: "0.1.0"
  description: >
    Phase 1(코어) 범위의 API 명세. Auth / 문서인식(공통모듈) / 복약 / Chat(RAG) / Push구독을 포함한다.
    인증은 JWT(Access/Refresh Token, `Authorization: Bearer` 헤더)로 처리하며(2026-07, httpOnly 쿠키에서 변경),
    인증이 필요한 엔드포인트는 security: bearerAuth로 표기한다."""

new = """openapi: 3.0.3
info:
  title: ReMedi API — Phase 1 (Core)
  version: "0.2.0"
  description: >
    Phase 1(코어) 범위의 API 명세. Auth / 문서인식(공통모듈) / 복약 / Chat(RAG) / Push구독을 포함한다.
    인증은 JWT(Access/Refresh Token, `Authorization: Bearer` 헤더)로 처리하며(2026-07, httpOnly 쿠키에서 변경),
    인증이 필요한 엔드포인트는 security: bearerAuth로 표기한다.
  x-changelog:
    - version: "0.1.0"
      date: "2026-07"
      changes: "초안 — Phase 1 Core 범위 (Auth/문서인식/복약/Chat/Push구독), 인증은 httpOnly 쿠키 기반"
    - version: "0.2.0"
      date: "2026-07-06"
      changes: "인증 방식을 httpOnly 쿠키에서 JWT(Authorization: Bearer)로 전환 — securitySchemes, AuthTokenResult, /auth/refresh, /auth/logout 갱신"""

assert text.count(old) == 1, f"match count: {text.count(old)}"
text = text.replace(old, new)

with io.open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("api_spec versioned.")
