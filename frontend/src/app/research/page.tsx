"use client"

import React, { useState } from "react"
import axios from "axios"
import WorkspaceSidebar from "../../components/chat/WorkspaceSidebar"
import { useChatStore } from "../../store/chatStore"
import { ClipboardList, FileSearch, FileText, Send, Sparkles, Loader2, Globe, Database } from "lucide-react"

function getAuthToken(): string | null {
  if (typeof document === "undefined") return null
  const name = "auth_token="
  const decodedCookie = decodeURIComponent(document.cookie)
  const cookieArray = decodedCookie.split(";")
  
  for (let i = 0; i < cookieArray.length; i++) {
    let cookie = cookieArray[i]
    while (cookie.charAt(0) === " ") {
      cookie = cookie.substring(1)
    }
    if (cookie.indexOf(name) === 0) {
      return cookie.substring(name.length, cookie.length)
    }
  }
  return null
}

export default function AgenticResearchPage() {
  const { activeWorkspaceId } = useChatStore()
  const [query, setQuery] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<any | null>(null)

  const handleRunResearch = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim()) return
    if (!activeWorkspaceId) {
      setError("Please select a workspace folder inside the sidebar first.")
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const token = getAuthToken()
      const headers = token ? { Authorization: `Bearer ${token}` } : {}
      
      const response = await axios.post(
        "http://localhost:8000/research",
        {
          workspace_id: activeWorkspaceId,
          conversation_id: "agent_session_" + Date.now(),
          query: query
        },
        { headers }
      )

      setResult(response.data)
    } catch (err: any) {
      console.error(err)
      setError(err.response?.data?.detail || "The agentic orchestration pipeline faulted.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="flex h-screen w-full bg-zinc-950 text-zinc-100 antialiased overflow-hidden">
      <WorkspaceSidebar />

      <div className="flex-1 flex flex-col p-8 overflow-y-auto space-y-8 select-none">
        <header className="border-b border-zinc-800 pb-6">
          <h1 className="text-2xl font-bold tracking-tight flex items-center gap-2">
            <Sparkles className="h-6 w-6 text-indigo-400" />
            Agentic Research Workflows
          </h1>
          <p className="text-xs text-zinc-500 mt-1">
            Deploy deterministic multi-agent planner, retriever, web search, and evidence fusion report engines
          </p>
        </header>

        <form onSubmit={handleRunResearch} className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 shadow-xl space-y-4">
          <div className="flex flex-col space-y-2">
            <label className="text-xs font-semibold text-zinc-400 uppercase tracking-wider">Deep Investigation Directive</label>
            <div className="flex gap-4">
              <input
                type="text"
                placeholder="Ask the orchestrator to plan, extract from Qdrant, query Tavily, and synthesize a fused final report..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="flex-1 text-sm bg-zinc-950 border border-zinc-800 rounded-lg px-4 py-3 text-zinc-100 placeholder-zinc-600 focus:outline-none focus:border-indigo-500 transition-colors"
                disabled={loading}
                required
              />
              <button
                type="submit"
                disabled={loading}
                className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-sm px-6 py-3 rounded-lg transition-colors cursor-pointer shrink-0"
              >
                {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
                <span>{loading ? "Orchestrating..." : "Launch Agents"}</span>
              </button>
            </div>
          </div>
          {error && <p className="text-xs text-red-400 font-medium">{error}</p>}
        </form>

        {loading && (
          <div className="flex-1 flex flex-col items-center justify-center p-12 bg-zinc-900/40 border border-zinc-800 border-dashed rounded-xl text-center animate-pulse">
            <Loader2 className="h-8 w-8 text-indigo-400 animate-spin mb-4" />
            <p className="text-sm font-medium text-zinc-300 font-mono">Central Orchestrator parsing objectives...</p>
          </div>
        )}

        {result && (
          <div className="space-y-8 pb-12">
            <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 space-y-4">
              <h2 className="text-sm font-semibold text-zinc-200 uppercase tracking-wider flex items-center gap-2">
                <ClipboardList className="h-4 w-4 text-indigo-400" />
                1. Orchestration Research Plan Tasks
              </h2>
              <div className="space-y-2">
                {result.plan?.tasks?.map((task: any) => (
                  <div key={task.task_id} className="bg-zinc-950 border border-zinc-800 rounded-lg p-3 flex items-center justify-between text-sm">
                    <span className="font-medium text-zinc-200">{task.description}</span>
                    <span className="text-xs font-mono font-semibold px-2.5 py-1 bg-zinc-900 border border-zinc-700 text-zinc-400 rounded-md uppercase">
                      {task.task_type}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 space-y-4">
              <h2 className="text-sm font-semibold text-zinc-200 uppercase tracking-wider flex items-center gap-2">
                <FileSearch className="h-4 w-4 text-emerald-400" />
                2. Multi-Silo Evidence Fusion ({result.internal_chunks || 0} Internal / {result.web_sources || 0} Web)
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {result.evidence_summary?.internal?.map((ev: any, idx: number) => (
                  <div key={"int-" + idx} className="bg-zinc-950 border border-zinc-800 rounded-lg p-4 space-y-2 flex flex-col justify-between">
                    <p className="text-xs text-zinc-400 font-light leading-relaxed line-clamp-4 font-serif italic">"{ev.content}"</p>
                    <div className="flex items-center justify-between border-t border-zinc-800 pt-2 mt-2 text-[10px] font-mono text-zinc-500">
                      <span className="text-indigo-400 font-semibold flex items-center gap-1"><Database className="h-3 w-3" /> {ev.source}</span>
                      <span className="text-emerald-400 font-semibold">Score: {ev.score?.toFixed(4)}</span>
                    </div>
                  </div>
                ))}
                {result.evidence_summary?.web?.map((ev: any, idx: number) => (
                  <div key={"web-" + idx} className="bg-zinc-950 border border-zinc-800 rounded-lg p-4 space-y-2 flex flex-col justify-between">
                    <p className="text-xs text-zinc-400 font-light leading-relaxed line-clamp-4 font-serif italic">"{ev.content}"</p>
                    <div className="flex items-center justify-between border-t border-zinc-800 pt-2 mt-2 text-[10px] font-mono text-zinc-500">
                      <span className="text-amber-400 font-semibold flex items-center gap-1"><Globe className="h-3 w-3" /> Web Source</span>
                      <span className="text-zinc-500">External Data</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 space-y-4">
              <h2 className="text-sm font-semibold text-zinc-200 uppercase tracking-wider flex items-center gap-2">
                <FileText className="h-4 w-4 text-amber-400" />
                3. Summarizer Agent Synthesized Final Report
              </h2>
              <div className="bg-zinc-950 border border-zinc-800 rounded-xl p-6 text-sm text-zinc-300 leading-relaxed font-sans whitespace-pre-wrap select-text selection:bg-indigo-600 prose prose-invert max-w-none">
                {result.report}
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  )
}
