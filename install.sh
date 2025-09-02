#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"
ENV_FILE="$SCRIPT_DIR/backend/.env"
if [ ! -f "$ENV_FILE" ]; then
  touch "$ENV_FILE"
fi

update_env() {
  local KEY=$1
  local VALUE=$2
  if grep -q "^$KEY=" "$ENV_FILE"; then
    sed -i.bak "s|^$KEY=.*|$KEY=$VALUE|" "$ENV_FILE"
    echo "✅ Updated $KEY"
  else
    echo "$KEY=$VALUE" >> "$ENV_FILE"
    echo "✅ Added $KEY"
  fi
}


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

echo "🔑 API Key Setup"
read -s -p "Enter HuggingFace API Key: " HF_KEY
echo ""
read -s -p "Enter Gemini API Key: " GEMINI_KEY
echo ""
read -s -p "Enter GitHub App Token: " GH_APP_TOKEN
echo ""
read -s -p "Enter GitHub Installation Token: " GH_INSTALL_TOKEN
echo ""
read -p "Enter GitHub Private Key Path (e.g. /path/to/key.pem): " GH_PRIVATE_KEY_PATH
echo ""



update_env "HUGGING_FACE_API" "$HF_KEY"
update_env "GEMINI_API_KEY" "$GEMINI_KEY"
update_env "GIT_APP_ID" "$GH_APP_TOKEN"
update_env "GIT_INSTALL_ID" "$GH_INSTALL_TOKEN"
update_env "GIT_PRIVATE_KEY" "$GH_PRIVATE_KEY_PATH"



BASHRC="$HOME/.bashrc"
NEO_FILE="$SCRIPT_DIR/shell-script/neocli.sh"
if ! grep -Fxq "source $NEO_FILE" "$BASHRC"; then
    echo "Adding source line to $BASHRC"
    echo "source $NEO_FILE" >> "$BASHRC"
fi

echo "Setup complete."
echo "the change will be applied to the new terminal"
