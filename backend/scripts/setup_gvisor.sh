#!/bin/bash

# Setup script for gVisor installation
# This script helps set up gVisor runtime for Docker

set -e

echo "Setting up gVisor runtime for Docker..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if runsc is already installed
if command -v runsc &> /dev/null; then
    echo "gVisor (runsc) is already installed at $(which runsc)"
    RUNSC_PATH=$(which runsc)
else
    echo "Installing gVisor..."
    
    # Download and install gVisor
    curl -fsSL https://gvisor.dev/install | bash
    
    # Find runsc path
    RUNSC_PATH="/usr/local/bin/runsc"
    
    if [ ! -f "$RUNSC_PATH" ]; then
        echo "Error: gVisor installation failed. runsc not found at $RUNSC_PATH"
        exit 1
    fi
    
    echo "gVisor installed successfully at $RUNSC_PATH"
fi

# Configure Docker to use gVisor
DOCKER_DAEMON_JSON="/etc/docker/daemon.json"

if [ -f "$DOCKER_DAEMON_JSON" ]; then
    echo "Backing up existing Docker daemon.json..."
    sudo cp "$DOCKER_DAEMON_JSON" "${DOCKER_DAEMON_JSON}.backup"
fi

# Create or update daemon.json
echo "Configuring Docker to use gVisor runtime..."
sudo tee "$DOCKER_DAEMON_JSON" > /dev/null <<EOF
{
  "runtimes": {
    "runsc": {
      "path": "$RUNSC_PATH",
      "runtimeArgs": []
    }
  }
}
EOF

# Restart Docker
echo "Restarting Docker..."
if command -v systemctl &> /dev/null; then
    sudo systemctl restart docker
elif command -v service &> /dev/null; then
    sudo service docker restart
else
    echo "Warning: Could not restart Docker automatically. Please restart Docker manually."
fi

# Verify installation
echo "Verifying gVisor installation..."
if docker run --runtime=runsc hello-world &> /dev/null; then
    echo "✓ gVisor is working correctly!"
else
    echo "✗ gVisor verification failed. Please check the installation."
    exit 1
fi

echo ""
echo "Setup complete! gVisor is ready to use."
echo "You can test it with: docker run --runtime=runsc hello-world"

