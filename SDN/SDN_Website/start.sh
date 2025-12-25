#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}═══════════════════════════════════════════════${NC}"
echo -e "${BLUE}    SDN Management Platform - Full Startup${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════${NC}\n"

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "${YELLOW}Setting up Python environment...${NC}"
cd "$DIR"

# Check if virtual environment exists, if not create it
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Creating Python virtual environment...${NC}"
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install requirements
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install -r requirements.txt -q

echo -e "${GREEN}✓ Python environment ready${NC}\n"

# Start the API server
echo -e "${YELLOW}Starting API Server...${NC}"
python3 sdn_api_server.py &
API_PID=$!
echo -e "${GREEN}✓ API Server started (PID: $API_PID)${NC}"
echo -e "   ${BLUE}Available at: http://localhost:5000${NC}"
echo -e "   ${BLUE}API Endpoints:${NC}"
echo -e "      - GET  /api/stats - Network statistics"
echo -e "      - POST /api/attacks/simulate - Start attack"
echo -e "      - GET  /api/security/blocked-ips - List blocked IPs"
echo -e "      - WebSocket: ws://localhost:5000 - Real-time updates\n"

# Wait a moment for the API server to start
sleep 2

# Start the web server
echo -e "${YELLOW}Starting Web Server...${NC}"
python3 -m http.server 8000 -d "$DIR" &
WEB_PID=$!
echo -e "${GREEN}✓ Web Server started (PID: $WEB_PID)${NC}"
echo -e "   ${BLUE}Available at: http://localhost:8000${NC}\n"

echo -e "${GREEN}═══════════════════════════════════════════════${NC}"
echo -e "${GREEN}    ✓ All services are running!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════${NC}\n"

echo -e "${BLUE}Quick Start:${NC}"
echo -e "   1. Open browser: ${YELLOW}http://localhost:8000${NC}"
echo -e "   2. Navigate to ${YELLOW}Security Control${NC} page for attack simulation"
echo -e "   3. Create attacks to test the system\n"

echo -e "${BLUE}API Server Processes:${NC}"
echo -e "   ${YELLOW}API Server: $API_PID${NC}"
echo -e "   ${YELLOW}Web Server: $WEB_PID${NC}\n"

echo -e "${BLUE}To stop all services:${NC}"
echo -e "   ${YELLOW}kill $API_PID $WEB_PID${NC}"
echo -e "   ${YELLOW}Or press Ctrl+C in both terminals\n"

echo -e "${BLUE}Logs and Monitoring:${NC}"
echo -e "   - Check API logs above for attacks and connections"
echo -e "   - Open browser developer console (F12) for frontend logs"
echo -e "   - Check Network tab for API calls and WebSocket\n"

# Keep the script running
wait
