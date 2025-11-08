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

### Backend (.env)

```env
PROJECT_NAME=Firecracker Railway API
VERSION=1.0.0
API_V1_STR=/api/v1
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
HOST=0.0.0.0
PORT=8000
DEBUG=false
```

### Frontend (.env)

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_API_V1_STR=/api/v1
```

**Note:** Frontend environment variables must be prefixed with `VITE_` to be accessible in the client-side code.

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
