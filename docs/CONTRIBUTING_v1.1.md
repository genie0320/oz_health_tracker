# ReMedi 협업 하네스 (최소 버전)

> 목적: 여러 장소에서, 스쿼드별로 나눠서, 개발 초보자들이 참여하는 프로젝트에서
> "서로 꼬이지 않는 것"에만 집중한 최소 규칙입니다. 완벽한 프로세스가 아니라
> **사고를 줄이는 최소 장치**라고 생각하고 팀 상황에 맞게 가감하세요.
>
> **문서 버전**: v1.2 · **최종 수정**: 2026-07-06
> **변경 이력**
> - v1.0: 최초 작성
> - v1.1 (2026-07-06): 레포 구조를 실제 이름(`backend/`, `frontend/`, 도메인 우선)으로 수정, 스쿼드 매핑의 폴더 예시 갱신, 환경변수 표기를 `envs/` 컨벤션에 맞춤
> - v1.2 (2026-07-06): 백엔드 구조를 도메인 우선 → **레이어 우선**(`app/`)으로 재변경. 스쿼드 매핑을 폴더 단위 → 파일명 접두어 단위로 수정 (`decision_log.md` 참고)

---

## 0. 한 장 요약

| 항목 | 규칙 |
| --- | --- |
| 레포 | 모노레포 1개 (`frontend/`, `app/` — `app`은 레이어 우선 구조) |
| 브랜치 | `main`(배포) ← `develop`(통합) ← `feature/T-ID-설명`(작업), 필요 시 `release/*`, `hotfix/*` |
| 커밋 | `type(T-ID): 설명` 예) `feat(T-AUTH-1): 이메일 회원가입 폼` |
| PR | 작은 단위, 제목에 T-ID/F-ID, 리뷰 1명 필수, `develop`으로 머지 |
| 이슈 | 제목에 T-ID 포함, 담당 스쿼드 라벨 지정 |
| 충돌 방지 | 작업 시작 전 슬랙에 "지금 어떤 파일/기능 건드림" 1줄 공지 |
| 하루 루틴 | 시작 시 `git pull`, 끝날 때 push + PR, 자기 전 develop 최신화 |

---

## 1. 레포 구조 (모노레포)

```
remedi/
├─ app/                  # 백엔드 (레이어 우선 구조 — 상세는 CODING_RULES.md 2번)
│  ├─ apis/ services/ repositories/ models/ dtos/   # 레이어별 폴더, 도메인 파일은 파일명 접두어로 구분
├─ frontend/             # 프론트엔드
├─ packages/
│  └─ shared/            # 타입, 상수, 공통 유틸 (양쪽에서 import) — 아직 없음, 필요해지면 생성
├─ envs/                 # 환경별 설정 파일 (CODING_RULES.md 2-2 참고)
├─ docs/
│  ├─ PRD_ReMedi.md
│  ├─ TRD_ReMedi.md
│  └─ squad-map.md        # 아래 2번 내용
└─ CONTRIBUTING.md        # 이 문서
```

**모노레포를 쓰는 이유**: 초보 개발자 팀에서 레포가 나뉘면 "API 스펙이 바뀌었는데 프론트가 몰랐다"는 문제가 반드시 생깁니다. 하나의 레포 + 하나의 PR 흐름이면 리뷰할 때 프론트/백엔드 변경을 같이 볼 수 있어 훨씬 안전합니다. 나중에 팀이 커지면 그때 분리해도 늦지 않습니다.

`packages/shared`가 생기면 API 요청/응답 타입, 에러 코드, 상수만 둡니다. 여기는 **모든 스쿼드가 함께 쓰는 영역**이라 변경 시 PR에 `[shared]` 태그를 달고 다른 스쿼드에게 리뷰를 요청하세요.

---

## 2. 스쿼드 ↔ 기능 도메인 매핑 (4개 스쿼드 기준)

TRD의 T-그룹 경계를 그대로 스쿼드 경계로 씁니다. 이렇게 하면 "이 파일은 누구 담당인지"를 이슈 번호만 보고 알 수 있습니다.

| 스쿼드 | 담당 T-그룹 (TRD 기준) | 주요 백엔드 파일 접두어 (레이어 우선이라 폴더 대신 파일명으로 구분, 예시) |
| --- | --- | --- |
| **A. 인증/보안** | T-AUTH-1~6, T-SEC-1, T-STAT-1, T-PRIV-1, T-ENC-1, T-ARCH-1 | `auth_*` (각 레이어 폴더 안에서 `apis/v1/auth_routers.py`, `services/auth_service.py` 등) |
| **B. 복약인식/알림** | T-MED-1~2, T-DOC-1~3, T-NTFY-1~6, T-CARD-1 | `medication_*`, `notification_*` |
| **C. 목표/추적/건강정보** | T-GOAL-1~3, T-ADH-1~3, T-GUIDE-1, T-INFO-1~3, T-TRCK-1~3, T-DIET-1~2, T-ACC-1 | `tracking_*`, `diet_*` |
| **D. LLM/AI** | T-LLM-1~6, (T-QUAL-2 관련) | `chat_*` + 별도 AI/RAG 워커 서비스(`decision_log.md` 참고) |

- **레이어 우선 구조라 폴더가 아니라 파일명으로 소유권을 나눕니다**: 도메인 하나의 코드가 `apis/`, `services/`, `repositories/`, `models/`, `dtos/`에 흩어져 있으므로, "이 폴더는 내 것"이 아니라 "이 접두어가 붙은 파일은 내 것"으로 구분하세요 (`CODING_RULES.md` 2번 참고). `services/`의 4개 공통모듈(접두어 없는 `safety_service.py` 등)은 스쿼드 소유가 아니라 담당자 지정제입니다.
- **프론트 폴더는 표에서 뺐습니다**: 탭 구조가 아직 가안(`decision_log.md` 참고)이라 도메인-탭 매핑을 지금 확정하면 나중에 다시 손대야 합니다. 프론트 담당 범위는 스쿼드끼리 협의해서 정하세요.
- **3개 스쿼드로 줄일 경우**: D(LLM)를 B 또는 C에 흡수하거나, A(인증/보안)를 작게 보고 C에 붙이는 방식을 추천합니다. 백로그(채팅/커뮤니티, 자체 AI 모델)는 이번 범위에서 아예 제외했습니다.
- 접두어는 예시이니 첫 스프린트 킥오프 때 실제 도메인 이름에 맞게 `docs/squad-map.md`에 확정해서 적어두세요. **이 매핑표 자체가 "누구에게 물어볼지"를 알려주는 지도**가 됩니다.

---

## 3. 브랜치 전략 (GitFlow)

```
main (master)  ← 배포 가능한 최종 상태만 (직접 push 금지, release/hotfix 머지만 허용)
 └─ develop     ← 개발 중인 기능이 모이는 통합 브랜치 (직접 push 금지, PR로만 병합)
     ├─ feature/{T-ID}-{짧은설명}   ← develop에서 분기, develop으로 병합
     ├─ release/{버전}              ← develop에서 분기, main + develop 양쪽에 병합
     └─ hotfix/{짧은설명}           ← main에서 분기, main + develop 양쪽에 병합
```

| 브랜치 | 분기 시작점 | 병합 대상 | 언제 만드나 |
| --- | --- | --- | --- |
| `feature/*` | `develop` | `develop` | T-ID 단위 기능 개발할 때 (평소 대부분의 작업) |
| `release/*` | `develop` | `main` + `develop` | 배포 준비(QA, 버전 고정)할 때 |
| `hotfix/*` | `main` | `main` + `develop` | 운영 중 긴급 버그를 바로 고쳐야 할 때 |

- 브랜치 예: `feature/T-MED-1-pill-recognition`, `hotfix/login-token-expire-crash`
- 초보 팀은 대부분 `feature/*`만 씁니다. `release/*`, `hotfix/*`는 실제 배포 단계에 들어가기 전까지는 안 써도 됩니다 — 미리 규칙만 정해두는 것.
- **main, develop은 보호 브랜치로 설정**하고(깃허브 Settings → Branches → Branch protection rule), 반드시 PR + 최소 1명 승인 후에만 병합되게 하세요.
- `feature/*`는 항상 **`develop`을 최신으로 pull한 뒤** 분기하세요. 오래된 develop에서 분기하면 나중에 충돌이 커집니다.

---

## 4. 커밋 & PR 규칙

### 커밋 메시지
```
type(T-ID): 설명

예)
feat(T-AUTH-1): 이메일 회원가입 API 구현
fix(T-NTFY-1): 알림 미도착 버그 수정
docs(T-LLM-1): 면책조항 정책 문서 추가
```
`type`은 `feat`(기능) / `fix`(버그) / `docs`(문서) / `refactor`(리팩터링) / `chore`(설정) 정도만 써도 충분합니다.

### PR 규칙
- 제목: `[T-ID] 작업 내용 요약` (예: `[T-MED-1] 알약 사진 업로드 + 후보 리스트 UI`)
- 설명에 최소 포함:
  - 무엇을 했는지 (TRD 성공요건 중 어떤 것을 충족했는지 체크)
  - 어떻게 테스트했는지 (스크린샷/GIF면 더 좋음, 초보자에게는 말보다 그림)
- **200~300줄 이내로 작게** 쪼개서 올리기 — 초보자 리뷰는 PR이 작을수록 실질적으로 이뤄집니다.
- 리뷰어 1명 승인 후 본인이 머지 (스쿼드 내 서로 리뷰, `shared` 변경 시 다른 스쿼드원 1명 추가 리뷰)
- 머지 방식은 **Squash and merge**로 통일 (커밋 이력이 지저분해지는 걸 방지, 초보자가 rebase 안 해도 됨)

---

## 5. 이슈 관리 (칸반이든 뭐든 최소 규칙)

- 이슈 제목에 반드시 T-ID/F-ID 포함: `[T-AUTH-1] 이메일 회원가입`
- 라벨: 스쿼드명(`squad-a`~`squad-d`), 상태(`todo`/`in-progress`/`review`/`done`)
- 담당자 지정 없이 작업 시작 금지 — "일단 내가 할게요"를 이슈에 코멘트로 남기고 시작 (동시에 같은 T-ID 작업하는 사고 방지)
- PRD/TRD의 T-ID를 그대로 쓰는 이유: 나중에 "이 요구사항 누가 했지?" 찾을 때 문서-이슈-PR-커밋이 하나의 번호로 다 연결됩니다.

---

## 6. 충돌(코드/작업) 방지 원칙

개발 초보자 팀에서 실제로 자주 터지는 문제와 대응:

| 문제 상황 | 예방 규칙 |
| --- | --- |
| 같은 파일을 두 사람이 동시에 수정 | 작업 시작 전 슬랙/디스코드에 "지금 `medication/schedule.ts` 건드립니다" 한 줄 공지 |
| `shared` 타입을 바꿨는데 다른 스쿼드가 모름 | `shared` 변경 PR은 팀 전체 채널에 별도 공지 + 다른 스쿼드 리뷰 필수 |
| 오래된 브랜치에서 작업해서 충돌 폭탄 | 매일 작업 시작 전 `git checkout develop && git pull` 후 새로 브랜치 따기 습관화 |
| develop에 머지했는데 깨짐 | 머지 전 로컬에서 최소 1회 실행/빌드 확인 (아래 7번 최소 CI가 자동으로 잡아줌) |
| 누가 뭘 하는지 몰라서 중복 작업 | 이슈 담당자 지정 + 주 2회(예: 월/목) 짧은 스쿼드 간 동기화 |

---

## 7. 최소 CI (선택이지만 강력 추천)

GitHub Actions로 PR마다 아래만 돌려도 초보 팀 사고의 절반은 막습니다.

```yaml
# .github/workflows/ci.yml
name: CI
on:
  pull_request:
    branches: [develop, main]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm install
      - run: npm run lint
      - run: npm run build
```
→ "빌드 깨진 코드가 develop에 머지되는 것"만 막아도 팀 전체 생산성이 크게 오릅니다.

백엔드 쪽 CI(`ruff check`/`ruff format --check` + `pytest`, MySQL 서비스 컨테이너 포함)는 이미 도입하기로 확정되어 있습니다 — 상세는 `decision_log.md`의 CI/CD 항목 참고. 위 프론트 job과 같은 workflow 파일에 백엔드 job을 나란히 추가하면 됩니다.

---

## 8. 환경변수 / 시크릿

- 실제 값이 든 `.env`, `envs/.local.env`, `envs/.prod.env`는 절대 커밋 금지. 커밋하는 건 `envs/example.local.env`, `envs/example.prod.env`처럼 키 이름만 있는 예시 파일뿐 (상세 구조는 `CODING_RULES.md` 2-2)
- API 키(구글 로그인, LLM API 등)는 슬랙 DM이나 1Password/Notion 비공개 페이지로 공유, **절대 PR/이슈/코드에 평문으로 남기지 않기**
- `.gitignore`에 `.env`, `envs/.*.env`, `node_modules`, `dist` 기본 포함 확인

---

## 9. 초보자용 Git 사용법 요약 (하루 루틴)

```bash
# 하루 시작
git checkout develop
git pull origin develop
git checkout -b feature/T-MED-1-pill-recognition

# 작업 중 (자주, 작게)
git add .
git commit -m "feat(T-MED-1): 알약 사진 업로드 UI"

# 작업 끝 / 하루 마무리
git push origin feature/T-MED-1-pill-recognition
# → GitHub에서 develop으로 PR 생성, 리뷰 요청

# 충돌 나면
git checkout develop && git pull origin develop
git checkout feature/T-MED-1-pill-recognition
git merge develop
# 충돌 파일 직접 열어서 <<<<<<< / ======= / >>>>>>> 부분 정리 후
git add .
git commit -m "merge: develop 반영"
git push
```

---

## 10. 다음에 정할 것 (킥오프 때 채우기)

- [ ] `docs/squad-map.md`에 실제 4개 스쿼드 이름 + 담당 T-ID 확정
- [ ] GitHub 브랜치 보호 규칙 설정 (main, develop)
- [ ] PR 템플릿(`.github/pull_request_template.md`) 등록
- [ ] 이슈 라벨 생성 (스쿼드별 + 상태별)
- [ ] 슬랙(or 디스코드) 채널: `#전체공지`, `#squad-a`~`#squad-d`, `#shared-변경`
