/**
 * T-LLM-2 스트리밍 훅. 소유자: 서현(RAG/Chat 연동) — FRONTEND_ARCHITECTURE.md 6번.
 */
export function useChatStream() {
  // TODO: StreamingResponse 청크를 fetch로 읽어 타이핑 효과 구현 (decision_log.md 챗봇 응답 항목 참고)
  return { messages: [], sendMessage: async (_text: string) => {} };
}
