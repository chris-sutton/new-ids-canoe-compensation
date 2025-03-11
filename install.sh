#!/bin/bash

# Script to install the CANOE Compensation Pipeline in a pseudo-virtual environment

# Check if Python 3.12 is available
if ! command -v python3.12 &> /dev/null; then
    echo "Error: Python 3.12 is required but not found."
    exit 1
fi

# Set up pseudo-venv directory
PSEUDO_VENV_DIR="venv"
echo "Setting up pseudo-virtual environment in $PSEUDO_VENV_DIR..."

# Clean up any existing pseudo-venv
if [ -d "$PSEUDO_VENV_DIR" ]; then
    rm -rf "$PSEUDO_VENV_DIR"
fi
mkdir -p "$PSEUDO_VENV_DIR/lib/python3.12/site-packages"
mkdir -p "$PSEUDO_VENV_DIR/bin"

# Download get-pip.py if not present
if [ ! -f "get-pip.py" ]; then
    echo "Attempting to download get-pip.py..."
    if ! curl -sSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py 2>/dev/null; then
        echo "Error: Could not download get-pip.py due to network restrictions."
        echo "Please download https://bootstrap.pypa.io/get-pip.py manually and place it in this directory."
        exit 1
    fi
fi

# Install pip into the pseudo-venv's site-packages
echo "Installing pip locally..."
PYTHONPATH="$PWD/$PSEUDO_VENV_DIR/lib/python3.12/site-packages" python3.12 get-pip.py --target "$PSEUDO_VENV_DIR/lib/python3.12/site-packages"
if [ $? -ne 0 ]; then
    echo "Error: Failed to install pip into $PSEUDO_VENV_DIR."
    exit 1
fi

# Install dependencies into the pseudo-venv using python -m pip
echo "Installing dependencies from requirements.txt..."
PYTHONPATH="$PWD/$PSEUDO_VENV_DIR/lib/python3.12/site-packages" python3.12 -I -s -m pip install -r requirements.txt --no-user --target "$PSEUDO_VENV_DIR/lib/python3.12/site-packages"
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies. Check requirements.txt or network access."
    exit 1
fi

# Create a simple python wrapper to use the pseudo-venv
cat <<EOL > "$PSEUDO_VENV_DIR/bin/python"
#!/bin/bash
export PYTHONPATH="\$PYTHONPATH:$PWD/$PSEUDO_VENV_DIR/lib/python3.12/site-packages"
exec /usr/bin/python3.12 -I -s "\$@"
EOL
chmod +x "$PSEUDO_VENV_DIR/bin/python"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Creating a template..."
    cat <<EOL > .env
C2G_TOKEN=your_c2g_token
CVU_TOKEN=your_cvu_token
COMPENSATION_TOKEN=your_compensation_token
ERROR_TOKEN=your_error_token
API_URL=https://redcap.your-institution.org/api/
EOL
    echo "Please edit .env with your REDCap tokens and API URL."
else
    echo ".env file found. Skipping template creation."
fi

echo "Installation complete! To test, run:"
echo "  $PSEUDO_VENV_DIR/bin/python src/main.py"
echo "See README.md for cronjob setup."