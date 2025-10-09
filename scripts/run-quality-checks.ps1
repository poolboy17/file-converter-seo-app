#!/usr/bin/env pwsh
# Run all quality checks locally before committing

Write-Host "🔍 Running Code Quality Checks..." -ForegroundColor Cyan
Write-Host ""

$ErrorCount = 0

# Activate virtual environment
Write-Host "📦 Activating virtual environment..." -ForegroundColor Yellow
& .venv\Scripts\Activate.ps1

# 1. Black formatting check
Write-Host ""
Write-Host "🎨 Checking code formatting with Black..." -ForegroundColor Yellow
& python -m black --check --diff . 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Black formatting issues found. Run: black ." -ForegroundColor Red
    $ErrorCount++
} else {
    Write-Host "✅ Black formatting OK" -ForegroundColor Green
}

# 2. isort import sorting check
Write-Host ""
Write-Host "📋 Checking import sorting with isort..." -ForegroundColor Yellow
& python -m isort --check-only --diff . 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Import sorting issues found. Run: isort ." -ForegroundColor Red
    $ErrorCount++
} else {
    Write-Host "✅ Import sorting OK" -ForegroundColor Green
}

# 3. Pyright type checking
Write-Host ""
Write-Host "🔬 Running Pyright type checker..." -ForegroundColor Yellow
& python -m pyright 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Pyright found type issues (see above)" -ForegroundColor Yellow
    # Don't increment error count - type issues are warnings
} else {
    Write-Host "✅ Pyright type checking passed" -ForegroundColor Green
}

# 4. MyPy type checking (alternative)
Write-Host ""
Write-Host "🔍 Running MyPy type checker..." -ForegroundColor Yellow
& python -m mypy --install-types --non-interactive --ignore-missing-imports converters/ utils/ app.py 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  MyPy found type issues (see above)" -ForegroundColor Yellow
    # Don't increment error count - type issues are warnings
} else {
    Write-Host "✅ MyPy type checking passed" -ForegroundColor Green
}

# 5. Syntax check
Write-Host ""
Write-Host "🐍 Checking Python syntax..." -ForegroundColor Yellow
$SyntaxOK = $true
Get-ChildItem -Path . -Filter *.py -Recurse -Exclude .venv,__pycache__ | ForEach-Object {
    & python -m py_compile $_.FullName 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Syntax error in: $($_.Name)" -ForegroundColor Red
        $SyntaxOK = $false
        $ErrorCount++
    }
}
if ($SyntaxOK) {
    Write-Host "✅ Python syntax OK" -ForegroundColor Green
}

# 6. Import check
Write-Host ""
Write-Host "📦 Verifying imports..." -ForegroundColor Yellow
$ImportsOK = $true

& python -c "import app; print('✅ app.py imports successfully')" 2>&1
if ($LASTEXITCODE -ne 0) { $ImportsOK = $false; $ErrorCount++ }

& python -c "from converters.csv_converter import CsvConverter; print('✅ CsvConverter imports successfully')" 2>&1
if ($LASTEXITCODE -ne 0) { $ImportsOK = $false; $ErrorCount++ }

& python -c "from converters.docx_converter import DocxConverter; print('✅ DocxConverter imports successfully')" 2>&1
if ($LASTEXITCODE -ne 0) { $ImportsOK = $false; $ErrorCount++ }

& python -c "from utils.html_generator import HtmlGenerator; print('✅ HtmlGenerator imports successfully')" 2>&1
if ($LASTEXITCODE -ne 0) { $ImportsOK = $false; $ErrorCount++ }

if ($ImportsOK) {
    Write-Host "✅ All imports verified" -ForegroundColor Green
}

# 7. Security check with Bandit (if installed)
Write-Host ""
Write-Host "🔒 Running security checks with Bandit..." -ForegroundColor Yellow
try {
    & python -m bandit -r converters/ utils/ app.py -f json -o bandit-report.json 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ No security issues found" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Security issues found (see bandit-report.json)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "ℹ️  Bandit not installed (optional)" -ForegroundColor Gray
}

# Summary
Write-Host ""
Write-Host "═══════════════════════════════════════" -ForegroundColor Cyan
if ($ErrorCount -eq 0) {
    Write-Host "✅ All checks passed! Ready to commit." -ForegroundColor Green
    exit 0
} else {
    Write-Host "❌ $ErrorCount check(s) failed. Please fix before committing." -ForegroundColor Red
    exit 1
}
