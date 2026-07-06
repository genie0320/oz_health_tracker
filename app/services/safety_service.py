"""
공통① 응급필터 + 면책정책 (T-LLM-1, T-LLM-2 관련).
소유자: 팀 협의 후 지정. 다른 *_service.py 파일과 같은 폴더에 있으니 스타일을 맞춰서 작성할 것.
"""

DISCLAIMER_TEXT = "이 정보는 의학적 조언이 아니며, 정확한 진단은 의료진과 상담하세요."

EMERGENCY_KEYWORDS = ["가슴 통증", "숨이 안 쉬어져", "의식이 없어요"]


def contains_emergency_keyword(text: str) -> bool:
    return any(keyword in text for keyword in EMERGENCY_KEYWORDS)


def with_disclaimer(payload: dict) -> dict:
    payload["disclaimer"] = DISCLAIMER_TEXT
    return payload
