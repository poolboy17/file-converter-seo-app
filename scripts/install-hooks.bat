@echo off
REM Install git hooks for the project (Windows version)
REM This script sets up pre-commit and pre-push hooks

echo.
echo 🔧 Setting up git hooks for the project...
echo.

REM Check if we're in a git repository
if not exist .git (
    echo ❌ Not a git repository
    exit /b 1
)

REM Install pre-commit framework
echo 📦 Installing pre-commit framework...
pip install pre-commit --quiet

REM Install pre-commit hooks
echo 🎣 Installing pre-commit hooks...
pre-commit install --install-hooks

REM Install pre-push hooks specifically
echo 🎣 Installing pre-push hooks...
pre-commit install --hook-type pre-push

REM Run pre-commit on all files to verify setup
echo.
echo 🧪 Testing hooks on existing files...
pre-commit run --all-files

echo.
echo ✅ Git hooks successfully installed!
echo.
echo Installed hooks:
echo   • pre-commit: Runs linters and formatters on staged files
echo   • pre-push: Runs test suite before pushing
echo.
echo What happens now:
echo   • On git commit: Code formatting, linting, and security checks
echo   • On git push: Full test suite must pass (52%% coverage required)
echo.
echo To bypass hooks (not recommended):
echo   • git commit --no-verify
echo   • git push --no-verify
echo.
echo Happy coding! 🚀
