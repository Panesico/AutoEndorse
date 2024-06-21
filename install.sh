#!/bin/bash

# Function to install Python on Debian/Ubuntu
install_python_debian() {
    echo "Installing Python on Debian/Ubuntu..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-venv python3-pip
}

# Function to install Python on Arch Linux
install_python_arch() {
    echo "Installing Python on Arch Linux..."
    sudo pacman -Sy --needed --noconfirm python python-virtualenv python-pip
}

# Detect the Linux distribution
if [ -f /etc/os-release ]; then
    . /etc/os-release
    case "$ID" in
        ubuntu|debian)
            if ! command -v python3 &> /dev/null; then
                install_python_debian
            else
                echo "Python is already installed on Debian/Ubuntu."
            fi
            ;;
        arch)
            if ! command -v python3 &> /dev/null; then
                install_python_arch
            else
                echo "Python is already installed on Arch Linux."
            fi
            ;;
        *)
            echo "Unsupported Linux distribution."
            exit 1
            ;;
    esac
else
    echo "Cannot detect the Linux distribution."
    exit 1
fi

# Create a virtual environment in the current directory
echo "Creating virtual environment..."
python3 -m venv venv

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install the packages from requirements.txt if it exists
if [ -f "requirements.txt" ]; then
    echo "Installing packages from requirements.txt..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Skipping package installation."
fi

echo "Setup complete. Virtual environment 'venv' is activated."
exec "$SHELL"