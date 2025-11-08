/**
 * API client for communicating with the backend.
 */
import axios from 'axios';
import { env } from '../config/env';

const API_BASE_URL = `${env.API_BASE_URL}${env.API_V1_STR}`;

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API request failed:', error);
    return Promise.reject(error);
  }
);

/**
 * API client methods.
 */
export const api = {
  /**
   * GET request.
   */
  get: (endpoint, config = {}) => apiClient.get(endpoint, config),

  /**
   * POST request.
   */
  post: (endpoint, data = {}, config = {}) => apiClient.post(endpoint, data, config),

  /**
   * PUT request.
   */
  put: (endpoint, data = {}, config = {}) => apiClient.put(endpoint, data, config),

  /**
   * DELETE request.
   */
  delete: (endpoint, config = {}) => apiClient.delete(endpoint, config),

  /**
   * Health check.
   */
  health: () => apiClient.get('/health'),

  /**
   * Get example data.
   */
  getExample: () => apiClient.get('/example'),

  /**
   * Post example data.
   */
  postExample: (data) => apiClient.post('/example', data),
};

export default api;

