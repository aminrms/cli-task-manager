#!/bin/bash
# Cross-platform installer script for Linux/macOS

set -e

echo "🚀 Installing CLI Task Manager..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Python 3.8+ is installed
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        echo -e "${RED}❌ Python not found. Please install Python 3.8+${NC}"
        exit 1
    fi
    
    # Check Python version
    PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    if [ "$(echo "$PYTHON_VERSION < 3.8" | bc -l)" -eq 1 ]; then
        echo -e "${RED}❌ Python 3.8+ required. Found: $PYTHON_VERSION${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ Found Python $PYTHON_VERSION${NC}"
}

# Install system dependencies
install_dependencies() {
    echo -e "${BLUE}📦 Installing system dependencies...${NC}"
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get &> /dev/null; then
            # Debian/Ubuntu
            sudo apt-get update
            sudo apt-get install -y python3-pip python3-venv git
        elif command -v yum &> /dev/null; then
            # CentOS/RHEL
            sudo yum install -y python3-pip git
        elif command -v dnf &> /dev/null; then
            # Fedora
            sudo dnf install -y python3-pip git
        elif command -v pacman &> /dev/null; then
            # Arch Linux
            sudo pacman -S python-pip git
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if ! command -v brew &> /dev/null; then
            echo -e "${YELLOW}⚠️  Homebrew not found. Installing...${NC}"
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        brew install python git
    fi
}

# Create installation directory
create_install_dir() {
    INSTALL_DIR="$HOME/.local/share/cli-task-manager"
    BIN_DIR="$HOME/.local/bin"
    
    mkdir -p "$INSTALL_DIR"
    mkdir -p "$BIN_DIR"
    
    echo -e "${GREEN}✓ Created installation directory: $INSTALL_DIR${NC}"
}

# Download and install
install_app() {
    echo -e "${BLUE}📥 Downloading CLI Task Manager...${NC}"
    
    cd "$INSTALL_DIR"
    
    # Clone repository
    if [ -d ".git" ]; then
        git pull
    else
        git clone https://github.com/yourusername/cli-task-manager.git .
    fi
    
    # Create virtual environment
    echo -e "${BLUE}🐍 Setting up Python environment...${NC}"
    $PYTHON_CMD -m venv venv
    source venv/bin/activate
    
    # Install dependencies
    pip install --upgrade pip
    pip install -r requirements.txt
    
    echo -e "${GREEN}✓ Installed Python dependencies${NC}"
}

# Create executable script
create_executable() {
    SCRIPT_PATH="$BIN_DIR/mytasks"
    
    cat > "$SCRIPT_PATH" << EOF
#!/bin/bash
# CLI Task Manager executable script
cd "$INSTALL_DIR"
source venv/bin/activate
python main.py "\$@"
EOF
    
    chmod +x "$SCRIPT_PATH"
    echo -e "${GREEN}✓ Created executable: $SCRIPT_PATH${NC}"
}

# Update PATH
update_path() {
    # Check if ~/.local/bin is in PATH
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        echo -e "${YELLOW}⚠️  Adding ~/.local/bin to PATH${NC}"
        
        # Add to shell profile
        SHELL_NAME=$(basename "$SHELL")
        case $SHELL_NAME in
            bash)
                PROFILE_FILE="$HOME/.bashrc"
                ;;
            zsh)
                PROFILE_FILE="$HOME/.zshrc"
                ;;
            fish)
                PROFILE_FILE="$HOME/.config/fish/config.fish"
                echo 'set -gx PATH $PATH $HOME/.local/bin' >> "$PROFILE_FILE"
                echo -e "${GREEN}✓ Added to PATH in $PROFILE_FILE${NC}"
                return
                ;;
            *)
                PROFILE_FILE="$HOME/.profile"
                ;;
        esac
        
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$PROFILE_FILE"
        echo -e "${GREEN}✓ Added to PATH in $PROFILE_FILE${NC}"
        echo -e "${YELLOW}📝 Please restart your terminal or run: source $PROFILE_FILE${NC}"
    else
        echo -e "${GREEN}✓ ~/.local/bin is already in PATH${NC}"
    fi
}

# Test installation
test_installation() {
    echo -e "${BLUE}🧪 Testing installation...${NC}"
    
    if [ -x "$BIN_DIR/mytasks" ]; then
        echo -e "${GREEN}✓ Installation successful!${NC}"
        echo ""
        echo -e "${BLUE}🚀 You can now run: ${YELLOW}mytasks${NC}"
        echo ""
    else
        echo -e "${RED}❌ Installation failed${NC}"
        exit 1
    fi
}

# Main installation process
main() {
    echo "==============================================="
    echo "🚀 CLI Task Manager Installer"
    echo "==============================================="
    echo ""
    
    check_python
    install_dependencies
    create_install_dir
    install_app
    create_executable
    update_path
    test_installation
    
    echo ""
    echo "==============================================="
    echo -e "${GREEN}✅ Installation Complete!${NC}"
    echo "==============================================="
    echo ""
    echo -e "Run ${YELLOW}mytasks${NC} to start the application"
    echo ""
}

# Run main function
main "$@"
