@echo off
cd /d "%~dp0"
python main.py
if %errorlevel% neq 0 (
    echo.
    echo Failed to start! Please check if Python is installed.
    echo.
    pause
)