#!/bin/bash

echo "🚀 Starting DataFoundry..."

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command_exists node; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

if ! command_exists python3; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Prerequisites check passed!"

# Setup frontend
echo "🎨 Setting up frontend..."
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

# Create .env.local if it doesn't exist
if [ ! -f ".env.local" ]; then
    echo "Creating frontend environment file..."
    echo "BACKEND_URL=http://localhost:8000" > .env.local
fi

# Setup backend
echo "🔧 Setting up backend..."
if [ ! -d "backend/venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv backend/venv
fi

echo "Installing Python dependencies..."
source backend/venv/bin/activate
pip install -r backend/requirements.txt

# Check if API key is set
if grep -q "your_gemini_api_key_here" backend/.env; then
    echo "⚠️  Please set your GEMINI_API_KEY in backend/.env file"
    echo "   Get your API key from: https://makersuite.google.com/app/apikey"
    exit 1
fi

echo "✅ Setup complete!"
echo ""
echo "🚀 Starting services..."
echo "   Frontend will be available at: http://localhost:3000"
echo "   Backend API will be available at: http://localhost:8000"
echo "   API Documentation at: http://localhost:8000/docs"
echo ""

# Start backend in background
echo "Starting backend server..."
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "Starting frontend server..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo "🎉 DataFoundry is running!"
echo "   Frontend: http://localhost:3000"
echo "   Backend: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for user to stop
wait