# chainlit_prototype/ — 임시 프로토타입 (제품 아님)

`app/services/chat_service.py`의 LLM/RAG 로직이 실제로 동작하는지 프론트엔드 없이
빠르게 눈으로 확인하기 위한 도구입니다. 정식 화면(`frontend/src/pages/ChatPage/`)이나
레이어 우선 백엔드 구조(`app/`)와는 무관하며, 이 폴더를 지워도 제품에 영향 없습니다.

세션/로그인/대화 기록 저장은 생략하고 `app/services/safety_service.py`,
`app/services/retriever.py`, `app/services/llm_client.py`만 그대로 재사용합니다.

## 실행 방법

```bash
# 레포 루트에서 .env가 심볼릭 링크로 준비돼 있어야 한다 (OPENAI_API_KEY 필요, README.md 참고)
pip install chainlit openai pydantic pydantic-settings
cd chainlit_prototype
chainlit run chat_app.py -w
```

브라우저가 자동으로 열리고, 채팅창에 메시지를 입력하면 OpenAI 모델(`OPENAI_MODEL`, 기본
`gpt-4o-mini`)이 실시간으로 스트리밍 응답합니다. 응급 키워드("가슴 통증" 등)를 입력하면
LLM 호출 없이 고정 안내가 즉시 뜨는 것도 확인할 수 있습니다.
