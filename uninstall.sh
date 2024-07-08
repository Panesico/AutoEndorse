#!/bin/bash

# Function to remove pyenv and clean up on Debian/Ubuntu
uninstall_pyenv_debian() {
    echo "Removing pyenv and cleaning up on Debian/Ubuntu..."
    sudo apt-get autoremove -y
    sudo apt-get clean
}

# Function to remove pyenv and clean up on Arch Linux
uninstall_pyenv_arch() {
    echo "Removing pyenv and cleaning up on Arch Linux..."
}

# Function to remove pyenv
uninstall_pyenv() {
    echo "Removing pyenv..."
    rm -rf "$HOME/.pyenv"
    sed -i '/pyenv/d' ~/.bashrc
    sed -i '/pyenv/d' ~/.zshrc
}

# Detect the Linux distribution
if [ -f /etc/os-release ]; then
    . /etc/os-release
    case "$ID" in
        ubuntu|debian)
            if command -v pyenv &> /dev/null; then
                uninstall_pyenv
                uninstall_pyenv_debian
            else
                echo "pyenv is not installed on Debian/Ubuntu."
            fi
            ;;
        arch)
            if command -v pyenv &> /dev/null; then
                uninstall_pyenv
                uninstall_pyenv_arch
            else
                echo "pyenv is not installed on Arch Linux."
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

# Deactivate and remove the virtual environment
if pyenv virtualenvs | grep -q "venv"; then
    echo "Deactivating and removing virtual environment..."
    pyenv deactivate
    pyenv uninstall -f venv
else
    echo "Virtual environment 'venv' not found."
fi

# Remove the local Python version
if pyenv versions | grep -q "3.11.8"; then
    echo "Removing Python 3.11.8..."
    pyenv uninstall -f 3.11.8
else
    echo "Python 3.11.8 not found."
fi

echo "Uninstallation complete."
