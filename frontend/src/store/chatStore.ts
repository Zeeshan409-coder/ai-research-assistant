import { create } from "zustand"

export interface WorkspaceRecord {
  id: string
  name: string
  created_at: string
}

interface ChatState {
  workspaces: WorkspaceRecord[]
  activeWorkspaceId: string | null
  
  // Setters and Array Handlers
  setWorkspaces: (workspaces: WorkspaceRecord[]) => void
  setActiveWorkspaceId: (id: string | null) => void
  addWorkspace: (workspace: WorkspaceRecord) => void
}

export const useChatStore = create<ChatState>((set) => ({
  workspaces: [],
  activeWorkspaceId: null,

  setWorkspaces: (workspaces) => set({ workspaces }),
  
  setActiveWorkspaceId: (id) => set({ activeWorkspaceId: id }),
  
  // 👈 Crucial Update: Appends the fresh database workspace row into the active visual array list
  addWorkspace: (workspace) => set((state) => ({ 
    workspaces: [workspace, ...state.workspaces],
    activeWorkspaceId: workspace.id
  }))
}))
