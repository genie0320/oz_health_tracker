/**
 * API 클라이언트 베이스 (fetch wrapper). 모든 api/*.ts가 이걸 통해서만 호출한다.
 * 인증: JWT — Authorization: Bearer 헤더 (decision_log.md 2026-07, httpOnly 쿠키에서 변경).
 * Access Token은 메모리에만 보관 권장 (localStorage/sessionStorage 지양 — XSS 리스크).
 */
let accessToken: string | null = null;

export function setAccessToken(token: string | null) {
  accessToken = token;
}

export async function apiFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`/api/v1${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
      ...options.headers,
    },
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.message ?? `API 오류 (${res.status})`);
  }
  return res.json() as Promise<T>;
}
