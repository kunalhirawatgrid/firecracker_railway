# React Frontend

React frontend application built with Vite for Firecracker Railway.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Copy `.env.example` to `.env` and configure:
```bash
cp .env.example .env
```

3. Start the development server:
```bash
npm run dev
```

The application will be available at http://localhost:5173

## Build for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## Preview Production Build

```bash
npm run preview
```

## Environment Variables

See `.env.example` for all available environment variables.

### Available Variables

- `VITE_API_BASE_URL`: Base URL for the API (default: http://localhost:8000)
- `VITE_API_V1_STR`: API version prefix (default: /api/v1)

**Note:** All environment variables must be prefixed with `VITE_` to be accessible in the client-side code.
