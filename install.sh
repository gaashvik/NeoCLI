#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"


if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment at $VENV_DIR"
    python3 -m venv "$VENV_DIR"
else
    echo "Virtual environment already exists at $VENV_DIR"
fi

# Install requirements.txt if it exists
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt"
    "$VENV_DIR/bin/pip" install --upgrade pip
    "$VENV_DIR/bin/pip" install -r requirements.txt
else
    echo "No requirements.txt found, skipping dependency installation."
fi

# Add source line to ~/.bashrc if not already present
BASHRC="$HOME/.bashrc"
NEO_FILE="$SCRIPT_DIR/shell-script/neocli.sh"
if ! grep -Fxq "source $NEO_FILE" "$BASHRC"; then
    echo "Adding source line to $BASHRC"
    echo "source $NEO_FILE" >> "$BASHRC"
fi

echo "Setup complete."
echo "Please run: source $BASHRC"
