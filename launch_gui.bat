@echo off
title Visual Detection Control Panel
echo.
echo Visual Detection Control Panel
echo ===============================
echo.
echo Starting GUI application...
echo.

:: Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found in PATH, trying 'py' command...
    py --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo Error: Python not found!
        echo Please install Python or add it to your PATH.
        pause
        exit /b 1
    )
    py visual_detector_gui.py
) else (
    python visual_detector_gui.py
)

echo.
echo GUI application closed.
echo.
pause

