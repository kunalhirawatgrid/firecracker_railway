# Coding Assessment Platform

A production-ready online coding assessment platform with secure code execution using gVisor sandbox. Candidates can solve coding problems with a timer, run code against test cases, and see compilation logs and test results.

## Features

### Candidate Features
- ⏱️ **Timer**: Real-time countdown timer for assessments
- 💻 **Multi-language Support**: Python, Java, C++, and JavaScript
- 🧪 **Test Cases**: Sample test cases (visible) and hidden test cases
- 🏃 **Run Code**: Execute code and see results for sample test cases
- 📊 **Test Results**: Detailed view of passed/failed test cases with inputs/outputs
- 📝 **Compilation Logs**: See compilation errors and execution logs
- ✅ **Submit**: Submit final solution with hidden test case evaluation

### Technical Features
- 🔒 **Secure Execution**: Code runs in gVisor sandbox for isolation
- 🗄️ **JSON Storage**: In-memory database using JSON files
- 🚀 **FastAPI Backend**: High-performance async API
- ⚛️ **React Frontend**: Modern UI with Monaco editor
- 🐳 **Docker Integration**: Uses Docker with gVisor runtime

## Architecture

```
┌─────────────┐
│   Frontend  │  React + Vite + Monaco Editor
│  (React)    │
└──────┬──────┘
       │ HTTP/REST
┌──────▼──────┐
│   Backend   │  FastAPI
│  (FastAPI)  │
└──────┬──────┘
       │
┌──────▼──────┐
│   gVisor    │  Docker + runsc runtime
│  Executor   │
└─────────────┘
```

## Prerequisites

### System Requirements
- Python 3.11+
- Node.js 18+
- Docker with gVisor runtime installed
- Linux/macOS (gVisor requires Linux, but can run on macOS with Docker)

### Installing gVisor

1. **Install Docker** (if not already installed)

2. **Install gVisor runtime**:
   ```bash
   # On Linux
   curl -fsSL https://gvisor.dev/install | bash
   
   # Or download from: https://github.com/google/gvisor/releases
   ```

3. **Configure Docker to use gVisor**:
   ```bash
   # Add to /etc/docker/daemon.json
   {
     "runtimes": {
       "runsc": {
         "path": "/usr/local/bin/runsc",
         "runtimeArgs": []
       }
     }
   }
   
   # Restart Docker
   sudo systemctl restart docker
   ```

4. **Verify gVisor installation**:
   ```bash
   docker run --runtime=runsc hello-world
   ```

## Installation

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file (optional, uses defaults if not present):
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. Create storage directory:
   ```bash
   mkdir -p storage
   ```

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Running the Application

### Start Backend

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python main.py
```

Backend will run on `http://localhost:8000`

API documentation available at `http://localhost:8000/docs`

### Start Frontend

```bash
cd frontend
npm run dev
```

Frontend will run on `http://localhost:3000`

## Usage

1. **Access the application**: Open `http://localhost:3000` in your browser

2. **Default Assessment**: The app loads with a demo assessment if no assessment ID is provided

3. **Create Assessment** (via API):
   ```bash
   curl -X POST http://localhost:8000/api/v1/assessments \
     -H "Content-Type: application/json" \
     -d '{
       "title": "My Assessment",
       "description": "Test assessment",
       "duration": 60,
       "questions": [...]
     }'
   ```

4. **Take Assessment**:
   - Select a question from the sidebar
   - Write code in the editor
   - Click "Run Code" to test against sample test cases
   - Click "Submit" to evaluate against all test cases (including hidden)

## API Endpoints

### Assessments
- `GET /api/v1/assessments` - Get all assessments
- `GET /api/v1/assessments/{id}` - Get assessment by ID
- `POST /api/v1/assessments` - Create new assessment

### Code Execution
- `POST /api/v1/execute` - Execute code with optional input
- `POST /api/v1/execute/test` - Execute code and run test cases
- `GET /api/v1/execute/submissions` - Get submissions

### Health
- `GET /api/v1/health/health` - Health check

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/    # API endpoints
│   │   ├── core/                # Configuration
│   │   ├── db/                  # JSON storage
│   │   ├── models/              # Data models
│   │   ├── schemas/             # Pydantic schemas
│   │   └── services/            # Business logic
│   │       ├── gvisor_executor.py  # gVisor execution
│   │       └── code_executor.py   # Code execution service
│   ├── storage/                 # JSON database files
│   ├── main.py                  # FastAPI app
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── pages/               # Page components
│   │   └── services/            # API clients
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Configuration

### Backend Configuration (.env)

```env
HOST=0.0.0.0
PORT=8000
DEBUG=false

GVISOR_RUNTIME_PATH=/usr/local/bin/runsc
GVISOR_TIMEOUT=30
GVISOR_MEMORY_LIMIT=512m
GVISOR_CPU_LIMIT=1

STORAGE_PATH=./storage
```

### Frontend Configuration

Edit `frontend/src/services/api.js` to change API URL:
```javascript
const API_BASE_URL = 'http://your-backend-url/api/v1'
```

## Security Considerations

- Code execution is isolated in gVisor sandbox
- Containers run with network disabled
- Read-only filesystem for containers
- Memory and CPU limits enforced
- Timeout protection against infinite loops

## Production Deployment

### Backend
1. Use a production ASGI server (Gunicorn with Uvicorn workers)
2. Set up proper CORS origins
3. Use environment variables for sensitive config
4. Set up logging and monitoring
5. Use a proper database (PostgreSQL, MongoDB, etc.) instead of JSON

### Frontend
1. Build for production: `npm run build`
2. Serve static files with Nginx or similar
3. Configure proper API proxy
4. Enable HTTPS

### gVisor
1. Ensure gVisor is properly installed on production servers
2. Monitor resource usage
3. Set appropriate limits based on workload

## Troubleshooting

### gVisor not found
- Verify gVisor is installed: `which runsc`
- Check Docker runtime configuration
- Ensure Docker has permission to use runsc

### Code execution fails
- Check Docker is running: `docker ps`
- Verify gVisor runtime: `docker run --runtime=runsc hello-world`
- Check backend logs for errors
- Verify code syntax for the selected language

### Frontend can't connect to backend
- Check backend is running on port 8000
- Verify CORS settings in backend
- Check browser console for errors
- Verify API URL in frontend config

## License

MIT License

## Contributing

Contributions welcome! Please open an issue or submit a pull request.

