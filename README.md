# Firecracker Railway

A full-stack application with FastAPI backend and React frontend built with Vite.

## Project Structure

```
firecracker_railway/
├── backend/          # FastAPI backend
│   ├── app/         # Application code
│   ├── main.py      # Application entry point
│   └── requirements.txt
└── frontend/        # React frontend with Vite
    ├── src/         # Source code
    └── package.json
```

## Prerequisites

- Python 3.11+ (for backend)
- Node.js 18+ and npm (for frontend)

## Quick Start

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
# Copy .env.example to .env (if not already present)
cp .env.example .env
# Edit .env with your settings
```

5. Run the server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment variables:
```bash
# Copy .env.example to .env (if not already present)
cp .env.example .env
# Edit .env with your settings
```

4. Start the development server:
```bash
npm run dev
```

The frontend will be available at http://localhost:5173

## Environment Variables

**Important:** All URLs and configuration values are stored in `.env` files. There are no hardcoded URLs in the codebase for production safety. Copy `.env.example` to `.env` and configure according to your environment.

### Backend (.env)

See `backend/.env.example` for the complete configuration. Required variables:

```env
# Required: CORS origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# For production, use your actual frontend URL(s):
# CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

**Note:** `CORS_ORIGINS` is required and must be set in `.env`. The application will fail to start if it's not configured.

### Frontend (.env)

See `frontend/.env.example` for the complete configuration. Required variables:

```env
# Required in production, optional in development (has localhost default)
VITE_API_BASE_URL=http://localhost:8000

# For production, use your actual backend URL:
# VITE_API_BASE_URL=https://api.yourdomain.com
```

**Note:** 
- Frontend environment variables must be prefixed with `VITE_` to be accessible in the client-side code.
- `VITE_API_BASE_URL` is required in production builds. In development, it defaults to `http://localhost:8000` if not set.

## Features

- ✅ FastAPI backend with proper project structure
- ✅ React frontend with Vite for fast development
- ✅ CORS configuration for cross-origin requests
- ✅ Environment variable management
- ✅ Production-ready code structure
- ✅ API documentation (Swagger/ReDoc)
- ✅ Health check endpoints

## Development

### Backend

- Code formatting: Uses Black and isort (configured in `pyproject.toml`)
- Linting: Configured with flake8 (`.flake8`)

### Frontend

- Code formatting: Prettier (`.prettierrc`)
- Linting: ESLint (configured in `eslint.config.js`)

## Production Build

### Backend

The backend runs with uvicorn. For production, use a process manager like systemd, supervisor, or a container orchestration tool.

### Frontend

```bash
cd frontend
npm run build
```

The production build will be in the `frontend/dist` directory.

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /api/v1/health` - API health check
- `GET /api/v1/example` - Example GET endpoint
- `POST /api/v1/example` - Example POST endpoint

## License

MIT
