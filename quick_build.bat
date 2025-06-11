@echo off
title Visual Detection GUI - Quick Build
echo.
echo Visual Detection GUI - Quick Build
echo ===================================
echo.
echo This script will:
echo 1. Install required packages
echo 2. Build standalone .exe file
echo 3. Test the application
echo.
pause

echo.
echo Step 1: Installing requirements...
echo --------------------------------
py install_requirements.py
if %errorlevel% neq 0 (
    echo Error: Requirements installation failed!
    pause
    exit /b 1
)

echo.
echo Step 2: Building executable...
echo ------------------------------
py build_exe.py
if %errorlevel% neq 0 (
    echo Error: Build failed!
    pause
    exit /b 1
)

echo.
echo Step 3: Build completed successfully!
echo =====================================
echo.
echo Files created:
echo - dist/VisualDetector.exe (standalone executable)
echo - build/ (temporary files - can be deleted)
echo.
echo The .exe file can be distributed without Python installation.
echo.
set /p choice="Would you like to test the .exe now? (y/n): "
if /i "%choice%"=="y" (
    echo.
    echo Testing executable...
    start "" "dist\VisualDetector.exe"
    echo ✓ Executable launched!
)

echo.
echo Build process completed!
pause

