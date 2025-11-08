# Firecracker Railway - Online Coding Assessment Platform

A production-ready online coding assessment platform with secure code execution using Firecracker microVMs. Built with FastAPI backend and React frontend.

## Features

- ✅ **Secure Code Execution**: Code runs in isolated Firecracker microVMs for maximum security
- ✅ **Multi-Language Support**: Python, Java, C++, and JavaScript
- ✅ **Timer Management**: Real-time countdown timer for assessments
- ✅ **Test Cases**: Sample and hidden test cases with detailed results
- ✅ **Code Editor**: Monaco Editor with syntax highlighting
- ✅ **Compilation Logs**: View compilation errors and execution output
- ✅ **Assessment Management**: Create, start, and manage coding assessments
- ✅ **Production Ready**: Environment-based configuration, error handling, and security

## Architecture

### Backend
- **FastAPI**: High-performance async API framework
- **JSON Storage**: In-memory JSON file-based storage (no database required)
- **Firecracker**: Secure microVM-based code execution

### Frontend
- **React**: UI framework
- **Vite**: Fast build tool
- **Monaco Editor**: Code editor with syntax highlighting
- **Axios**: HTTP client

## Project Structure

```
firecracker_railway/
├── backend/
│   ├── app/
│   │   ├── api/           # API endpoints
│   │   ├── core/          # Configuration
│   │   ├── db/            # Database session
│   │   ├── models/        # Database models
│   │   ├── schemas/       # Pydantic schemas
│   │   └── services/      # Business logic (Firecracker, code execution)
│   ├── alembic/           # Database migrations
│   ├── main.py            # Application entry point
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── components/    # React components
    │   ├── pages/         # Page components
    │   ├── services/         # API clients
    │   └── config/         # Configuration
    └── package.json
```

## Prerequisites

- Python 3.11+
- Node.js 18+ and npm
- Firecracker (optional, for production VM execution - falls back to subprocess for development)
- Docker (optional, for containerized deployment)

## Quick Start

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run server
uvicorn main:app --reload

# (Optional) Seed sample data for testing
python scripts/seed_data.py
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Start development server
npm run dev
```

## Environment Variables

### Backend (.env)

```env
# Project Settings
PROJECT_NAME=Firecracker Railway API
VERSION=1.0.0
API_V1_STR=/api/v1

# CORS Settings
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Server Settings
HOST=0.0.0.0
PORT=8000
DEBUG=false

# Storage Settings (JSON file storage)
STORAGE_FILE=data.json

# Firecracker VM Configuration
FIRECRACKER_SOCKET_PATH=/tmp/firecracker.socket
FIRECRACKER_KERNEL_PATH=/opt/firecracker/vmlinux.bin
FIRECRACKER_ROOTFS_PATH=/opt/firecracker/rootfs.ext4
FIRECRACKER_VM_TIMEOUT_SECONDS=30
FIRECRACKER_MAX_MEMORY_MB=512
FIRECRACKER_VCPU_COUNT=2

# Code Execution Limits
MAX_CODE_LENGTH=50000
MAX_EXECUTION_TIME_MS=10000
MAX_STDOUT_SIZE=100000
```

### Frontend (.env)

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_API_V1_STR=/api/v1
```

## API Endpoints

### Assessments

- `POST /api/v1/assessments` - Create assessment
- `GET /api/v1/assessments/{id}` - Get assessment
- `POST /api/v1/assessments/{id}/start` - Start assessment
- `GET /api/v1/assessments/{id}/questions` - Get questions
- `POST /api/v1/assessments/{id}/questions/{q_id}/submit` - Submit solution

### Code Execution

- `POST /api/v1/execute/run` - Execute code (for testing)

## Usage

### Creating an Assessment

```python
POST /api/v1/assessments
{
  "title": "Python Assessment",
  "description": "Test your Python skills",
  "duration_minutes": 60,
  "candidate_id": "candidate_1",
  "questions": [
    {
      "title": "Two Sum",
      "description": "Find two numbers that add up to target",
      "difficulty": "easy",
      "test_cases": [
        {
          "input_data": "2 7 11 15\n9",
          "expected_output": "[0, 1]",
          "is_sample": true
        }
      ]
    }
  ]
}
```

### Accessing Assessment

Navigate to: `http://localhost:5173/assessment/{assessment_id}?candidate_id={candidate_id}`

## Firecracker Integration

The platform uses [Firecracker microVMs](https://firecracker-microvm.github.io/) for secure code execution. Firecracker provides:

- **Security**: KVM-based isolation
- **Speed**: < 125ms startup time
- **Efficiency**: < 5 MiB memory footprint per microVM

### Setting Up Firecracker

1. Install Firecracker: https://github.com/firecracker-microvm/firecracker
2. Prepare kernel and rootfs images
3. Configure paths in `.env`

**Note**: For development/testing, the code execution service falls back to subprocess execution. For production, configure Firecracker properly.

## Supported Languages

- **Python**: Python 3.x
- **Java**: Java 11+
- **C++**: C++17 (g++)
- **JavaScript**: Node.js

## Production Deployment

### Security Considerations

1. **Code Execution**: Use Firecracker VMs in production
2. **Rate Limiting**: Implement rate limiting on code execution endpoints
3. **Input Validation**: All inputs are validated
4. **CORS**: Configure CORS origins properly
5. **Database**: Use connection pooling and prepared statements
6. **Secrets**: Store secrets in environment variables or secret management

### Docker Deployment

```dockerfile
# Example Dockerfile for backend
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Data Storage

The application uses JSON file-based storage located in `backend/storage/data.json`. This file is automatically created and managed by the application. For production, consider migrating to a proper database like PostgreSQL.

## Development

### Backend

- Code formatting: Black, isort
- Linting: flake8
- Type checking: mypy (optional)

### Frontend

- Code formatting: Prettier
- Linting: ESLint

## Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## License

MIT

## References

- [Firecracker Documentation](https://firecracker-microvm.github.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
