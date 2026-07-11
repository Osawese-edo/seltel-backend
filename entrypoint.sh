#!/bin/bash
set -e

echo "Starting Seltel API..."

# Run uvicorn with Render's PORT env var (default 8000 for local dev)
exec uvicorn src.app:app --host 0.0.0.0 --port "${PORT:-8000}"
