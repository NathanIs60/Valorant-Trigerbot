@echo off
title Unified Trading Bot Manager
echo.
echo ===============================================
echo      UNIFIED TRADING BOT MANAGER
echo ===============================================
echo.
echo Starting Unified Trading Bot Application...
echo.
echo Available Trading Bots:
echo - Purple Trigger Bot (Standard detection)
echo - Green Trigger Bot (Buy signals)
echo - Red Trigger Bot (Sell signals)  
echo - Blue Trigger Bot (Neutral signals)
echo - Multi-Color Pattern Bot (Complex patterns)
echo.
echo Features:
echo - Easy bot selection and switching
echo - Real-time performance monitoring
echo - Emergency stop functionality
echo - Configuration management
echo - Activity logging
echo.
echo Starting application...
echo.

:: Start the Unified Trading Bot
start "Unified Trading Bot" "dist\UnifiedTradingBot.exe"

echo ✓ Unified Trading Bot launched successfully!
echo.
echo The application window should now be open.
echo You can close this command window.
echo.
echo To use the application:
echo 1. Select a trading bot from the dropdown or buttons
echo 2. Configure scan interval and action cooldown
echo 3. Click "START TRADING BOT" to begin
echo 4. Monitor performance in real-time
echo 5. Use "EMERGENCY STOP" if needed
echo.
pause