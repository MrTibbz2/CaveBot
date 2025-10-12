#!/bin/bash

set -e

echo "Installing CaveCore dependencies..."

# Update system
sudo apt-get update

# Install Python3 and pip
sudo apt-get install -y python3 python3-pip

# Install required Python packages
pip3 install pyserial websockets pybricksconnect

echo "Setup complete! Run with: python3 main.py"
