"use client"

import React from "react"
import MetricCard from "./MetricCard"

interface AnalyticsOverviewProps {
  stats: {
    total_requests?: number
    avg_latency_ms?: number
    avg_chunks_retrieved?: number
    avg_citation_coverage?: number
  } | null
}

export default function AnalyticsOverview({ stats }: AnalyticsOverviewProps) {
  // 🛡️ Fallback Isolation: Guard against empty database state or connection stalls
  const totalRequests = stats?.total_requests ?? 0
  const avgLatency = stats?.avg_latency_ms ?? 0
  const avgChunks = stats?.avg_chunks_retrieved ?? 0
  const rawCoverage = stats?.avg_citation_coverage ?? 0

  // Format citation ratio into clean display percentage text
  const formattedCoverage = `${(rawCoverage * 100).toFixed(1)}%`

  return (
    <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 selection:bg-indigo-600">
      <MetricCard
        title="Total Requests"
        value={totalRequests}
        description="Cumulative RAG executions across user workspaces"
      />

      <MetricCard
        title="Avg Latency"
        value={`${avgLatency} ms`}
        description="End-to-end response turnaround performance metric"
      />

      <MetricCard
        title="Avg Chunks"
        value={avgChunks}
        description="Average context nodes pulled out of vector memory"
      />

      <MetricCard
        title="Citation Coverage"
        value={formattedCoverage}
        description="Ratio of source chunks cited in final LLM outputs"
      />
    </div>
  )
}
