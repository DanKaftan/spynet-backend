#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Run the server
echo "🚀 Starting SpyNet Backend..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
