import { create } from "zustand"
import { api } from "../lib/api" // Clean relative folder path lookup mapping

export interface UserProfile {
  id: string
  email: string
  created_at: string
}

interface AuthState {
  accessToken: string | null
  user: UserProfile | null
  isAuthenticated: boolean
  isLoading: boolean
  authError: string | null

  // Cryptographic Multi-Tenant SaaS State Dispatches
  login: (email: string, password: string) => Promise<boolean>
  logout: () => void
  setAuthError: (error: string | null) => void
}

export const useAuthStore = create<AuthState>((set) => ({
  accessToken: null,
  user: null,
  isAuthenticated: false,
  isLoading: false,
  authError: null,

  login: async (email, password) => {
    set({ isLoading: true, authError: null })
    try {
      // 🛡️ STEP 7 CRITICAL ALIGNMENT: Pass email and password variables explicitly as separate parameters
      // This allows our API adapter to package them into the required OAuth2 URLSearchParams format!
      const data = await api.loginUser(email, password)
      const token = data.access_token

      // 🔐 Edge Network Firewall Cookie Synchronization Layer
      const maxAge = 7 * 24 * 60 * 60
      document.cookie = `auth_token=${token}; path=/; max-age=${maxAge}; SameSite=Strict; Secure`

      const userProfile: UserProfile = {
        id: "session_user",
        email: email,
        created_at: new Date().toISOString()
      }

      set({
        accessToken: token,
        user: userProfile,
        isAuthenticated: true,
        isLoading: false
      })
      return true
    } catch (error: any) {
      // Catch backend validation faults or cryptographic signature failures gracefully
      const fallbackMessage = error.response?.data?.detail || "Invalid email address or password credentials."
      set({ 
        authError: fallbackMessage, 
        isLoading: false, 
        isAuthenticated: false 
      })
      return false
    }
  },

  logout: () => {
    // Clear browser cookie maps to engage your middleware navigation blocks instantly
    document.cookie = "auth_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT"
    set({
      accessToken: null,
      user: null,
      isAuthenticated: false,
      authError: null
    })
  },

  setAuthError: (error) => set({ authError: error })
}))
