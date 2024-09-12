#!/bin/bash
echo "Checking Fedora version:"
cat /etc/fedora-release

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Python 3 is installed
if ! command_exists python3; then
    echo "Python 3 is not installed. Installing it now..."
    sudo dnf install -y python3
else
    echo "Python 3 is already installed."
fi

# Check if pip is installed (to install Python packages)
if ! command_exists pip3; then
    echo "pip is not installed. Installing it now..."
    sudo dnf install -y python3-pip
else
    echo "pip is already installed."
fi

# Check if urwid is installed
if ! python3 -c "import urwid" &> /dev/null; then
    echo "The urwid library is not installed. Installing it now..."
    pip3 install urwid
    
else
    echo "The urwid library is already installed."
fi

# check if psutil is installed
if ! python3 -c "import psutil" &> /dev/null; then
    echo "The psutil library is not installed. Installing it now..."
    pip3 install psutil
else
    echo "The psutil library is already installed."
fi

# check if requests is installed
if ! python3 -c "import requests" &> /dev/null; then
    echo "The requests library is not installed. Installing it now..."
    pip3 install requests
else
    echo "The requests library is already installed."
fi

# Run the Python script
echo "Running the Python script..."
python3 menu_tui.py
