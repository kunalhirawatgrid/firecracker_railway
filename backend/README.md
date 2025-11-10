# Backend - Coding Assessment Platform

FastAPI backend for the coding assessment platform with gVisor code execution.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment (optional):
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. Run the server:
   ```bash
   python main.py
   ```

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## gVisor Setup

The backend requires gVisor runtime to be installed and configured with Docker. See main README for installation instructions.

## Testing

```bash
# Test health endpoint
curl http://localhost:8000/api/v1/health/health

# Create an assessment
curl -X POST http://localhost:8000/api/v1/assessments \
  -H "Content-Type: application/json" \
  -d @examples/assessment.json
```

