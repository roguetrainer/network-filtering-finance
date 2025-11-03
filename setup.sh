#!/bin/bash

# Setup script for Animated Correlation Network Filtering
# This script creates a virtual environment and installs all required dependencies

set -e  # Exit on error

echo "============================================"
echo "Animated Correlation Network Filtering"
echo "Environment Setup Script"
echo "============================================"
echo ""

# Define Python path
PYTHON_PATH="/usr/local/bin/python3"

# Check if Python exists
if [ ! -f "$PYTHON_PATH" ]; then
    echo "Error: Python not found at $PYTHON_PATH"
    echo "Please install Python 3.8 or higher, or update PYTHON_PATH in this script."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_PATH --version 2>&1 | awk '{print $2}')
echo "Found Python version: $PYTHON_VERSION"
echo ""

# Define virtual environment directory
VENV_DIR="venv"

# Check if virtual environment already exists
if [ -d "$VENV_DIR" ]; then
    echo "Virtual environment already exists at ./$VENV_DIR"
    read -p "Do you want to remove it and create a new one? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Removing existing virtual environment..."
        rm -rf "$VENV_DIR"
    else
        echo "Using existing virtual environment."
        echo "To activate it, run: source $VENV_DIR/bin/activate"
        exit 0
    fi
fi

# Create virtual environment
echo "Creating virtual environment..."
$PYTHON_PATH -m venv "$VENV_DIR"
echo "✓ Virtual environment created at ./$VENV_DIR"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip
echo "✓ pip upgraded"
echo ""

# Install required packages
echo "Installing required packages..."
echo "This may take a few minutes..."
echo ""

pip install numpy>=1.21.0
echo "✓ numpy installed"

pip install pandas>=1.3.0
echo "✓ pandas installed"

pip install scipy>=1.7.0
echo "✓ scipy installed"

pip install networkx>=2.6.0
echo "✓ networkx installed"

pip install matplotlib>=3.4.0
echo "✓ matplotlib installed"

# Optional: Install Jupyter for running the notebook
read -p "Do you want to install Jupyter Notebook? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Installing Jupyter..."
    pip install jupyter ipykernel
    echo "✓ Jupyter installed"
    
    # Register the kernel
    python -m ipykernel install --user --name=correlation_networks --display-name="Python (Correlation Networks)"
    echo "✓ Jupyter kernel registered as 'Python (Correlation Networks)'"
fi

echo ""
echo "============================================"
echo "Installation Complete!"
echo "============================================"
echo ""
echo "Package versions installed:"
pip list | grep -E "numpy|pandas|scipy|networkx|matplotlib|jupyter"
echo ""
echo "To activate the virtual environment in the future, run:"
echo "  source $VENV_DIR/bin/activate"
echo ""
echo "To deactivate the virtual environment, run:"
echo "  deactivate"
echo ""
echo "To run the main script:"
echo "  python correlation_network_animation.py"
echo ""
echo "To run the Jupyter notebook:"
echo "  jupyter notebook examples.ipynb"
echo ""

# Check for ffmpeg
echo "Checking for ffmpeg (required for video export)..."
if command -v ffmpeg &> /dev/null; then
    FFMPEG_VERSION=$(ffmpeg -version 2>&1 | head -n 1)
    echo "✓ ffmpeg found: $FFMPEG_VERSION"
else
    echo "⚠ Warning: ffmpeg not found!"
    echo "  Video export will not work without ffmpeg."
    echo ""
    echo "  To install ffmpeg:"
    echo "    Ubuntu/Debian: sudo apt-get install ffmpeg"
    echo "    macOS:         brew install ffmpeg"
    echo "    Windows:       Download from https://ffmpeg.org/download.html"
fi

echo ""
echo "Setup complete! Happy coding! 🎉"
echo ""
