/**
 * API client for communicating with the backend.
 */
import { env } from '../config/env';

const API_BASE_URL = `${env.API_BASE_URL}${env.API_V1_STR}`;

/**
 * Create a fetch request with default options.
 * @param {string} endpoint - API endpoint
 * @param {RequestInit} options - Fetch options
 * @returns {Promise<Response>}
 */
async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(url, defaultOptions);
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({
        message: `HTTP error! status: ${response.status}`,
      }));
      throw new Error(errorData.message || 'An error occurred');
    }
    
    return await response.json();
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
}

/**
 * API client methods.
 */
export const api = {
  /**
   * Health check.
   */
  health: () => apiRequest('/health'),

  /**
   * Get example data.
   */
  getExample: () => apiRequest('/example'),

  /**
   * Post example data.
   */
  postExample: (data) =>
    apiRequest('/example', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
};

export default api;

