@echo off
REM File Converter SEO App Launcher
REM Double-click this file to run the app

echo.
echo ========================================
echo  File Converter SEO App
echo ========================================
echo.
echo Starting Streamlit app...
echo The app will open in your browser automatically.
echo.
echo Press Ctrl+C to stop the app
echo ========================================
echo.

REM Activate virtual environment and run Streamlit
call .venv\Scripts\activate.bat
streamlit run app.py

pause
