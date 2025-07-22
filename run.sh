#!/bin/bash

# Python Mathematical Console - Quick Start Script
# This script sets up and runs the Python Mathematical Console

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🐍 Python Mathematical Console - Quick Start${NC}"
echo "=================================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install Python dependencies
install_dependencies() {
    echo -e "${YELLOW}📦 Installing Python dependencies...${NC}"
    
    if command_exists uv; then
        echo "Using uv for faster installation..."
        uv pip install --system streamlit numpy scipy matplotlib plotly
    elif command_exists pip; then
        echo "Using pip for installation..."
        pip install streamlit numpy scipy matplotlib plotly
    else
        echo -e "${RED}❌ Neither pip nor uv found. Please install Python package manager.${NC}"
        exit 1
    fi
}

# Function to check Python version
check_python() {
    if command_exists python3; then
        PYTHON_CMD="python3"
    elif command_exists python; then
        PYTHON_CMD="python"
    else
        echo -e "${RED}❌ Python not found. Please install Python 3.11 or higher.${NC}"
        exit 1
    fi
    
    # Check Python version
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
    MAJOR_VERSION=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    MINOR_VERSION=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [ "$MAJOR_VERSION" -eq 3 ] && [ "$MINOR_VERSION" -ge 11 ]; then
        echo -e "${GREEN}✅ Python $PYTHON_VERSION detected${NC}"
    else
        echo -e "${YELLOW}⚠️  Python $PYTHON_VERSION detected. Recommended: Python 3.11+${NC}"
    fi
}

# Function to setup environment
setup_environment() {
    echo -e "${YELLOW}🛠️  Setting up environment...${NC}"
    
    # Create sessions directory if it doesn't exist
    mkdir -p sessions
    
    # Setup completed - no additional configuration needed
}

# Function to run with Docker
run_docker() {
    echo -e "${BLUE}🐳 Running with Docker...${NC}"
    
    if command_exists docker; then
        if command_exists docker-compose; then
            echo "Using Docker Compose..."
            docker-compose up --build
        else
            echo "Using Docker directly..."
            docker build -t python-math-console .
            docker run -p 5000:5000 python-math-console
        fi
    else
        echo -e "${RED}❌ Docker not found. Installing dependencies locally...${NC}"
        run_local
    fi
}

# Function to run locally
run_local() {
    echo -e "${BLUE}🚀 Running locally...${NC}"
    
    check_python
    install_dependencies
    setup_environment
    
    echo -e "${GREEN}✅ Starting Python Mathematical Console...${NC}"
    echo -e "${BLUE}📱 Access the application at: http://localhost:5000${NC}"
    echo -e "${YELLOW}📝 Press Ctrl+C to stop the server${NC}"
    echo ""
    
    streamlit run app.py --server.port 5000 --server.address 0.0.0.0 --server.headless true --theme.base dark
}

# Function to show help
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -d, --docker     Run using Docker (recommended for production)"
    echo "  -l, --local      Run locally with Python"
    echo "  -h, --help       Show this help message"
    echo "  -v, --version    Show version information"
    echo ""
    echo "Examples:"
    echo "  $0                # Auto-detect and run (tries Docker first, then local)"
    echo "  $0 --docker       # Force Docker execution"
    echo "  $0 --local        # Force local Python execution"
}

# Function to show version
show_version() {
    echo "Python Mathematical Console v1.0.0"
    echo "Built with Streamlit, NumPy, SciPy, and Matplotlib"
}

# Main execution logic
main() {
    case "${1:-}" in
        -d|--docker)
            run_docker
            ;;
        -l|--local)
            run_local
            ;;
        -h|--help)
            show_help
            ;;
        -v|--version)
            show_version
            ;;
        "")
            # Auto-detect best method
            if command_exists docker && [ -f docker-compose.yml ]; then
                echo -e "${BLUE}🔍 Docker detected. Running with Docker...${NC}"
                run_docker
            else
                echo -e "${BLUE}🔍 No Docker found. Running locally...${NC}"
                run_local
            fi
            ;;
        *)
            echo -e "${RED}❌ Unknown option: $1${NC}"
            show_help
            exit 1
            ;;
    esac
}

# Check if script is being sourced or executed
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi