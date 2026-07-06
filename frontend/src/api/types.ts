// api_spec_core_v1.yaml과 1:1로 수동 동기화 (FRONTEND_ARCHITECTURE.md 4번 — React Query/자동생성 대신 수동 패턴).
export interface AuthTokenResult {
  user_id: string;
  message: string;
  access_token: string;
  refresh_token: string;
  token_type: string;
}
