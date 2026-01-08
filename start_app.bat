@echo off
setlocal

echo ================================
echo Agile Maturity App - Startup
echo ================================

REM Move to script directory
cd /d %~dp0

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found in PATH
    echo Please install Python 3.9+ and add to PATH
    pause
    exit /b 1
)

REM Create venv if missing
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate venv
call venv\Scripts\activate

REM Upgrade pip
python -m pip install --upgrade pip

REM Install dependencies
pip install -r requirements.txt

REM Run Streamlit (launcher-safe)
echo Starting Streamlit...
python -m streamlit run app.py

pause
