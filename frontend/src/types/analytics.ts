export interface AnalyticsStats {
  avg_latency_ms: number
  avg_retrieval_ms: number
  avg_llm_ms: number
  total_requests: number
  avg_chunks_retrieved: number
  avg_citations: number
  avg_citation_coverage: number
  avg_rerank_score: number
}

export interface EvaluationRecord {
  id: string
  query: string
  retrieval_latency_ms: number
  llm_latency_ms: number
  total_latency_ms: number
  retrieved_chunks: number
  citations_used: number
  avg_rerank_score: number
  created_at: string
}
