param()

Write-Host "Setting up project virtual environment (.venv) and installing dependencies..."

if (-not (Test-Path -Path ".venv")) {
    python -m venv .venv
    Write-Host "Created virtual environment at ./.venv"
} else {
    Write-Host ".venv already exists - skipping venv creation"
}

Write-Host "Activating virtual environment and installing dependencies..."
& .\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
if (Test-Path -Path "requirements.txt") {
    pip install -r requirements.txt
} else {
    Write-Host "requirements.txt not found; ensure dependencies are installed manually or via pyproject.toml"
}

Write-Host "Setup complete. To run the app in this session:"
Write-Host "  1) Ensure the venv is activated: .\\.venv\\Scripts\\Activate.ps1"
Write-Host "  2) Run: streamlit run app.py --server.port 5000"
