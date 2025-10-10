@echo off
REM ==================================================================
REM  File Converter SEO App - Desktop Launcher
REM ==================================================================
REM  This script launches the File Converter SEO App
REM
REM  Usage: Double-click this file from anywhere
REM ==================================================================

echo.
echo ===============================================
echo   File Converter SEO App
echo ===============================================
echo.
echo Starting application...
echo.

REM Get the directory where this script is located
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run this script from the app directory.
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Check if Streamlit is installed
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo ERROR: Streamlit not found!
    echo Installing dependencies...
    python -m pip install -r requirements-prod.txt
    echo.
)

REM Start the app
echo.
echo ===============================================
echo  App is starting...
echo  Your browser will open automatically.
echo.
echo  Local URL: http://localhost:8501
echo.
echo  Press Ctrl+C to stop the app
echo  Or close this window to exit
echo ===============================================
echo.

REM Start Streamlit in background and open browser
start /B streamlit run app.py --server.headless=false

REM Wait 3 seconds for server to start
timeout /t 3 /nobreak >nul

REM Open browser
start http://localhost:8501

REM Keep the window open and wait for Streamlit
echo.
echo Browser opened. Keep this window open while using the app.
echo Press Ctrl+C to stop the app.
echo.

REM Wait indefinitely (Streamlit is running in background)
:WAIT
timeout /t 60 /nobreak >nul
goto WAIT

REM If app exits, pause so user can see any error messages
if errorlevel 1 (
    echo.
    echo ===============================================
    echo  App stopped with an error
    echo ===============================================
    echo.
    pause
)
