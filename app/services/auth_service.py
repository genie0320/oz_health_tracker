"""T-AUTH-1~4 (이메일 가입, 소셜 로그인, 토큰 갱신, 로그아웃)."""

from app.repositories.auth_repository import AuthRepository


class AuthService:
    def __init__(self, repository: AuthRepository):
        self.repository = repository

    # TODO: 유스케이스 메서드 구현
