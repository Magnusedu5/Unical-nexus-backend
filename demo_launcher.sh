#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Cleanup function to kill background processes
cleanup() {
    echo ""
    echo ">>> Shutting down demo environment..."
    kill $(jobs -p) 2>/dev/null
    exit
}

# Trap Ctrl+C (SIGINT) and call cleanup
trap cleanup SIGINT SIGTERM

echo ">>> Starting Django Backend (Port 8005)..."
source venv/bin/activate
python manage.py runserver 8005 > backend.log 2>&1 &

echo ">>> Starting Vite Frontend (Port 8080)..."
cd unical-nexus
npm run dev -- --port 8080 > ../frontend.log 2>&1 &
cd ..

echo ">>> Waiting for servers to initialize..."
sleep 5

echo "-------------------------------------------------------"
echo "IMPORTANT: LocalTunnel requires a password to access the site."
echo "Fetching password..."
TUNNEL_PASSWORD=$(curl -s https://loca.lt/mytunnelpassword)
echo "Tunnel Password: $TUNNEL_PASSWORD"
echo "-------------------------------------------------------"

echo ">>> Starting LocalTunnel. Share the URL below with your client:"
npx -y localtunnel --port 8080