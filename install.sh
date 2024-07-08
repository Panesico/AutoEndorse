#!/bin/bash

# Function to install dependencies and pyenv on Debian/Ubuntu
install_pyenv_debian() {
    echo "Installing dependencies and pyenv on Debian/Ubuntu..."
    sudo apt-get update
    sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python-openssl git

    echo "Installing Google Chrome..."
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    sudo dpkg -i google-chrome-stable_current_amd64.deb
    sudo apt-get install -f -y
}

# Function to install dependencies and pyenv on Arch Linux
install_pyenv_arch() {
    echo "Installing dependencies and pyenv on Arch Linux..."
    sudo pacman -Sy --needed --noconfirm base-devel openssl zlib xz git

    echo "Installing Google Chrome..."
    yay -S --noconfirm google-chrome
}

# Function to install pyenv
install_pyenv() {
    echo "Installing pyenv..."
    curl https://pyenv.run | bash
    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init --path)"
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"
    echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
    echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
    echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.zshrc
    echo 'eval "$(pyenv init --path)"' >> ~/.zshrc
    echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zshrc
}

# Detect the Linux distribution
if [ -f /etc/os-release ]; then
    . /etc/os-release
    case "$ID" in
        ubuntu|debian)
            if ! command -v pyenv &> /dev/null; then
                install_pyenv_debian
                install_pyenv
            else
                echo "pyenv is already installed on Debian/Ubuntu."
            fi
            ;;
        arch)
            if ! command -v pyenv &> /dev/null; then
                install_pyenv_arch
                install_pyenv
            else
                echo "pyenv is already installed on Arch Linux."
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

# Install Python 3.11.8 using pyenv
echo "Installing Python 3.11.8..."
pyenv install 3.11.8
pyenv local 3.11.8

# Create a virtual environment in the current directory
echo "Creating virtual environment with Python 3.11.8..."
pyenv virtualenv 3.11.8 venv
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"

# Activate the virtual environment
echo "Activating virtual environment..."
pyenv activate venv

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
