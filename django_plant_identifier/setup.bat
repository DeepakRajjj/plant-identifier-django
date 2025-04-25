@echo off
echo Django Plant Identifier - Setup Script
echo =====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH. Please install Python 3.8 or higher.
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
) else (
    echo Virtual environment already exists.
)

REM Activate virtual environment and install dependencies
echo Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt

REM Set up database
echo Setting up database...
python manage.py migrate

REM Create media directories
echo Creating media directories...
if not exist media\plants mkdir media\plants

echo.
echo Setup completed successfully!
echo.
echo To run the server:
echo python manage.py runserver
echo.
echo Access the application at: http://127.0.0.1:8000/
echo.
echo Press any key to exit...
pause >nul
