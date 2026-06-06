import axios from "axios"

// 🛡️ Helper function to extract token values directly out of browser cookies array
const getAuthToken = (): string | null => {
  if (typeof document === "undefined") return null
  const name = "auth_token="
  const decodedCookie = decodeURIComponent(document.cookie)
  const cookieArray = decodedCookie.split(";")
  
  for (let i = 0; i < cookieArray.length; i++) {
    let cookie = cookieArray[i]
    while (cookie.charAt(0) === " ") {
      cookie = cookie.substring(1)
    }
    if (cookie.indexOf(name) === 0) {
      return cookie.substring(name.length, cookie.length)
    }
  }
  return null
}

// Instantiate custom telemetry client instance targeting your FastAPI port
const api = axios.create({
  baseURL: "http://localhost:8000"
})

// 🔐 Secure Token Interceptor Layer: Pre-authenticates all outbound requests
api.interceptors.request.use((config) => {
  const token = getAuthToken()
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, (error) => {
  return Promise.reject(error)
})

export async function getAnalyticsStats() {
  const response = await api.get("/analytics/evaluations/stats")
  return response.data
}

export async function getEvaluations() {
  const response = await api.get("/analytics/evaluations")
  return response.data
}
