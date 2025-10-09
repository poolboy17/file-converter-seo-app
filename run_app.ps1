# File Converter SEO App Launcher (PowerShell)
# Right-click this file and select "Run with PowerShell"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " File Converter SEO App" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting Streamlit app..." -ForegroundColor Green
Write-Host "The app will open in your browser automatically." -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the app" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment and run Streamlit
& .\.venv\Scripts\Activate.ps1
streamlit run app.py

Read-Host "Press Enter to exit"
