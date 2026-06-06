"use client"

import React, { useState } from "react"
import axios from "axios"
import WorkspaceSidebar from "../../components/chat/WorkspaceSidebar"
import { useChatStore } from "../../store/chatStore"
import { ClipboardList, FileSearch, FileText, Send, Sparkles, Loader2 } from "lucide-react"

// Helper function to extract token values directly out of browser cookies
const getAuthToken = (): string | null => {
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
      setError("Please select or create an active workspace folder inside the sidebar first.")
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
      console.error("Agentic framework network call exception:", err)
      setError(err.response?.data?.detail || "The agentic orchestration pipeline faulted during active loop execution.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="flex h-screen w-full bg-zinc-950 text-zinc-100 antialiased overflow-hidden">
      {/* Platform Left Folder Context Navigation Sidebar */}
      <WorkspaceSidebar />

      <div className="flex-1 flex flex-col p-8 overflow-y-auto space-y-8 select-none">
        {/* Header Section */}
        <header className="border-b border-zinc-800 pb-6">
          <h1 className="text-2xl font-bold tracking-tight flex items-center gap-2">
            <Sparkles className="h-6 w-6 text-indigo-400" />
            Agentic Research Workflows
          </h1>
          <p className="text-xs text-zinc-500 mt-1">
            Deploy deterministic multi-agent planner, retriever, and synthesis report engines
          </p>
        </header>

        {/* Query Input Box Component form */}
        <form onSubmit={handleRunResearch} className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 shadow-xl space-y-4">
          <div className="flex flex-col space-y-2">
            <label className="text-xs font-semibold text-zinc-400 uppercase tracking-wider">Deep Investigation Directive</label>
            <div className="flex gap-4">
              <input
                type="text"
                placeholder="Ask the orchestrator to plan, retrieve, and synthesize a deep research report..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="flex-1 text-sm bg-zinc-950 border border-zinc-800 rounded-lg px-4 py-3 text-zinc-100 placeholder-zinc-600 focus:outline-none focus:border-indigo-500 transition-colors"
                disabled={loading}
                required
              />
              <button
                type="submit"
                disabled={loading}
                className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 disabled:bg-indigo-600/40 text-white font-medium text-sm px-6 py-3 rounded-lg transition-colors cursor-pointer disabled:cursor-not-allowed shrink-0"
              >
                {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
                <span>{loading ? "Orchestrating..." : "Launch Agents"}</span>
              </button>
            </div>
          </div>
          {error && <p className="text-xs text-red-400 font-medium">{error}</p>}
        </form>

        {/* Loading Placeholders Canvas */}
        {loading && (
          <div className="flex-1 flex flex-col items-center justify-center p-12 bg-zinc-900/40 border border-zinc-800 border-dashed rounded-xl animate-pulse text-center">
            <Loader2 className="h-8 w-8 text-indigo-400 animate-spin mb-4" />
            <p className="text-sm font-medium text-zinc-300 font-mono">Central Orchestrator parsing objectives...</p>
            <p className="text-xs text-zinc-500 mt-1">Planner Agent generating structural research roadmap tasks.</p>
          </div>
        )}

        {/* Multi-Agent Sequential Tracking View Output Panel */}
        {result && (
          <div className="space-y-8 animate-fade-in pb-12">
            {/* Stage 1: The Research Execution Plan */}
            <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 space-y-4">
              <h2 className="text-sm font-semibold text-zinc-200 uppercase tracking-wider flex items-center gap-2">
                <ClipboardList className="h-4 w-4 text-indigo-400" />
                1. Orchestration Research Plan Tasks
              </h2>
              <div className="space-y-2">
                {result.plan?.tasks?.map((task: any) => (
                  <div key={task.task_id} className="bg-zinc-950 border border-zinc-800/80 rounded-lg p-3 flex items-center justify-between text-sm">
                    <div className="flex flex-col">
                      <span className="font-medium text-zinc-200">{task.description}</span>
                      <span className="text-[10px] font-mono text-zinc-500 mt-1">Task ID: {task.task_id}</span>
                    </div>
                    <span className="text-xs font-mono font-semibold px-2.5 py-1 bg-zinc-900 border border-zinc-700 text-zinc-400 rounded-md uppercase">
                      {task.task_type}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Stage 2: Evidence Summary Harvested */}
            <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 space-y-4">
              <h2 className="text-sm font-semibold text-zinc-200 uppercase tracking-wider flex items-center gap-2">
                <FileSearch className="h-4 w-4 text-emerald-400" />
                2. Retriever Agent Collected Evidence ({result.retrieved_chunks_count} Chunks)
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {result.evidence_summary?.map((ev: any, idx: number) => (
                  <div key={idx} className="bg-zinc-950 border border-zinc-800 rounded-lg p-4 space-y-2 flex flex-col justify-between">
                    <p className="text-xs text-zinc-400 font-light leading-relaxed line-clamp-4 font-serif italic">
                      "{ev.content}"
                    </p>
                    <div className="flex items-center justify-between border-t border-zinc-800 pt-2 mt-2 text-[10px] font-mono text-zinc-500">
                      <span className="truncate max-w-[150px]">{ev.source}</span>
                      <span className="text-emerald-400 font-semibold">Rank: {ev.score?.toFixed(4)}</span>
                    </div>
                  </div>
                ))}
                {result.evidence_summary?.length === 0 && (
                  <p className="text-xs text-zinc-500 col-span-2 py-2">No underlying document knowledge available in this workspace container slot.</p>
                )}
              </div>
            </div>

            {/* Stage 3: The Final Synthesis Generated Report */}
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
