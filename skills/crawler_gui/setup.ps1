# PowerShell Virtual Environment Setup Script for Playwright Web Crawler GUI Tool

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Playwright Web Crawler GUI Tool Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "[1/5] Checking Python version..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host $pythonVersion -ForegroundColor Green
} catch {
    Write-Host "Error: Python not found. Please install Python 3.8 or higher first." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# Create virtual environment
Write-Host "[2/5] Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "Virtual environment already exists, skipping creation" -ForegroundColor Green
} else {
    try {
        python -m venv .venv
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Virtual environment created successfully" -ForegroundColor Green
        } else {
            Write-Host "Error: Failed to create virtual environment" -ForegroundColor Red
            Read-Host "Press Enter to exit"
            exit 1
        }
    } catch {
        Write-Host "Error: Failed to create virtual environment - $_" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}
Write-Host ""

# Activate virtual environment
Write-Host "[3/5] Activating virtual environment..." -ForegroundColor Yellow
try {
    & ".venv\Scripts\Activate.ps1"
    Write-Host "Virtual environment activated successfully" -ForegroundColor Green
} catch {
    Write-Host "Error: Failed to activate virtual environment - $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
try {
    python -m pip install --upgrade pip --quiet
    Write-Host "Pip upgraded successfully" -ForegroundColor Green
} catch {
    Write-Host "Warning: Failed to upgrade pip - $_" -ForegroundColor Yellow
}
Write-Host ""

# Install dependencies
Write-Host "[4/5] Installing dependencies..." -ForegroundColor Yellow
try {
    pip install -r requirements.txt
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Dependencies installed successfully" -ForegroundColor Green
    } else {
        Write-Host "Error: Failed to install dependencies" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
} catch {
    Write-Host "Error: Failed to install dependencies - $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# Install Playwright browsers
Write-Host "[5/5] Installing Playwright browsers..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Cyan
try {
    python -m playwright install
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Playwright browsers installed successfully" -ForegroundColor Green
    } else {
        Write-Host "Error: Failed to install Playwright browsers" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
} catch {
    Write-Host "Error: Failed to install Playwright browsers - $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup completed successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Usage:" -ForegroundColor Yellow
Write-Host "1. Activate virtual environment: .venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "2. Run program: python main.py" -ForegroundColor White
Write-Host "3. Deactivate virtual environment: deactivate" -ForegroundColor White
Write-Host ""

Read-Host "Press Enter to exit"
