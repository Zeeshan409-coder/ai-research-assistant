import { create } from "zustand"

export interface Message {
  id?: string
  role: "user" | "assistant"
  content: string
  created_at?: string
}

export interface Conversation {
  id: string
  workspace_id?: string
  title: string
  created_at: string
}

export interface Workspace {
  id: string
  name: string
  created_at: string
}

interface ChatState {
  workspaces: Workspace[]
  activeWorkspaceId: string | null
  conversations: Conversation[]
  activeConversationId: string | null
  messages: Message[]
  isStreaming: boolean
  isLoading: boolean
  citations: any[]
  metrics: any | null
  
  // Actions
  setWorkspaces: (workspaces: Workspace[]) => void
  setActiveWorkspaceId: (id: string | null) => void
  setConversations: (conversations: Conversation[]) => void
  setActiveConversationId: (id: string | null) => void
  setMessages: (messages: Message[]) => void
  addMessage: (message: Message) => void
  updateLastMessageToken: (token: string) => void
  setIsStreaming: (status: boolean) => void
  setIsLoading: (status: boolean) => void
  setCitations: (citations: any[]) => void
  setMetrics: (metrics: any) => void
  clearChat: () => void
}

export const useChatStore = create<ChatState>((set) => ({
  workspaces: [],
  activeWorkspaceId: null,
  conversations: [],
  activeConversationId: null,
  messages: [],
  isStreaming: false,
  isLoading: false,
  citations: [],
  metrics: null,

  setWorkspaces: (workspaces) => set({ workspaces }),
  
  setActiveWorkspaceId: (id) => set({ 
    activeWorkspaceId: id,
    activeConversationId: null, // Clear active chat when shifting rooms
    messages: [],               // Wipe display message board loop
    citations: [],
    metrics: null 
  }),
  
  setConversations: (conversations) => set({ conversations }),
  setActiveConversationId: (id) => set({ activeConversationId: id, citations: [], metrics: null }),
  setMessages: (messages) => set({ messages }),
  
  addMessage: (message) => set((state) => ({ 
    messages: [...state.messages, message] 
  })),
  
  updateLastMessageToken: (token) => set((state) => {
    if (state.messages.length === 0) return {}
    const updatedMessages = [...state.messages]
    const lastMessage = updatedMessages[updatedMessages.length - 1]
    
    if (lastMessage.role === "assistant") {
      lastMessage.content += token
    }
    return { messages: updatedMessages }
  }),
  
  setIsStreaming: (status) => set({ isStreaming: status }),
  setIsLoading: (status) => set({ isLoading: status }),
  setCitations: (citations) => set({ citations }),
  setMetrics: (metrics) => set({ metrics }),
  
  clearChat: () => set({ 
    workspaces: [],
    messages: [], 
    activeConversationId: null, 
    activeWorkspaceId: null,
    citations: [], 
    metrics: null 
  })
}))
