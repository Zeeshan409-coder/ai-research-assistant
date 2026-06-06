import axios from "axios"

const API_BASE_URL = "http://localhost:8000"

// 🛡️ Bulletproof Substring Cookie Extraction Engine
// Guarantees token readings clear successfully even with padding spaces or encoding variations
const getAuthToken = (): string | null => {
  if (typeof document === "undefined") return null
  
  const name = "auth_token="
  const decodedCookie = decodeURIComponent(document.cookie)
  const cookieArray = decodedCookie.split(';')
  
  for (let i = 0; i < cookieArray.length; i++) {
    let cookie = cookieArray[i]
    while (cookie.charAt(0) === ' ') {
      cookie = cookie.substring(1)
    }
    if (cookie.indexOf(name) === 0) {
      return cookie.substring(name.length, cookie.length)
    }
  }
  return null
}

export const api = {
  // Scoped Multi-Tenant Authentication Network Operations
  loginUser: async (email: string, password: string) => {
    const response = await axios.post(`${API_BASE_URL}/auth/login`, { email, password })
    return response.data
  },

  registerUser: async (email: string, password: string) => {
    const response = await axios.post(`${API_BASE_URL}/auth/register`, { email, password })
    return response.data
  },

  // Workspace Scoped Network Operations (Fully Hydrated with Bearer Token Injection)
  getWorkspaces: async () => {
    const token = getAuthToken()
    const headers = token ? { Authorization: `Bearer ${token}` } : {}
    const response = await axios.get(`${API_BASE_URL}/workspaces`, { headers })
    return response.data
  },
  
  createWorkspace: async (name: string) => {
    const token = getAuthToken()
    const headers = token ? { Authorization: `Bearer ${token}` } : {}
    const response = await axios.post(`${API_BASE_URL}/workspaces`, { name }, { headers })
    return response.data
  },

  getWorkspaceStats: async (workspaceId: string) => {
    const token = getAuthToken()
    const headers = token ? { Authorization: `Bearer ${token}` } : {}
    const response = await axios.get(`${API_BASE_URL}/workspaces/${workspaceId}/stats`, { headers })
    return response.data
  },

  getWorkspaceDocuments: async (workspaceId: string) => {
    const token = getAuthToken()
    const headers = token ? { Authorization: `Bearer ${token}` } : {}
    const response = await axios.get(`${API_BASE_URL}/workspaces/${workspaceId}/documents`, { headers })
    return response.data
  },

  // Scoped Conversation History Operations
  getConversations: async () => {
    const token = getAuthToken()
    const headers = token ? { Authorization: `Bearer ${token}` } : {}
    const response = await axios.get(`${API_BASE_URL}/conversations`, { headers })
    return response.data
  }
}
