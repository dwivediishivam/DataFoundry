#!/bin/bash

echo "Starting DataFoundry Frontend..."

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

# Check if .env.local file exists
if [ ! -f ".env.local" ]; then
    echo "Creating .env.local file..."
    echo "BACKEND_URL=http://localhost:8000" > .env.local
fi

# Start the development server
echo "Starting Next.js development server..."
npm run dev