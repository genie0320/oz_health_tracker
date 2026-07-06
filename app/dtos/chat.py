from pydantic import BaseModel


class ChatMessageRequest(BaseModel):
    message: str
    input_type: str = "text"


class ChatSessionCreateResult(BaseModel):
    session_id: str
