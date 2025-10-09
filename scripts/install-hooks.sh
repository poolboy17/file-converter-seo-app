#!/bin/bash
# Install git hooks for the project
# This script sets up pre-commit and pre-push hooks

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔧 Setting up git hooks for the project...${NC}"
echo ""

# Get the root directory of the git repository
ROOT_DIR=$(git rev-parse --show-toplevel)
cd "$ROOT_DIR"

# Check if we're in a git repository
if [ ! -d .git ]; then
    echo -e "${RED}❌ Not a git repository${NC}"
    exit 1
fi

# Install pre-commit framework
echo -e "${YELLOW}📦 Installing pre-commit framework...${NC}"
pip install pre-commit --quiet

# Install pre-commit hooks
echo -e "${YELLOW}🎣 Installing pre-commit hooks...${NC}"
pre-commit install --install-hooks

# Install pre-push hooks specifically
echo -e "${YELLOW}🎣 Installing pre-push hooks...${NC}"
pre-commit install --hook-type pre-push

# Make sure the pre-push hook is executable
if [ -f .git/hooks/pre-push ]; then
    chmod +x .git/hooks/pre-push
    echo -e "${GREEN}✅ Pre-push hook installed and made executable${NC}"
fi

# Run pre-commit on all files to verify setup
echo ""
echo -e "${YELLOW}🧪 Testing hooks on existing files...${NC}"
pre-commit run --all-files || true

echo ""
echo -e "${GREEN}✅ Git hooks successfully installed!${NC}"
echo ""
echo -e "${BLUE}Installed hooks:${NC}"
echo "  • pre-commit: Runs linters and formatters on staged files"
echo "  • pre-push: Runs test suite before pushing"
echo ""
echo -e "${BLUE}What happens now:${NC}"
echo "  • On ${YELLOW}git commit${NC}: Code formatting, linting, and security checks"
echo "  • On ${YELLOW}git push${NC}: Full test suite must pass (52% coverage required)"
echo ""
echo -e "${BLUE}To bypass hooks (not recommended):${NC}"
echo "  • git commit --no-verify"
echo "  • git push --no-verify"
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}"
