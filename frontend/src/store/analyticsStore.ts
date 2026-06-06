import { create } from "zustand"
import { getAnalyticsStats, getEvaluations } from "../lib/analytics-api" // 👈 Explicit relative folder tracking path alignment

interface AnalyticsStore {
  stats: any
  evaluations: any[]
  loading: boolean
  fetchAnalytics: () => Promise<void>
}

export const useAnalyticsStore = create<AnalyticsStore>((set) => ({
  stats: null,
  evaluations: [],
  loading: false,

  fetchAnalytics: async () => {
    set({ loading: true })
    try {
      // 🚀 Concurrent Resolution: Fires both analytical data fetches simultaneously in parallel
      const [stats, evaluations] = await Promise.all([
        getAnalyticsStats(),
        getEvaluations()
      ])

      set({
        stats,
        evaluations,
        loading: false
      })
    } catch (error) {
      console.error("Failed to concurrently populate observability data stores:", error)
      set({ loading: false })
    }
  }
}))
