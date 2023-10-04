#!/bin/bash

# Check if the operating system is Windows or macOS
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows
    VENV_DIR="myenv/Scripts/activate"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    VENV_DIR="myenv/bin/activate"
else
    echo "Unsupported operating system."
    exit 1
fi

# Activate the virtual environment
source "$VENV_DIR"

# Run the streamlit command
streamlit run main.py
