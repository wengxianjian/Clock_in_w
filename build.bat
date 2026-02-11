@echo off
echo ========================================
echo Clock-in App Build Script
echo ========================================
echo.

echo [1/5] Checking PyInstaller...
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller not found, installing...
    pip install pyinstaller
)
echo.

echo [2/5] Checking Pillow...
pip show pillow >nul 2>&1
if %errorlevel% neq 0 (
    echo Pillow not found, installing...
    pip install pillow
)
echo.

echo [3/5] Cleaning old files...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del /q "*.spec"
echo Clean complete
echo.

echo [4/5] Building...
pyinstaller --onefile --windowed --icon=clock_in_icon.png --name="ClockIn" main.py
if %errorlevel% neq 0 (
    echo Build failed!
    pause
    exit /b 1
)
echo.

echo [5/5] Build complete!
echo.
echo ========================================
echo Result:
echo Executable: dist\ClockIn.exe
echo.
echo Press any key to open dist folder...
pause >nul
explorer dist
