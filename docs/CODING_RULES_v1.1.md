# ReMedi 개발 시작 전 규칙 (Backend)

> **문서 버전**: v1.4 · **최종 수정**: 2026-07-06
> **변경 이력**
> - v1.0 (2026-07-06): 데이터 모델 설계 원칙(`profile_id`, 2-1) 섹션 추가
> - v1.1 (2026-07-06): 백엔드 폴더 구조를 도메인 우선으로 전면 개편, 환경변수 관리(2-2)·설정 관리(2-3) 섹션 신설, CI 규칙 추가, stale한 `demo/` 경로를 실제 위치로 수정
> - v1.2 (2026-07-06): 백엔드 폴더 구조를 도메인 우선 → **레이어 우선**(`app/`)으로 재변경 (`decision_log.md` 참고). 6번 stub 경로 수정
> - v1.3 (2026-07-06): 4번 TDD 규칙에 best-practice 체크리스트 추가 (`CLAUDE.md` 작업 완료 전 체크리스트와 짝)
> - v1.4 (2026-07-06): T-LLM-2 실제 구현 시 정한 테스트 위치(`app/tests/`)를 2번 폴더 구조에 반영

## 1. 계층 구조 — 이것만 지켜도 꼬임의 80%가 사라집니다

```
Router  → Service → Repository → (DB/Redis/Chroma/외부API)
(HTTP)    (판단)     (데이터접근)
```

**절대 규칙: 화살표 반대 방향으로도, 화살표를 건너뛰어서도 호출하지 않는다.**

| 레이어 | 여기서 해도 되는 것 | 여기서 절대 하면 안 되는 것 |
| --- | --- | --- |
| Router | 요청 파싱, Service 호출, 응답 반환 | if로 비즈니스 판단, DB/쿼리 직접 접근 |
| Service | 조건 분기, 여러 Repository 조합, 외부 API 호출 | SQL 직접 작성, `Request`/`status_code` 등 HTTP 관련 코드 |
| Repository | DB/Redis/Chroma 쿼리 | 비즈니스 판단(if 조건 분기) |

이렇게 나누는 이유: Router가 Service만 알고 Service 내부 구현을 모르면, **나중에 MySQL을 다른 걸로 바꿔도 Router/Service 코드는 한 줄도 안 바뀝니다.** (`docs/sample_code_chat/nickname_repository.py`의 주석 참고)

실제로 동작하는 예제가 `docs/sample_code_chat/`(닉네임 중복확인 기본형 + AI 챗봇 실시간 스트리밍형)와 `docs/sample_code_recog/`(Recognition 확정 — Tier 2 stub 패턴 조합형)에 있습니다. 각 폴더 README대로 `PYTHONPATH=. pytest -v`로 직접 돌려보고 시작하세요 (총 14개 테스트 통과 확인됨: `sample_code_chat/` 10개, `sample_code_recog/` 4개).

이 규칙은 아래 2번의 레이어 우선 폴더 구조에도 그대로 적용됩니다 — `apis/`의 라우터 파일이 `services/`의 서비스 파일만 알고, `services/`의 서비스 파일이 `repositories/`의 저장소 파일만 알아야 합니다.

## 2. 폴더 구조 (Backend)

> 2026-07 팀 재논의 결과 **레이어 우선(종류별) 구조**로 확정했습니다 (학원 템플릿 기준, `decision_log.md` 참고 — 멘토님은 도메인 우선을 조언했으나, 도메인이 많아지면 폴더가 잘게 쪼개져 코드 스타일이 제각각으로 갈릴 위험과, 레이어 우선이 같은 폴더 안 옆 파일을 보고 패턴을 따라 하기 쉽다는 점을 이유로 팀이 의도적으로 다른 방향을 택함). 종류(레이어)당 폴더 하나이며, 도메인별 파일들이 같은 레이어 폴더 안에 나란히 놓입니다.

```
app/
├── main.py                  # FastAPI 생성 + 라우터 등록 + SQLAdmin mount
├── core/                     # DB 연결, 환경설정, 공통 Depends — 레이어에도 도메인에도 안 속하는 것만
│   ├── config.py                 # pydantic-settings 기반 설정 (2-3 참고)
│   ├── database.py               # SQLAlchemy Async Engine, Redis client, Chroma client
│   └── dependencies.py           # get_current_user, get_db 등
│
├── utils/                    # 여러 도메인이 같이 쓰는 순수 유틸 (비밀번호 해싱, 로깅 등)
│
├── apis/v1/                  # API 엔드포인트 — 도메인별 파일이 한 폴더 안에 나란히
│   ├── auth_routers.py
│   ├── medication_routers.py
│   └── chat_routers.py               # ... 실제 도메인 목록은 팀 합의로 확정 (PRD의 F-그룹 단위가 출발점)
│
├── services/                  # 비즈니스 로직. 도메인별 서비스 + 여러 도메인이 함께 쓰는 공통 서비스가 같은 폴더에 공존
│   ├── auth_service.py
│   ├── medication_service.py
│   ├── chat_service.py
│   ├── safety_service.py             # 공통① 응급필터 + 면책정책
│   ├── user_health_context_service.py   # 공통② 질병/복약/목표 조회 단일창구
│   ├── recognition_service.py        # 공통③ T-MED-1+T-DOC-1 통합 (RAG 완성 전엔 stub, 6번 참고)
│   └── notification_service.py       # 공통④ Push 발송
│
├── repositories/               # DB 접근
│   ├── auth_repository.py
│   ├── medication_repository.py
│   └── chat_repository.py
│
├── models/                     # SQLAlchemy ORM
│   ├── auth.py / medication.py / chat.py
│
├── dtos/                       # Pydantic request/response (템플릿 명명 규칙 — schema가 아니라 dto)
│   ├── base.py / auth.py / medication.py / chat.py
│
├── workers/                    # Redis Streams 소비자 (알림 발송 등 — AI/RAG 관련 아닌 백그라운드 작업)
├── tests/                      # pytest. 실제 코드와 같은 레이어 우선 폴더 구조를 따르지 않고 한 폴더에 모음
│   └── test_chat_service.py / test_chat_router.py  # (T-LLM-2 구현 시 확립된 패턴)
└── admin.py                    # SQLAdmin 등록
```

> AI/RAG/멀티모달(임베딩, 이미지 인식 등) 추론은 이 백엔드 프로세스 안에 두지 않고 **별도 서비스로 분리**합니다. 상세 통신 방식(동기/비동기)은 RAG 설계 확정 시 `decision_log.md`에 반영됩니다.

**`services/`의 4개 공통모듈(safety/user_health_context/recognition/notification)은 소유자를 명확히 하세요** (누가 고칠 수 있는지). 서로 다른 팀원이 같은 공통 파일을 동시에 수정하면 그 지점에서 충돌이 몰립니다. 4개 공통모듈 각각 담당자 한 명씩 지정 추천.

### 2-1. 데이터 모델 설계 원칙

- 사용자 관련 테이블은 `user_id`가 아니라 **`profile_id`** 기준으로 설계합니다. 본인도 하나의 프로필로 취급합니다.
- 이렇게 하면 한 계정이 여러 프로필을 갖게 되는 경우가 생겨도 테이블 구조를 바꾸지 않고 확장할 수 있습니다.
- 배경(왜 이 결정을 했는지)은 `decision_log.md` 참고.

### 2-2. 환경 변수 관리

- `envs/` 폴더에 환경별 설정 파일을 둡니다: 예시 파일(`envs/example.local.env`, `envs/example.prod.env` — 커밋 대상)과 실제 값이 든 파일(`envs/.local.env`, `envs/.prod.env` — `.gitignore` 대상).
- 앱과 Docker Compose가 실제로 읽는 파일은 프로젝트 루트의 `.env` 하나뿐입니다. 로컬/배포 환경 전환은 `.env` 내용을 직접 고치는 대신, **심볼릭 링크로 바꿔치기**합니다: `ln -s envs/.local.env .env`. 이렇게 하면 여러 환경 설정을 동시에 보관하면서도 코드는 항상 `.env` 하나만 알면 됩니다.

### 2-3. 설정 관리

- `os.getenv()`를 여러 파일에서 각자 호출하지 않고, `pydantic-settings`의 `BaseSettings`로 설정 클래스 하나를 만들어 `core/config.py`에 둡니다.
- 필수 환경변수가 없으면 앱 시작 시점에 바로 에러가 나서, 실행 중간에 알아채는 것보다 훨씬 빨리 문제를 잡을 수 있습니다.

## 3. 폴더 구조 (Frontend)

> 상태관리·컴포넌트 소유권·API 연동 패턴 등 상세 협업 규칙은 `FRONTEND_ARCHITECTURE.md`(이 문서의 프론트엔드 짝 문서) 참고.

```
frontend/src/
├── App.tsx                  # React Router 설정 (5탭: 홈/추적/상담/Info/더보기 — 2026-07 IA 개편 반영)
├── pages/                    # 탭 1개 = 파일 1개
│   ├── HomePage.tsx / TrackingPage.tsx / ChatPage.tsx / InfoPage.tsx / MorePage.tsx
├── components/
│   ├── common/                # 여러 탭에서 재사용 (예: DisclaimerBanner — T-LLM-1)
│   └── (탭별 하위 폴더)
├── api/                       # 백엔드 호출 함수. API 명세(OpenAPI) 엔드포인트와 파일을 1:1로 맞춤
│   ├── authApi.ts / chatApi.ts / medicationApi.ts ...
├── hooks/                      # useChatStream 등 커스텀 훅
└── serviceWorker.ts
```

**규칙: 컴포넌트(`pages/`, `components/`)는 `fetch`를 직접 호출하지 않는다. 반드시 `api/` 폴더 함수를 통해서만 호출한다.** 나중에 인증 방식이 바뀌거나 에러 처리 포맷이 바뀌어도 `api/` 폴더만 고치면 됩니다.

## 4. TDD 규칙
- **테스트 없는 기능 코드는 미완성이다.** Service 함수 하나(또는 엔드포인트/버그수정) 만들면, 최소 2개 테스트(정상/실패)를 **같은 PR 안에** 포함한다. (Claude가 작업할 때도 동일 — `CLAUDE.md` "작업 완료 전 체크리스트" 참고)
- Service 단위테스트는 진짜 DB 없이 가짜(Fake) Repository로 테스트한다 (`docs/sample_code_chat/test_nickname_service.py` 패턴 참고).
- Router는 `TestClient`로 통합테스트만 가볍게 — 상태코드와 응답 형태만 확인, 로직 재검증은 안 함.
- 테스트 작성 시 지킬 최소 원칙 (짧게):
  - 외부 의존성(DB/Redis/Chroma/LLM/네트워크)은 항상 Fake/Stub으로 대체한다 — 실제 호출 없이 몇 번을 돌려도 같은 결과가 나와야 한다.
  - 테스트 하나는 동작 하나만 검증한다 (여러 케이스를 한 테스트에 섞지 않는다).
  - 테스트 이름은 "무엇을 검증하는지" 설명하는 문장형으로 짓는다 (예: `test_새로운_닉네임은_사용가능하다`).
  - 정상 케이스만 있는 테스트는 미완성이다 — 경계값/실패 케이스를 반드시 포함한다.

## 5. 그 외 최소 규칙
- 커밋 메시지: `[T-ID] 설명` 형식 (예: `[T-LLM-2] 응급 키워드 필터 추가`) — Notion 스토리와 매칭용
- API 에러 응답은 항상 `{error_code, message}` 형태로 통일 (OpenAPI 명세의 `ErrorResponse` 스키마 참고)
- `.env`는 절대 커밋하지 않는다 — `envs/example.*.env`만 커밋 (2-2 참고)
- PR을 올리기 전 로컬에서 `ruff check`/`ruff format --check`, `pytest`를 미리 돌려본다 — GitHub Actions CI에서 동일하게 검사한다 (`decision_log.md`의 CI/CD 항목 참고)

## 6. RAG 완성 전 개발 규칙 (Tier 2 stub 패턴)
T-MED-2, T-DOC-2처럼 RAG Retriever가 필요한 기능인데 아직 RAG가 준비 안 됐다면:
- Router/Schema(API 명세)는 **최종 형태 그대로** 먼저 만든다 (`GuideCard` 스키마 참고)
- Service 내부(`services/recognition_service.py`)는 일단 규칙기반 하드코딩 값을 리턴하는 stub으로 채운다
- RAG가 완성되면 **Service 내부 구현만** 교체한다. AI/RAG는 별도 서비스로 분리되므로(2번 참고), 실제로는 Retriever를 직접 호출하는 대신 그 서비스에 요청을 보내는 코드로 바뀔 가능성이 높다 — 어느 쪽이든 Router/프론트/API 명세는 손대지 않는다
- 이게 가능한 이유는 1번 규칙(계층 분리)을 지켰기 때문. Router가 Service의 내부 구현을 몰라야 이 교체가 공짜로 된다.
- 참고 예제: `docs/sample_code_recog/`(Tier 2 stub 패턴 실제 코드)
