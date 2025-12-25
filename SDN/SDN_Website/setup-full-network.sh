#!/bin/bash

# ============================================================================
# SDN NETWORK WITH DASHBOARD - COMPLETE STARTUP SCRIPT
# ============================================================================
# 
# This script starts the complete SDN network:
# - 3 Backend Servers (ports 8001, 8002, 8003)
# - SDN Controller/Load Balancer (port 5000)
# - Web Dashboard (port 8000)
# - Demo Clients
#
# ============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}    SDN Network with Real-Time Dashboard - Full Setup${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}\n"

# Store directories
BACKEND_DIR="/Users/omsai/Documents/OS/projects/SDN/SDN_LoadBalancer"
DASHBOARD_DIR="/Users/omsai/Documents/OS/projects/SDN/SDN_Website"

# Function to start bridge API
start_bridge_api() {
    echo -e "${YELLOW}Starting Bridge API (Dashboard-to-Controller Bridge)...${NC}"
    
    cd "$DASHBOARD_DIR"
    python3 bridge_api.py &
    PIDS+=($!)
    echo -e "${GREEN}✓ Bridge API started (PID: $!)${NC}"
    echo -e "   ${BLUE}Available at: http://localhost:9000${NC}"
    
    sleep 1
    echo ""
}

# Function to start backend servers
start_backend_servers() {
    echo -e "${YELLOW}Starting Backend Servers...${NC}"
    
    for port in 8001 8002 8003; do
        cd "$BACKEND_DIR"
        python3 backend_server.py $port &
        PIDS+=($!)
        echo -e "${GREEN}✓ Backend Server started on port $port (PID: $!)${NC}"
        sleep 1
    done
    
    echo ""
}

# Function to start SDN controller
start_controller() {
    echo -e "${YELLOW}Starting SDN Controller/Load Balancer...${NC}"
    
    cd "$BACKEND_DIR"
    export BACKENDS="http://localhost:8001,http://localhost:8002,http://localhost:8003"
    export PORT=5000
    python3 run.py &
    PIDS+=($!)
    echo -e "${GREEN}✓ SDN Controller started (PID: $!)${NC}"
    echo -e "   ${BLUE}Available at: http://localhost:5000${NC}"
    
    sleep 2
    echo ""
}

# Function to start dashboard
start_dashboard() {
    echo -e "${YELLOW}Starting Web Dashboard...${NC}"
    
    cd "$DASHBOARD_DIR"
    python3 -m http.server 8000 &
    PIDS+=($!)
    echo -e "${GREEN}✓ Web Dashboard started (PID: $!)${NC}"
    echo -e "   ${BLUE}Available at: http://localhost:8000${NC}"
    
    sleep 1
    echo ""
}

# Main execution
PIDS=()

echo -e "${YELLOW}Setting up network...${NC}\n"

# Start all services
start_backend_servers
start_controller
start_bridge_api
start_dashboard

echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}    ✓ All services are running!${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}\n"

echo -e "${BLUE}Network Architecture:${NC}"
echo -e "   Backend Servers:"
echo -e "      • Port 8001: Server 1"
echo -e "      • Port 8002: Server 2"
echo -e "      • Port 8003: Server 3"
echo -e ""
echo -e "   SDN Controller (Load Balancer):"
echo -e "      • Port 5000: http://localhost:5000"
echo -e ""
echo -e "   Web Dashboard:"
echo -e "      • Port 8000: http://localhost:8000"
echo -e ""

echo -e "${BLUE}Quick Start:${NC}"
echo -e "   1. Open browser: ${YELLOW}http://localhost:8000${NC}"
echo -e "   2. Open new terminal for client commands"
echo -e "   3. Run clients or attacks"
echo -e ""

echo -e "${BLUE}Available Commands in New Terminal:${NC}"
echo -e "   ${YELLOW}# Test load balancing:${NC}"
echo -e "   cd $BACKEND_DIR"
echo -e "   python3 demo_client.py"
echo -e ""
echo -e "   ${YELLOW}# Send attack traffic:${NC}"
echo -e "   python3 -c \"import requests; [requests.get('http://localhost:5000/balance') for _ in range(100)]\""
echo -e ""

echo -e "${BLUE}Process IDs:${NC}"
for i in "${!PIDS[@]}"; do
    echo -e "   ${PIDS[$i]}"
done
echo -e ""

echo -e "${BLUE}To stop all services:${NC}"
echo -e "   ${YELLOW}kill ${PIDS[@]}${NC}"
echo -e "   ${YELLOW}Or press Ctrl+C${NC}\n"

# Keep script running
echo -e "${GREEN}Services running. Press Ctrl+C to stop all.${NC}\n"

# Handle Ctrl+C
trap "echo 'Stopping all services...'; kill ${PIDS[@]} 2>/dev/null; exit 0" INT

# Wait for all processes
wait
