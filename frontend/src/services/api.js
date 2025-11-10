import axios from 'axios'

// Get API URL from environment variable
// VITE_API_URL should be set in production (e.g., https://api.example.com/api/v1)
// For development, it falls back to the proxy or localhost
const getApiBaseUrl = () => {
  // Check if VITE_API_URL is explicitly set
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL
  }
  
  // In development, use proxy if available, otherwise localhost
  if (import.meta.env.DEV) {
    // Vite proxy will handle /api requests
    return '/api/v1'
  }
  
  // Production fallback (should be set via VITE_API_URL)
  return 'http://localhost:8000/api/v1'
}

const API_BASE_URL = getApiBaseUrl()

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 second timeout
})

// Add request interceptor for logging in development
if (import.meta.env.DEV) {
  api.interceptors.request.use(
    (config) => {
      console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`)
      return config
    },
    (error) => {
      console.error('[API] Request error:', error)
      return Promise.reject(error)
    }
  )
}

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error status
      console.error('[API] Response error:', error.response.status, error.response.data)
    } else if (error.request) {
      // Request made but no response
      console.error('[API] No response received:', error.request)
    } else {
      // Error setting up request
      console.error('[API] Request setup error:', error.message)
    }
    return Promise.reject(error)
  }
)

export default api

