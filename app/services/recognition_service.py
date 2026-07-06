"""
공통③ T-MED-1 + T-DOC-1 통합 (문서/알약 인식).
RAG 완성 전에는 규칙기반 stub을 리턴한다 (CODING_RULES.md 6번, Tier 2 stub 패턴).
RAG 완성 후에는 이 함수 내부만 AI 워커(scaffold/ai_worker) 호출로 교체 — Router/DTO는 그대로 유지.
"""


async def get_recognition_guide(recognition_result: dict) -> dict:
    return {
        "title": "안내 (임시 stub)",
        "content": "RAG 완성 전까지 노출되는 임시 안내입니다.",
        "severity": "info",
    }
