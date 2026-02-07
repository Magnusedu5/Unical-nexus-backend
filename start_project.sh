#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Cleanup function to kill background processes on script exit
cleanup() {
    echo ""
    echo ">>> Shutting down servers..."
    if [ -n "$DJANGO_PID" ]; then kill $DJANGO_PID 2>/dev/null; fi
    if [ -n "$VITE_PID" ]; then kill $VITE_PID 2>/dev/null; fi
    exit
}

# Trap script exit (e.g., Ctrl+C) and call the cleanup function
trap cleanup INT TERM EXIT

# --- Backend Setup ---
echo ">>> Setting up and starting Django backend..."

# Check for Python command
if command -v python3 &>/dev/null; then
    PYTHON_CMD=python3
else
    PYTHON_CMD=python
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ">>> Creating virtual environment..."
    $PYTHON_CMD -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

echo ">>> Installing backend dependencies..."
pip install -r requirements.txt


# Run database migrations
echo ">>> Applying database migrations..."
python manage.py migrate

# Start Django development server in the background
echo ">>> Starting Django server on http://localhost:8005..."
python manage.py runserver 8005 > django.log 2>&1 &
DJANGO_PID=$!

# --- Frontend Setup ---
echo ">>> Setting up and starting React frontend..."

# Navigate to the frontend directory
cd unical-nexus

# Install npm dependencies if node_modules is missing
if [ ! -d "node_modules" ]; then
    echo ">>> Installing npm dependencies..."
    npm install
fi

# Start the Vite development server
echo ">>> Starting Vite dev server on http://localhost:8080..."
npm run dev -- --port 8080 > ../frontend.log 2>&1 &
VITE_PID=$!

cd ..

echo ">>> Servers are running. Press Ctrl+C to stop."
echo ">>> Backend logs: django.log"
echo ">>> Frontend logs: frontend.log"

# Wait for background processes to finish (which they won't, until the script is terminated)
wait
