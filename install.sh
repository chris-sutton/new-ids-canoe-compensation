#!/bin/bash

# Reusable script to set up a pseudo-virtual environment for Python projects

# Default Python version (can be overridden with an environment variable)
PYTHON_VERSION=${PYTHON_VERSION:-3.12}
PYTHON_EXEC="python${PYTHON_VERSION}"

# Check if the specified Python version is available
if ! command -v "$PYTHON_EXEC" &> /dev/null; then
    echo "Error: $PYTHON_EXEC is required but not found."
    exit 1
fi

# Set up pseudo-venv directory (default is 'venv', can be overridden)
PSEUDO_VENV_DIR=${PSEUDO_VENV_DIR:-venv}
echo "Setting up pseudo-virtual environment in $PSEUDO_VENV_DIR..."

# Clean up any existing pseudo-venv
if [ -d "$PSEUDO_VENV_DIR" ]; then
    rm -rf "$PSEUDO_VENV_DIR"
fi
mkdir -p "$PSEUDO_VENV_DIR/lib/python${PYTHON_VERSION}/site-packages"
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
"$PYTHON_EXEC" get-pip.py --target "$PSEUDO_VENV_DIR/lib/python${PYTHON_VERSION}/site-packages"
if [ $? -ne 0 ]; then
    echo "Error: Failed to install pip into $PSEUDO_VENV_DIR."
    exit 1
fi

# Define absolute path for clarity
ABSOLUTE_VENV_PATH="$PWD/$PSEUDO_VENV_DIR/lib/python${PYTHON_VERSION}/site-packages"

# Create a pip executable in the pseudo-venv bin directory
echo "Creating pip executable..."
cat <<EOL > "$PSEUDO_VENV_DIR/bin/pip3"
#!/bin/bash
export PYTHONPATH="$ABSOLUTE_VENV_PATH"
exec /usr/bin/$PYTHON_EXEC -m pip "\$@"
EOL
chmod +x "$PSEUDO_VENV_DIR/bin/pip3"

# Verify pip executable works
PIP_EXEC="$PSEUDO_VENV_DIR/bin/pip3"
echo "Debugging pip installation..."
echo "Pip executable location: $PIP_EXEC"
"$PIP_EXEC" --version
if [ $? -ne 0 ]; then
    echo "Error: Pip executable is not working."
    echo "Checking pip module in site-packages:"
    ls -l "$ABSOLUTE_VENV_PATH/pip"
    echo "Testing pip module import:"
    PYTHONPATH="$ABSOLUTE_VENV_PATH" /usr/bin/$PYTHON_EXEC -c "import pip; print('pip version:', pip.__version__)"
    exit 1
fi

# Install a compatible version of setuptools (optional, comment out if not needed)
echo "Installing setuptools for Python ${PYTHON_VERSION} compatibility..."
"$PIP_EXEC" install "setuptools>=69.0.0" --no-user --target "$PSEUDO_VENV_DIR/lib/python${PYTHON_VERSION}/site-packages"
if [ $? -ne 0 ]; then
    echo "Error: Failed to install setuptools."
    exit 1
fi

# Install dependencies from requirements.txt if it exists
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    "$PIP_EXEC" install -r requirements.txt --no-user --target "$PSEUDO_VENV_DIR/lib/python${PYTHON_VERSION}/site-packages"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies. Check requirements.txt or network access."
        exit 1
    fi
else
    echo "Warning: No requirements.txt found. Skipping dependency installation."
fi

# Verify installed packages
echo "Listing installed packages in $ABSOLUTE_VENV_PATH..."
ls -l "$ABSOLUTE_VENV_PATH"

# Create a python wrapper to use the pseudo-venv
echo "Creating python wrapper..."
cat <<EOL > "$PSEUDO_VENV_DIR/bin/python"
#!/bin/bash
export PYTHONPATH="$ABSOLUTE_VENV_PATH:\$PYTHONPATH"
exec /usr/bin/$PYTHON_EXEC "\$@"
EOL
chmod +x "$PSEUDO_VENV_DIR/bin/python"

# Test the python wrapper
echo "Testing python wrapper..."
"$PSEUDO_VENV_DIR/bin/python" -c "import sys; print('sys.path:', sys.path)"
"$PSEUDO_VENV_DIR/bin/python" -c "import pkg_resources; print('Installed packages:', [d.project_name for d in pkg_resources.working_set])"

# Optional: Test a main script (uncomment and adjust if needed)
# MAIN_SCRIPT="src/main.py"
# echo "Testing $MAIN_SCRIPT execution..."
# if [ -f "$MAIN_SCRIPT" ]; then
#     "$PSEUDO_VENV_DIR/bin/python" "$MAIN_SCRIPT"
#     if [ $? -ne 0 ]; then
#         echo "Error: $MAIN_SCRIPT failed to run. Please check the error above and ensure all required modules are in requirements.txt."
#     else
#         echo "$MAIN_SCRIPT ran successfully!"
#     fi
# else
#     echo "Warning: $MAIN_SCRIPT not found. Skipping test."
# fi

echo "Installation complete! To use the pseudo-venv, run:"
echo "  $PSEUDO_VENV_DIR/bin/python <your_script.py>"