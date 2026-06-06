"use client"

import React, { useEffect } from "react"
import { useAnalyticsStore } from "../../../store/analyticsStore" // 👈 Relative folder path alignment
import AnalyticsOverview from "../../../components/analytics/AnalyticsOverview"
import LatencyCard from "../../../components/analytics/LatencyCard"
import RetrievalCard from "../../../components/analytics/RetrievalCard"
import CitationCard from "../../../components/analytics/CitationCard"
import WorkspaceSidebar from "../../../components/chat/WorkspaceSidebar"
import { BarChart3, RotateCw } from "lucide-react"

export default function AnalyticsPage() {
  const { stats, evaluations, loading, fetchAnalytics } = useAnalyticsStore()

  useEffect(() => {
    fetchAnalytics()
  }, [fetchAnalytics])

  return (
    <main className="flex h-screen w-full bg-zinc-950 text-zinc-100 antialiased overflow-hidden">
      {/* Retain platform context continuity by including your multi-tenant workspace sidebar */}
      <WorkspaceSidebar />

      <div className="flex-1 flex flex-col p-8 overflow-y-auto space-y-8 select-none">
        {/* Header Section */}
        <header className="flex items-center justify-between border-b border-zinc-800 pb-6">
          <div>
            <h1 className="text-2xl font-bold tracking-tight flex items-center gap-2">
              <BarChart3 className="h-6 w-6 text-indigo-400" />
              Observability & RAG Analytics
            </h1>
            <p className="text-xs text-zinc-500 mt-1">
              Real-time evaluation tracing and system latency telemetry distribution ledger
            </p>
          </div>

          <button
            onClick={() => fetchAnalytics()}
            disabled={loading}
            className="flex items-center gap-2 text-xs bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 hover:border-zinc-700 px-4 py-2 rounded-lg font-medium tracking-wide transition-colors cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed"
          >
            <RotateCw className={`h-3.5 w-3.5 ${loading ? "animate-spin text-indigo-400" : ""}`} />
            <span>{loading ? "Refreshing..." : "Refresh Logs"}</span>
          </button>
        </header>

        {loading && !stats ? (
          /* High-Fidelity Loading State View */
          <div className="flex-1 flex flex-col items-center justify-center opacity-40 animate-pulse">
            <BarChart3 className="h-10 w-10 text-zinc-500 mb-2 animate-bounce" />
            <p className="text-sm text-zinc-400 tracking-wide font-mono">
              Extracting system telemetry logs and computing averages...
            </p>
          </div>
        ) : (
          /* Metrics Visualization Workspace Grid Canvas */
          <div className="space-y-8 animate-fade-in">
            {/* Row 1: Executive Key Performance Indicators Summary */}
            <AnalyticsOverview stats={stats} />

            {/* Row 2: Latency Trace Curve vs Semantic Context Relevance Bars */}
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
              <LatencyCard evaluations={evaluations} />
              <RetrievalCard evaluations={evaluations} />
            </div>

            {/* Row 3: Grounding Density Volumetric Area Fill Frame */}
            <CitationCard evaluations={evaluations} />
          </div>
        )}
      </div>
    </main>
  )
}
