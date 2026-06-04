"use client"

import React, { useEffect, useState } from "react"
import { useChatStore } from "@/store/chatStore"
import { api } from "@/lib/api"
import { Folder, Plus, LayoutDashboard } from "lucide-react"

export default function WorkspaceSidebar() {
  const { workspaces, setWorkspaces, activeWorkspaceId, setActiveWorkspaceId } = useChatStore()
  const [newWorkspaceName, setNewWorkspaceName] = useState("")
  const [isCreating, setIsCreating] = useState(false)

  // Auto-fetch active workspace collections list from backend on mount
  useEffect(() => {
    const loadWorkspaces = async () => {
      try {
        const data = await api.getWorkspaces()
        setWorkspaces(data)
        // Auto-select the first available workspace partition if none is set
        if (data.length > 0 && !activeWorkspaceId) {
          setActiveWorkspaceId(data[0].id)
        }
      } catch (error) {
        console.error("Failed to load workspace data records:", error)
      }
    }
    loadWorkspaces()
  }, [setWorkspaces, setActiveWorkspaceId, activeWorkspaceId])

  const handleCreateWorkspace = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!newWorkspaceName.trim()) return

    try {
      const created = await api.createWorkspace(newWorkspaceName)
      setWorkspaces([created, ...workspaces])
      setActiveWorkspaceId(created.id)
      setNewWorkspaceName("")
      setIsCreating(false)
    } catch (error) {
      console.error("Failed to create workspace container partition:", error)
    }
  }

  return (
    <aside className="w-64 bg-zinc-900 border-r border-zinc-800 text-zinc-100 flex flex-col h-full min-h-screen p-4 select-none">
      {/* App Branding Head Title Header Layout */}
      <div className="flex items-center gap-2 mb-6 px-2">
        <LayoutDashboard className="h-5 w-5 text-indigo-400" />
        <h2 className="font-bold text-lg tracking-tight">AI Assistant</h2>
      </div>

      {/* Trigger Add Workspace Inline Form Button Element */}
      <div className="flex items-center justify-between mb-3 px-2">
        <span className="text-xs font-semibold text-zinc-400 uppercase tracking-wider">Workspaces</span>
        <button 
          onClick={() => setIsCreating(!isCreating)}
          className="p-1 rounded text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 transition-colors"
        >
          <Plus className="h-4 w-4" />
        </button>
      </div>

      {/* Render Dynamic Inline Entry Generation Box */}
      {isCreating && (
        <form onSubmit={handleCreateWorkspace} className="mb-4 px-2">
          <input
            type="text"
            placeholder="Workspace Name..."
            value={newWorkspaceName}
            onChange={(e) => setNewWorkspaceName(e.target.value)}
            className="w-full text-sm bg-zinc-800 border border-zinc-700 rounded p-2 text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-indigo-500 transition-colors"
            autoFocus
          />
        </form>
      )}

      {/* Render Active Relational Folders Collections Mapping Loops List */}
      <div className="flex-1 overflow-y-auto space-y-1 pr-1">
        {workspaces.map((ws) => {
          const isActive = ws.id === activeWorkspaceId
          return (
            <button
              key={ws.id}
              onClick={() => setActiveWorkspaceId(ws.id)}
              className={`w-full flex items-center gap-3 px-3 py-2 text-sm font-medium rounded transition-colors text-left ${
                isActive 
                  ? "bg-indigo-600 text-white" 
                  : "text-zinc-400 hover:bg-zinc-800 hover:text-zinc-100"
              }`}
            >
              <Folder className={`h-4 w-4 ${isActive ? "text-white" : "text-zinc-500"}`} />
              <span className="truncate">{ws.name}</span>
            </button>
          )
        })}

        {workspaces.length === 0 && !isCreating && (
          <p className="text-xs text-zinc-500 text-center py-4 px-2">No active workspaces found. Click + to create one.</p>
        )}
      </div>
    </aside>
  )
}
