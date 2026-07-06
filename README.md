# ReMedi

> **버전**: v3 (2026-07-06) — 레이어 우선 구조가 실제 레포 최상위 구조로 확정 반영됨.
> v1은 도메인 우선(`backend/`)이었으나 팀 논의 끝에 폐기, v2는 별도 `scaffold/` 폴더에 레이어 우선 구조를 새로 만든 제안 단계였음. 지금은 그 제안이 그대로 이 레포의 실제 구조가 된 상태 — `scaffold/`, `backend/` 같은 과거 폴더는 더 이상 존재하지 않는다.

LLM 기반 복약·건강관리 PWA. 자세한 요구사항/결정 배경은 `docs/PRD_ReMedi.md`, `docs/TRD_ReMedi.md`, `docs/decision_log.md`, `docs/CODING_RULES.md`, `docs/FRONTEND_ARCHITECTURE.md`를 참고.

## 무엇이 들어있나

| 폴더/파일 | 내용 | 근거 문서 |
| --- | --- | --- |
| `app/` | **레이어 우선 구조**. `apis/v1/`(라우터), `services/`(비즈니스 로직 + 4개 공통모듈), `repositories/`(DB 접근), `models/`, `dtos/`(요청/응답), `core/`(설정·DB), `utils/`, `workers/` | `CODING_RULES.md` 2번, `decision_log.md` "백엔드 구조" |
| `frontend/` | 5탭(홈/추적/상담/Info/더보기 — 가안) 페이지 구조, `api/`, `hooks/`, `components/common/` | `FRONTEND_ARCHITECTURE.md` |
| `ai_worker/` | AI/RAG/멀티모달 전용 별도 서비스. `sync_api.py`(동기), `queue_worker.py`(비동기 큐), `models/`(학습된 모델 파일 보관) | `decision_log.md` "AI/RAG/멀티모달 워커 분리 원칙" |
| `envs/` | 환경별 예시 설정 파일 | `CODING_RULES.md` 2-2 |
| `docker-compose.yml` | MySQL, Redis, ChromaDB(Server Mode), `app/`, `ai_worker/`(sync/queue 2개 서비스) | `decision_log.md` 확정 기술 결정 표 |
| `pyproject.toml` | uv 기반, `app`/`ai`/`dev` 의존성 그룹 분리 | — |
| `.github/workflows/ci.yml` | 백엔드(ruff+pytest, MySQL 서비스 컨테이너) + 프론트(lint+format+build) 두 job | `decision_log.md` CI/CD 항목 |
| `chainlit_prototype/` | T-LLM-2 로직을 화면 없이 빠르게 눈으로 확인하는 임시 도구 — **제품 아님**, 지워도 무방 | `chainlit_prototype/README.md` |

## 왜 레이어 우선으로 갔나 (도메인 우선에서 재결정)

`decision_log.md`에 정리했지만 요약하면: 멘토님은 도메인 우선을 조언하셨지만, 팀이 논의 끝에
**레이어 우선**을 택했다. 도메인 우선은 도메인이 15개 안팎인 우리 규모에서 각 폴더가
독립적이라 팀원마다(그리고 Claude 같은 AI 에이전트가 작업할 때도) 스타일이 제각각으로
갈릴 위험이 있다고 판단했다. 레이어 우선은 `services/` 폴더 하나에 모든 도메인의 서비스
파일이 나란히 있어서, 새 코드를 짤 때 옆 파일을 보고 패턴을 그대로 따라 하기 쉽다 —
사람 개발자에게도, 코드를 대신 작성하는 AI 에이전트에게도 동일하게 적용되는 이유다.

## 아직 안 채운 것 (일부러 비워둠)

- `app/apis`, `services`, `repositories`, `models`, `dtos`에 auth/medication/chat 3개
  도메인만 예시로 만들었다. 나머지 도메인은 실제 작업 시작할 때 같은 패턴으로 추가하면 된다.
- `repository.py`/`service.py`류는 메서드 시그니처 없이 껍데기만 있는 경우가 많다.
- `ai_worker/`의 큐 종류·엔드포인트 스펙은 RAG 담당자가 설계할 몫으로 비워뒀다.
- `profile_id` vs `user_id`: 원칙은 `profile_id`로 확정했으나(`CODING_RULES.md` 2-1), 기존 코드 일부에 `user_id`가 남아있을 수 있다 — 발견 시 팀 논의 후 정리.
- Access/Refresh Token을 프론트 어디에 보관할지(메모리만 vs 다른 방식)도 아직 미확정이라,
  일단 메모리 보관으로만 스캐폴딩했다 (`FRONTEND_ARCHITECTURE.md` 0번 참고).
- `docs/squad-map.md`의 스쿼드/공통모듈 소유자는 빈 템플릿 상태 — 팀 킥오프 때 채운다.

## 빠른 시작 (Quick Start)

```bash
# 1. 환경변수 준비
cp envs/example.local.env envs/.local.env
ln -s envs/.local.env .env

# 2. 전체 스택 실행
docker compose up -d --build

# 3. 프론트 별도 실행 (개발 중)
cd frontend && npm install && npm run dev
```

⚠ 처음 띄워볼 때 의존성 버전 등에서 사소한 오류가 날 수 있다. 문제 생기면 `docker compose logs -f`로 어느 서비스가 실패했는지 먼저 확인.
