"use client"

import React, { useState } from "react"
import { useAuthStore } from "../../store/authStore"
import { useRouter } from "next/navigation"
import { ShieldCheck, Lock, Mail, Loader2, LayoutDashboard } from "lucide-react" // 👈 Aligned to include LayoutDashboard

export default function LoginPage() {
  const { login, isLoading, authError } = useAuthStore()
  const router = useRouter()
  
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!email.trim() || !password.trim()) return

    const success = await login(email, password)
    if (success) {
      router.push("/")
      router.refresh()
    }
  }

  return (
    <main className="min-h-screen bg-zinc-950 flex flex-col items-center justify-center p-4 antialiased text-zinc-100 selection:bg-indigo-600">
      <div className="w-full max-w-md bg-zinc-900 border border-zinc-800 rounded-xl p-8 shadow-2xl space-y-6">
        
        <div className="flex flex-col items-center text-center space-y-2">
          <div className="p-3 bg-zinc-800/50 border border-zinc-700 rounded-xl">
            <ShieldCheck className="h-8 w-8 text-indigo-400" />
          </div>
          <h1 className="text-2xl font-bold tracking-tight">SaaS Portal</h1>
          <p className="text-sm text-zinc-400">Sign in to unlock your secure multi-document workspaces</p>
        </div>

        {authError && (
          <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-3 text-sm text-red-400 text-center">
            {authError}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-zinc-400 uppercase tracking-wider">Email Address</label>
            <div className="relative">
              <Mail className="absolute left-3 top-3 h-4 w-4 text-zinc-500" />
              <input
                type="email"
                placeholder="name@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full text-sm bg-zinc-950 border border-zinc-800 rounded-lg pl-10 pr-4 py-2.5 text-zinc-100 placeholder-zinc-600 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-colors"
                required
              />
            </div>
          </div>

          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-zinc-400 uppercase tracking-wider">Account Password</label>
            <div className="relative">
              <Lock className="absolute left-3 top-3 h-4 w-4 text-zinc-500" />
              <input
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full text-sm bg-zinc-950 border border-zinc-800 rounded-lg pl-10 pr-4 py-2.5 text-zinc-100 placeholder-zinc-600 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-colors"
                required
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-500 disabled:bg-indigo-600/50 text-white font-medium text-sm py-2.5 rounded-lg transition-colors cursor-pointer select-none"
          >
            {isLoading ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                <span>Authenticating Session...</span>
              </>
            ) : (
              <span>Sign In</span>
            )}
          </button>
        </form>

        <div className="text-center">
          <p className="text-xs text-zinc-500">
            Don&apos;t have an account yet? <span className="text-indigo-400 font-medium hover:underline cursor-pointer">Register natively here</span>
          </p>
        </div>

      </div>
    </main>
  )
}
