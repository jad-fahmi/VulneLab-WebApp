@echo off
echo Starting VulnLab...
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please download and install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit
)

cd /d "%~dp0"

if not exist venv (
    echo Virtual environment not found.
    echo Please run install.bat first.
    pause
    exit
)

call venv\Scripts\activate

echo Launching VulnLab...
echo.
echo Opening browser at http://127.0.0.1:5000
echo.

start "" "http://127.0.0.1:5000"

python app.py
pause