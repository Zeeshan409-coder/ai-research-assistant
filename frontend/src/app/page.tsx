"use client"

import React, { useEffect, useState } from "react"
import { useAuthStore } from "../store/authStore"
import { useChatStore } from "../store/chatStore"
import { api } from "../lib/api"
import WorkspaceSidebar from "../components/chat/WorkspaceSidebar"
import { 
  FileText, 
  MessageSquare, 
  Database, 
  BarChart3, 
  LogOut, 
  FolderHeart,
  LayoutDashboard // 👈 Explicitly imported to prevent runtime ReferenceErrors!
} from "lucide-react"

export default function HomeDashboardPage() {
  const { user, logout } = useAuthStore()
  const { activeWorkspaceId, workspaces } = useChatStore()
  
  const [stats, setStats] = useState({ documents: 0, conversations: 0, chunks: 0 })
  const [documents, setDocuments] = useState([])
  const [loading, setLoading] = useState(false)

  const activeWorkspaceName = workspaces.find(w => w.id === activeWorkspaceId)?.name || "Select a Workspace"

  useEffect(() => {
    if (!activeWorkspaceId) return

    const fetchWorkspaceData = async () => {
      setLoading(true)
      try {
        const statsData = await api.getWorkspaceStats(activeWorkspaceId)
        const docsData = await api.getWorkspaceDocuments(activeWorkspaceId)
        setStats(statsData)
        setDocuments(docsData)
      } catch (error) {
        console.error("Failed to fetch dashboard data:", error)
      } finally {
        setLoading(false)
      }
    }

    fetchWorkspaceData()
  }, [activeWorkspaceId])

  return (
    <main className="flex h-screen w-full bg-zinc-950 text-zinc-100 antialiased overflow-hidden">
      <WorkspaceSidebar />

      <div className="flex-1 flex flex-col justify-between p-8 overflow-y-auto">
        {/* Header Section */}
        <header className="flex items-center justify-between border-b border-zinc-800 pb-6">
          <div>
            <h1 className="text-2xl font-bold tracking-tight flex items-center gap-2">
              <FolderHeart className="h-6 w-6 text-indigo-400" />
              {activeWorkspaceName}
            </h1>
            <p className="text-xs text-zinc-500 mt-1">
              User: <span className="text-indigo-400 font-medium">{user?.email || "saas_user@example.com"}</span>
            </p>
          </div>
          
          <button
            onClick={() => logout()}
            className="flex items-center gap-2 text-xs bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 hover:border-zinc-700 px-4 py-2 rounded-lg font-medium tracking-wide transition-colors cursor-pointer select-none"
          >
            <LogOut className="h-3.5 w-3.5" />
            <span>Sign Out</span>
          </button>
        </header>

        {activeWorkspaceId ? (
          <div className="flex-1 space-y-8 mt-6">
            {/* Metrics Dashboard Row Summary Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 flex items-center justify-between">
                <div>
                  <p className="text-xs font-semibold text-zinc-500 uppercase tracking-wider">Documents</p>
                  <h3 className="text-3xl font-bold mt-2 text-indigo-400">{loading ? "..." : stats.documents}</h3>
                </div>
                <FileText className="h-6 w-6 text-zinc-500" />
              </div>

              <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 flex items-center justify-between">
                <div>
                  <p className="text-xs font-semibold text-zinc-500 uppercase tracking-wider">Conversations</p>
                  <h3 className="text-3xl font-bold mt-2 text-emerald-400">{loading ? "..." : stats.conversations}</h3>
                </div>
                <MessageSquare className="h-6 w-6 text-zinc-500" />
              </div>

              <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 flex items-center justify-between">
                <div>
                  <p className="text-xs font-semibold text-zinc-500 uppercase tracking-wider">Chunks</p>
                  <h3 className="text-3xl font-bold mt-2 text-amber-400">{loading ? "..." : stats.chunks}</h3>
                </div>
                <Database className="h-6 w-6 text-zinc-500" />
              </div>
            </div>

            {/* Document Collection List Data Matrix Table */}
            <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 space-y-4">
              <h2 className="text-lg font-bold tracking-tight flex items-center gap-2">
                <BarChart3 className="h-5 w-5 text-indigo-400" />
                Workspace Documents
              </h2>
              
              <div className="border border-zinc-800 rounded-lg overflow-hidden bg-zinc-950/40">
                {documents.length > 0 ? (
                  <div className="divide-y divide-zinc-800">
                    {documents.map((doc: any) => (
                      <div key={doc.id} className="p-4 flex items-center justify-between text-sm hover:bg-zinc-900/50 transition-colors">
                        <div className="flex items-center gap-3">
                          <FileText className="h-4 w-4 text-zinc-500" />
                          <span className="font-medium text-zinc-200">{doc.filename}</span>
                        </div>
                        <div className="text-xs text-zinc-500 flex gap-4">
                          <span>Pages: {doc.total_pages}</span>
                          <span>Chunks: {doc.total_chunks}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-xs text-zinc-500 text-center py-8">
                    {loading ? "Loading files..." : "No documents in this workspace."}
                  </p>
                )}
              </div>
            </div>
          </div>
        ) : (
          /* Empty Active Selection View State */
          <div className="flex-1 flex flex-col items-center justify-center text-center opacity-60">
            <LayoutDashboard className="h-10 w-10 text-zinc-500 mb-4" />
            <p className="text-sm text-zinc-400">Select a workspace to view dashboard analytics.</p>
          </div>
        )}
      </div>
    </main>
  )
}
