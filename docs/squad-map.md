# squad-map.md — 담당자 매핑 (킥오프 때 채우기)

> 목적: "이 파일/기능은 누구 담당인지"를 이슈 번호나 파일명만 보고 바로 알 수 있게 한다.
> `CONTRIBUTING.md` §2, `CODING_RULES.md` 2번, `FRONTEND_ARCHITECTURE.md` §6과 짝을 이루는 문서 — 표 구조는 그대로, 이름만 채운다.

## 1. 스쿼드 ↔ 담당자 ↔ T-그룹

레이어 우선 구조라 폴더가 아니라 **파일명 접두어**로 소유권을 나눈다 (`CODING_RULES.md` 2번).

| 스쿼드 | 담당자 | 담당 T-그룹 | 백엔드 파일 접두어 |
| --- | --- | --- | --- |
| A. 인증/보안 | _(이름)_ | T-AUTH-1~6, T-SEC-1, T-STAT-1, T-PRIV-1, T-ENC-1, T-ARCH-1 | `auth_*` |
| B. 복약인식/알림 | _(이름)_ | T-MED-1~2, T-DOC-1~3, T-NTFY-1~6, T-CARD-1 | `medication_*`, `notification_*` |
| C. 목표/추적/건강정보 | _(이름)_ | T-GOAL-1~3, T-ADH-1~3, T-GUIDE-1, T-INFO-1~3, T-TRCK-1~3, T-DIET-1~2, T-ACC-1 | `tracking_*`, `diet_*` |
| D. LLM/AI | _(이름)_ | T-LLM-1~6, (T-QUAL-2 관련) | `chat_*` + `ai_worker/` |

## 2. 백엔드 공통모듈 소유자 (`app/services/*`, 접두어 없음)

같은 공통 파일을 두 사람이 동시에 고치면 그 지점에서 충돌이 몰린다. 담당자 외에는 임의 수정하지 않는다 (`CODING_RULES.md` 2번).

| 공통모듈 | 파일 | 담당자 |
| --- | --- | --- |
| 응급필터 + 면책정책 | `app/services/safety_service.py` | _(이름)_ |
| 질병/복약/목표 조회 단일창구 | `app/services/user_health_context_service.py` | _(이름)_ |
| 문서/알약 인식 (Tier 2 stub) | `app/services/recognition_service.py` | _(이름)_ |
| Push 발송 | `app/services/notification_service.py` | _(이름)_ |
| RAG Retriever / Context Binder | `ai_worker/` | _(이름, decision_log.md 참고)_ |
| 건강 뉴스 수집 워커 | (T-LLM-6, 미정) | _(이름)_ |

## 3. 프론트 공통모듈 소유자 (`FRONTEND_ARCHITECTURE.md` §6과 동일)

| 공통 모듈 | 파일 | 담당자 |
| --- | --- | --- |
| API 클라이언트 베이스 | `frontend/src/api/client.ts` | _(이름)_ |
| 인증 상태 공유 훅 | `frontend/src/hooks/useAuth.ts` | _(이름, Auth 스쿼드)_ |
| 면책조항 공통 컴포넌트 | `frontend/src/components/common/DisclaimerBanner.tsx` | _(이름, T-LLM-1 담당)_ |
| 챗봇 스트리밍 훅 | `frontend/src/hooks/useChatStream.ts` | _(이름, RAG/Chat 담당)_ |

## 4. 3개 스쿼드로 줄일 경우

D(LLM)를 B 또는 C에 흡수하거나, A(인증/보안)를 C에 붙이는 방식을 추천 (`CONTRIBUTING.md` §2 참고).
