import { apiFetch } from "./client";
import type { AuthTokenResult } from "./types";

export const authApi = {
  login: (email: string, password: string) =>
    apiFetch<AuthTokenResult>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),
  logout: () => apiFetch<void>("/auth/logout", { method: "POST" }),
};
