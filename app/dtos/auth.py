from pydantic import BaseModel


class SignupRequest(BaseModel):
    email: str
    password: str
    name: str


class AuthTokenResult(BaseModel):
    user_id: str
    message: str
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
