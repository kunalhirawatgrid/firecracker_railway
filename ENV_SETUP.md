# Environment Variables Setup

This document describes all environment variables used in the application.

## Backend Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
# Server Configuration
HOST=0.0.0.0
PORT=8000                    # Overridden by PORT env var in cloud deployments (Railway, etc.)
DEBUG=false

# CORS Configuration
# In production, set specific origins (comma-separated)
# Example: https://yourdomain.com,https://www.yourdomain.com
# Use "*" for development only (NOT recommended for production)
CORS_ORIGINS=*

# gVisor Configuration
GVISOR_RUNTIME_PATH=/usr/local/bin/runsc
GVISOR_TIMEOUT=60
GVISOR_MEMORY_LIMIT=512m
GVISOR_CPU_LIMIT=1
GVISOR_FALLBACK_TO_DOCKER=false  # Set to true for development without gVisor

# Storage
STORAGE_PATH=./storage
```

### Production Backend Settings

For production deployments (Railway, Heroku, etc.):

```bash
# Railway/Cloud platforms automatically set PORT
# CORS should be set to your frontend domain
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
DEBUG=false
GVISOR_FALLBACK_TO_DOCKER=false  # Use gVisor in production
```

## Frontend Environment Variables

Create a `.env` file in the `frontend/` directory:

```bash
# API Configuration
# Set this to your backend API URL in production
# Example: https://api.yourdomain.com/api/v1
VITE_API_URL=

# Development proxy target (optional, defaults to http://localhost:8000)
VITE_API_PROXY_TARGET=http://localhost:8000

# Frontend port (optional, defaults to 3000)
VITE_PORT=3000
```

### Production Frontend Settings

For production builds:

```bash
# Set the full API URL
VITE_API_URL=https://api.yourdomain.com/api/v1
```

**Important:** Vite requires environment variables to be prefixed with `VITE_` to be exposed to the client-side code.

## Environment Variable Priority

1. **System environment variables** (highest priority)
2. **`.env` file** in the respective directory
3. **Default values** in code (lowest priority)

## Cloud Deployment Examples

### Railway

Backend:
- `PORT` is automatically set by Railway
- Set `CORS_ORIGINS` to your frontend URL
- Set `GVISOR_FALLBACK_TO_DOCKER=true` if gVisor is not available

Frontend:
- Set `VITE_API_URL` to your backend Railway URL
- Example: `VITE_API_URL=https://your-backend.railway.app/api/v1`

### Docker

Backend:
```bash
docker run -e PORT=8000 \
  -e CORS_ORIGINS=https://yourdomain.com \
  -e GVISOR_FALLBACK_TO_DOCKER=false \
  your-backend-image
```

Frontend:
```bash
docker run -e VITE_API_URL=https://api.yourdomain.com/api/v1 \
  your-frontend-image
```

## Security Notes

1. **Never commit `.env` files** - they are in `.gitignore`
2. **Use specific CORS origins in production** - don't use `*`
3. **Use HTTPS in production** - set API URLs with `https://`
4. **Keep secrets out of environment variables** - use secret management services

