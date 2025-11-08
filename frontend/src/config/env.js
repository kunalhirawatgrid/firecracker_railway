/**
 * Environment configuration.
 * Vite exposes env variables on import.meta.env
 * Variables prefixed with VITE_ are exposed to the client
 * 
 * All URLs must be set in .env file for production safety.
 * Development defaults are provided for local development convenience.
 */
const isDevelopment = import.meta.env.MODE === 'development';
const isProduction = import.meta.env.MODE === 'production';

const getEnvVar = (key, devDefault = null) => {
  const value = import.meta.env[key];
  
  // In production, require the env var to be set
  if (isProduction && !value) {
    throw new Error(
      `Environment variable ${key} is required in production but not set. ` +
      `Please set it in your .env file.`
    );
  }
  
  // In development, use provided default if value is not set
  if (!value && devDefault) {
    console.warn(
      `Environment variable ${key} not set, using development default: ${devDefault}. ` +
      `Set it in .env for production.`
    );
    return devDefault;
  }
  
  if (!value) {
    throw new Error(
      `Environment variable ${key} is required but not set. Please check your .env file.`
    );
  }
  
  return value;
};

export const env = {
  API_BASE_URL: getEnvVar('VITE_API_BASE_URL', isDevelopment ? 'http://localhost:8000' : null),
  API_V1_STR: getEnvVar('VITE_API_V1_STR', '/api/v1'),
  NODE_ENV: import.meta.env.MODE || 'development',
};

export { isDevelopment, isProduction };

