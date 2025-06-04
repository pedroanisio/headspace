#!/bin/bash

# Headspace Project Quick Start Script
echo "🚀 Starting Headspace Project Portfolio..."

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for required tools
echo "🔍 Checking prerequisites..."

if ! command_exists uv; then
    echo "❌ UV not found. Please install UV: https://docs.astral.sh/uv/"
    exit 1
fi

if ! command_exists node; then
    echo "❌ Node.js not found. Please install Node.js 18+: https://nodejs.org/"
    exit 1
fi

if ! command_exists npm; then
    echo "❌ npm not found. Please install npm"
    exit 1
fi

echo "✅ All prerequisites found!"

# Start backend
echo "🔧 Setting up and starting backend..."
cd src/headspace-be

# Install Python dependencies
echo "📦 Installing Python dependencies with UV..."
uv pip install -e .

# Start FastAPI server in background
echo "🐍 Starting FastAPI server on port 8000..."
uv run python main.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Check if backend is running
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is running at http://localhost:8000"
    echo "📚 API Documentation: http://localhost:8000/api/docs"
else
    echo "❌ Backend failed to start"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Start frontend
echo "🔧 Setting up and starting frontend..."
cd ../headspace-fe

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# Start Next.js development server in background
echo "⚛️  Starting Next.js server on port 3000..."
npm run dev &
FRONTEND_PID=$!

# Wait a moment for frontend to start
sleep 5

# Check if frontend is running
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Frontend is running at http://localhost:3000"
else
    echo "❌ Frontend failed to start"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 1
fi

echo ""
echo "🎉 Headspace is now running!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔌 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/api/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    echo "✅ All services stopped"
    exit 0
}

# Trap Ctrl+C
trap cleanup INT

# Keep script running
wait 