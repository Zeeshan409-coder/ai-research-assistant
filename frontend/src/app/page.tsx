"use client"

import React from "react"
import { useAuthStore } from "../store/authStore"
import WorkspaceSidebar from "../components/chat/WorkspaceSidebar"

export default function HomeDashboardPage() {
  const { user, logout } = useAuthStore()

  return (
    <main className="flex h-screen w-full bg-zinc-950 text-zinc-100 antialiased overflow-hidden">
      {/* Dynamic Multi-Document Scoped Workspace Folder Sidebar */}
      <WorkspaceSidebar />

      {/* Main Panel Content Canvas Container */}
      <div className="flex-1 flex flex-col justify-between p-8 relative">
        {/* Top Floating Dashboard Utilities Panel Header */}
        <header className="flex items-center justify-between border-b border-zinc-800 pb-4">
          <div>
            <h1 className="text-xl font-bold tracking-tight">AI Research Sandbox</h1>
            <p className="text-xs text-zinc-500">Authenticated Session Profile: <span className="text-indigo-400 font-medium">{user?.email || "SaaS Active Account"}</span></p>
          </div>
          
          <button
            onClick={() => logout()}
            className="text-xs bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 hover:border-zinc-700 px-3 py-1.5 rounded-lg font-medium tracking-wide transition-colors cursor-pointer select-none"
          >
            Sign Out
          </button>
        </header>

        {/* Dynamic Chat Canvas Loop Area */}
        <div className="flex-1 flex flex-col items-center justify-center text-center opacity-60">
          <p className="text-sm text-zinc-400 max-w-sm font-light leading-relaxed">
            Workspace context validated successfully completely offline! Choose a folder or paste your component script blocks to begin multi-turn streaming.
          </p>
        </div>
      </div>
    </main>
  )
}
