#!/bin/bash

echo "Starting DataFoundry Backend..."

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "Creating virtual environment..."
    cd backend
    python3 -m venv venv
    cd ..
fi

# Activate virtual environment
echo "Activating virtual environment..."
source backend/venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r backend/requirements.txt

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo "Creating .env file from example..."
    cp backend/.env.example backend/.env
    echo "Please edit backend/.env with your API keys before running the backend"
    exit 1
fi

# Start the backend server
echo "Starting FastAPI server..."
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000