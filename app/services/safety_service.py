"""
공통① 응급필터 + 면책정책 (T-LLM-1, T-LLM-2 관련).
소유자: 팀 협의 후 지정. 다른 *_service.py 파일과 같은 폴더에 있으니 스타일을 맞춰서 작성할 것.
"""

DISCLAIMER_TEXT = "이 정보는 의학적 조언이 아니며, 정확한 진단은 의료진과 상담하세요."

# 응급 감지 시 LLM 대신 반환하는 고정 안내 (T-LLM-2). DISCLAIMER_TEXT와는 목적이 다르다 —
# 매 응답에 붙는 일반 면책과 달리, 이건 응급 상황 자체에 대한 행동 지침이다.
EMERGENCY_FALLBACK_MESSAGE = "긴급한 증상일 수 있습니다. 즉시 119(응급실) 또는 자살예방상담전화 1393으로 연락하세요."

EMERGENCY_KEYWORDS = ["가슴 통증", "숨이 안 쉬어져", "의식이 없어요"]


def contains_emergency_keyword(text: str) -> bool:
    return any(keyword in text for keyword in EMERGENCY_KEYWORDS)


def with_disclaimer(payload: dict) -> dict:
    payload["disclaimer"] = DISCLAIMER_TEXT
    return payload
