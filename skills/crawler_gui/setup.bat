@echo off
chcp 65001 >nul
REM Windows Virtual Environment Setup Script for Playwright Web Crawler GUI Tool

echo ========================================
echo Playwright Web Crawler GUI Tool Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python 3.8 or higher first.
    pause
    exit /b 1
)

echo [1/5] Checking Python version...
python --version
echo.

REM Create virtual environment
echo [2/5] Creating virtual environment...
if exist .venv (
    echo Virtual environment already exists, skipping creation
) else (
    python -m venv .venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully
)
echo.

REM Activate virtual environment
echo [3/5] Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)
echo Virtual environment activated successfully
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install dependencies
echo [4/5] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)
echo.

REM Install Playwright browsers
echo [5/5] Installing Playwright browsers...
python -m playwright install
if errorlevel 1 (
    echo Error: Failed to install Playwright browsers
    pause
    exit /b 1
)
echo.

echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo Usage:
echo 1. Activate virtual environment: .venv\Scripts\activate.bat
echo 2. Run the program: python main.py
echo 3. Deactivate virtual environment: deactivate
echo.
pause
