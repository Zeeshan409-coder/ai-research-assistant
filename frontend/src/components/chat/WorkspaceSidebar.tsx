"use client"

import React, { useEffect, useState } from "react"
import { useChatStore } from "../../store/chatStore"
import { api } from "../../lib/api"
import { Folder, Plus, LayoutDashboard } from "lucide-react"

export default function WorkspaceSidebar() {
  // 🛡️ Added addWorkspace state modifier loop from your updated chatStore slice
  const { workspaces, setWorkspaces, activeWorkspaceId, setActiveWorkspaceId, addWorkspace } = useChatStore()
  const [newWorkspaceName, setNewWorkspaceName] = useState("")
  const [isCreating, setIsCreating] = useState(false)

  useEffect(() => {
    const loadWorkspaces = async () => {
      try {
        const data = await api.getWorkspaces()
        setWorkspaces(data)
        if (data.length > 0 && !activeWorkspaceId) {
          setActiveWorkspaceId(data[0].id) // Default auto-loads the primary collection tracking row safely
        }
      } catch (error) {
        console.error("Failed to fetch multi-tenant workspace list:", error)
      }
    }
    loadWorkspaces()
  }, [setWorkspaces, setActiveWorkspaceId, activeWorkspaceId])

  const handleCreateWorkspace = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!newWorkspaceName.trim()) return

    try {
      // 1. Submit the clean native JSON payload down to your FastAPI port
      const created = await api.createWorkspace(newWorkspaceName)
      
      // 2. Hydrate your global state array list natively to trigger visual updates instantly!
      addWorkspace(created)
      
      // 3. Clear out text form tracking string values
      setNewWorkspaceName("")
      setIsCreating(false)
    } catch (error) {
      console.error("Failed to provision sandboxed workspace entity partition:", error)
    }
  }

  return (
    <aside className="w-64 bg-zinc-900 border-r border-zinc-800 text-zinc-100 flex flex-col h-full min-h-screen p-4 select-none">
      {/* Central Interactive Platform Brand Title Logo */}
      <div 
        className="flex items-center gap-2 mb-6 px-2 cursor-pointer" 
        onClick={() => setActiveWorkspaceId(null)}
      >
        <LayoutDashboard className="h-5 w-5 text-indigo-400" />
        <h2 className="font-bold text-lg tracking-tight">AI Assistant</h2>
      </div>

      {/* Subheader Interaction Context Controls Link Bar */}
      <div className="flex items-center justify-between mb-3 px-2">
        <span className="text-xs font-semibold text-zinc-400 uppercase tracking-wider">Workspaces</span>
        <button 
          onClick={() => setIsCreating(!isCreating)}
          className="p-1 rounded text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 transition-colors cursor-pointer"
          title="Create New Sandboxed Workspace"
        >
          <Plus className="h-4 w-4" />
        </button>
      </div>

      {/* Dynamic Creation Inline Form Entry Row Slot */}
      {isCreating && (
        <form onSubmit={handleCreateWorkspace} className="mb-4 px-2">
          <input
            type="text"
            placeholder="Workspace Name..."
            value={newWorkspaceName}
            onChange={(e) => setNewWorkspaceName(e.target.value)}
            className="w-full text-sm bg-zinc-950 border border-zinc-800 rounded p-2 text-zinc-100 placeholder-zinc-600 focus:outline-none focus:border-indigo-500 transition-colors"
            autoFocus
            required
          />
        </form>
      )}

      {/* Render Workspace Folder Entities Tracking Loop Blocks Grid */}
      <div className="flex-1 overflow-y-auto space-y-1 pr-1">
        {workspaces.map((ws) => {
          const isActive = ws.id === activeWorkspaceId
          return (
            <button
              key={ws.id}
              onClick={() => setActiveWorkspaceId(ws.id)}
              className={`w-full flex items-center gap-3 px-3 py-2 text-sm font-medium rounded transition-colors text-left cursor-pointer ${
                isActive 
                  ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/10" 
                  : "text-zinc-400 hover:bg-zinc-800 hover:text-zinc-100"
              }`}
            >
              <Folder className={`h-4 w-4 shrink-0 ${isActive ? "text-white" : "text-zinc-500"}`} />
              <span className="truncate">{ws.name}</span>
            </button>
          )
        })}

        {workspaces.length === 0 && !isCreating && (
          <p className="text-xs text-zinc-500 text-center py-4 px-2 font-light">
            No workspaces found. Click + to create one.
          </p>
        )}
      </div>
    </aside>
  )
}
