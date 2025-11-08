/**
 * Environment configuration.
 * Vite exposes env variables on import.meta.env
 * Variables prefixed with VITE_ are exposed to the client
 */
export const env = {
  API_BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  API_V1_STR: import.meta.env.VITE_API_V1_STR || '/api/v1',
  NODE_ENV: import.meta.env.MODE || 'development',
};

export const isDevelopment = env.NODE_ENV === 'development';
export const isProduction = env.NODE_ENV === 'production';

