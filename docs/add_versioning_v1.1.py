import io

BASE = "/sessions/busy-laughing-noether/mnt/remedi_mweb_co/docs/"

def load(name):
    with io.open(BASE + name, encoding="utf-8") as f:
        return f.read()

def save(name, text):
    with io.open(BASE + name, "w", encoding="utf-8") as f:
        f.write(text)

def do_replace(text, old, new, label):
    n = text.count(old)
    assert n == 1, f"{label}: match count {n}"
    return text.replace(old, new)

# ---------------- PRD_ReMedi.md ----------------
name = "PRD_ReMedi.md"
text = load(name)
text = do_replace(
    text,
    "| 관련 TRD | `TRD_ReMedi.md` |\n| 원본 요구사항정의서 | `ReMedi_prd.md` (중복해소·재분류 완료본 158개 항목) |\n\n> 이 문서는 요구사항정의서의 158개 항목을 사용자 관점의 기능 단위(F-그룹)로 재구성한 것입니다.\n> 각 F-그룹은 대응하는 TRD 항목(T-그룹) 및 원본 REQ ID를 함께 표기해 상호 참조가 가능합니다.\n> ⚠ 표시된 그룹은 **Backlog**(이번 릴리스 범위 제외)입니다.",
    "| 관련 TRD | `TRD_ReMedi.md` |\n| 원본 요구사항정의서 | `ReMedi_prd.md` (중복해소·재분류 완료본 158개 항목) |\n| 문서 버전 | v1.0 (2026-07-06) |\n\n> 이 문서는 요구사항정의서의 158개 항목을 사용자 관점의 기능 단위(F-그룹)로 재구성한 것입니다.\n> 각 F-그룹은 대응하는 TRD 항목(T-그룹) 및 원본 REQ ID를 함께 표기해 상호 참조가 가능합니다.\n> ⚠ 표시된 그룹은 **Backlog**(이번 릴리스 범위 제외)입니다.\n>\n> **변경 이력**\n> - v1.0 (2026-07-06): F-AUTH-5/6 분리(가족연결/가족구성원관리), F-CARD-1(응급공유카드) 신설, \"추적\" 탭 설명 추가, IA 개편 메모 정리",
    "PRD header",
)
save(name, text)

# ---------------- TRD_ReMedi.md ----------------
name = "TRD_ReMedi.md"
text = load(name)
text = do_replace(
    text,
    "| 관련 PRD | `PRD_ReMedi.md` |\n\n> 데이터 모델, API 명세, 상세 아키텍처는 별도 문서에서 관리합니다.\n> 이 문서는 각 기능 단위(T-그룹)별 **입력 항목 / 출력·노출 항목 / 성공요건(Pass Criteria)**만 정의합니다.\n> 흐름·구현 방식(어떤 라이브러리로, 어떤 순서로 처리할지)은 개발자 재량에 맡깁니다.\n> 각 T-그룹은 PRD의 F-그룹과 번호가 1:1 대응됩니다.",
    "| 관련 PRD | `PRD_ReMedi.md` |\n| 문서 버전 | v1.0 (2026-07-06) |\n\n> 데이터 모델, API 명세, 상세 아키텍처는 별도 문서에서 관리합니다.\n> 이 문서는 각 기능 단위(T-그룹)별 **입력 항목 / 출력·노출 항목 / 성공요건(Pass Criteria)**만 정의합니다.\n> 흐름·구현 방식(어떤 라이브러리로, 어떤 순서로 처리할지)은 개발자 재량에 맡깁니다.\n> 각 T-그룹은 PRD의 F-그룹과 번호가 1:1 대응됩니다.\n>\n> **변경 이력**\n> - v1.0 (2026-07-06): T-AUTH-5/6 분리(가족연결/가족구성원관리), T-CARD-1(응급공유카드) 신설",
    "TRD header",
)
save(name, text)

# ---------------- decision_log.md ----------------
name = "decision_log.md"
text = load(name)
text = do_replace(
    text,
    "# ReMedi 아키텍처 결정 로그 (2026-07 확정본)\n\n## 확정된 기술 결정",
    "# ReMedi 아키텍처 결정 로그 (2026-07 확정본)\n\n"
    "> **문서 버전**: v1.1 · **최종 수정**: 2026-07-06\n"
    "> **변경 이력**\n"
    "> - v1.0 (2026-07-06): 5탭 IA 반영, T-AUTH-5/6 Phase 배치 정리, RAG 아키텍처(Chroma Server Mode·청킹·Collection·대화이력) 섹션 신설, 미결사항 신설\n"
    "> - v1.1 (2026-07-06): JWT 인증 전환, MySQL 비동기 요건, 백엔드 도메인 우선 구조 전환, AI/RAG 워커 분리 원칙, CI/CD·환경변수 관리 항목 추가, 팀 합의 없는 개인 작업 코드 관련 경고 추가\n\n"
    "## 확정된 기술 결정",
    "decision_log header",
)
save(name, text)

# ---------------- CLAUDE.md ----------------
name = "CLAUDE.md"
text = load(name)
text = do_replace(
    text,
    "불확실하면 추측해서 진행하지 말고 사용자에게 물어보세요.\n\n## 프로젝트",
    "불확실하면 추측해서 진행하지 말고 사용자에게 물어보세요.\n\n"
    "> **문서 버전**: v1.1 · **최종 수정**: 2026-07-06\n"
    "> **변경 이력**\n"
    "> - v1.0 (2026-07-06): 데이터 설계 원칙(`profile_id`) 섹션 추가\n"
    "> - v1.1 (2026-07-06): 폴더 구조 표기를 실제 이름(`backend/`, `frontend/`, `domains/*`)으로 수정, 팀 합의 없는 개인 작업 코드 관련 경계 규칙 추가\n\n"
    "## 프로젝트",
    "CLAUDE.md header",
)
# add versioning convention rule near the end
text = do_replace(
    text,
    "## 모호할 때\n\n- T-ID가 명시되지 않은 요청, 여러 도메인에 걸친 요청, 또는 TRD에 없는 동작이 필요한\n  요청을 받으면 임의로 판단해 진행하지 말고 무엇을 가정했는지 먼저 설명하고 확인받는다.\n- 이미 실패한 접근(예: 특정 라이브러리, 특정 스키마 설계)을 사용자가 이전에 명시적으로\n  피하라고 했다면, 같은 대화 내에서 이를 번복해 다시 시도하지 않는다.",
    "## 모호할 때\n\n- T-ID가 명시되지 않은 요청, 여러 도메인에 걸친 요청, 또는 TRD에 없는 동작이 필요한\n  요청을 받으면 임의로 판단해 진행하지 말고 무엇을 가정했는지 먼저 설명하고 확인받는다.\n- 이미 실패한 접근(예: 특정 라이브러리, 특정 스키마 설계)을 사용자가 이전에 명시적으로\n  피하라고 했다면, 같은 대화 내에서 이를 번복해 다시 시도하지 않는다.\n\n"
    "## 문서 버전 관리\n\n"
    "- `PRD_ReMedi.md`, `TRD_ReMedi.md`, `decision_log.md`, `CLAUDE.md`, `CODING_RULES.md`, `api_spec_core_v1.yaml` 중 하나라도\n"
    "  내용을 바꾸면, 그 문서 상단의 **버전 번호를 올리고 변경 이력에 한 줄 추가**한다 (예: v1.1 → v1.2, 오늘 날짜와 함께).\n"
    "  오타 수정처럼 사소한 변경은 예외로 하되, 애매하면 사용자에게 버전을 올릴지 확인한다.",
    "CLAUDE.md versioning rule",
)
save(name, text)

# ---------------- CODING_RULES.md ----------------
name = "CODING_RULES.md"
text = load(name)
text = do_replace(
    text,
    "# ReMedi 개발 시작 전 규칙 (Backend)\n\n## 1. 계층 구조",
    "# ReMedi 개발 시작 전 규칙 (Backend)\n\n"
    "> **문서 버전**: v1.1 · **최종 수정**: 2026-07-06\n"
    "> **변경 이력**\n"
    "> - v1.0 (2026-07-06): 데이터 모델 설계 원칙(`profile_id`, 2-1) 섹션 추가\n"
    "> - v1.1 (2026-07-06): 백엔드 폴더 구조를 도메인 우선으로 전면 개편, 환경변수 관리(2-2)·설정 관리(2-3) 섹션 신설, CI 규칙 추가, stale한 `demo/` 경로를 실제 위치로 수정\n\n"
    "## 1. 계층 구조",
    "CODING_RULES header",
)
save(name, text)

print("markdown version headers added.")
