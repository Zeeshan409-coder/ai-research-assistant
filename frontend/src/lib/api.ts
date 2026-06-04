import axios from "axios"

const API_BASE_URL = "http://localhost:8000"

export const api = {
  // Workspace Network Operations
  getWorkspaces: async () => {
    const response = await axios.get(`${API_BASE_URL}/workspaces`)
    return response.data
  },
  
  createWorkspace: async (name: string) => {
    const response = await axios.post(`${API_BASE_URL}/workspaces/`, { name })
    return response.data
  },

  // Scoped Conversation History Operations
  getConversations: async () => {
    const response = await axios.get(`${API_BASE_URL}/conversations/`)
    return response.data
  },

  createNewChat: async () => {
    const response = await axios.post(`${API_BASE_URL}/conversations/`)
    return response.data
  }
}
