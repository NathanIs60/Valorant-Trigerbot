@echo off
title Visual Detection Control Panel
echo.
echo ==============================================
echo      VISUAL DETECTION CONTROL PANEL
echo ==============================================
echo.
echo Starting Visual Detector GUI...
echo.
echo Features:
echo - Real-time color detection
echo - 9 central pixel monitoring  
echo - Purple detection (60%% tolerance)
echo - Interactive color picker
echo - Adjustable parameters
echo - Live statistics
echo.
echo Controls:
echo - START/STOP button to toggle detection
echo - Color picker to choose target color
echo - Tolerance slider (0-100%%)
echo - Save/Load configuration
echo.
echo Starting application...
echo.

:: Start the Visual Detector
start "Visual Detector" "dist\VisualDetector.exe"

echo ✓ Visual Detector launched successfully!
echo.
echo The GUI window should now be open.
echo You can close this command window.
echo.
echo To use the application:
echo 1. Click "START DETECTION" to begin monitoring
echo 2. Use "Choose Color" to select target color
echo 3. Adjust tolerance with the slider
echo 4. Monitor the activity log for detections
echo.
pause

