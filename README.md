# Experimental Purple Triggerbot System

## Overview
This is an experimental triggerbot system designed to analyze the 9 central pixels of the screen in real-time and trigger automated left-click actions when purple-like colors are detected within a 60% tolerance range.

## Features
- **Real-time Analysis**: Continuously monitors 9 central pixels (3x3 grid)
- **Color Detection**: Detects purple hues with 60% tolerance using advanced color similarity algorithms
- **Low CPU Usage**: Optimized for minimal resource consumption
- **Background Execution**: Runs seamlessly in the background
- **Performance Monitoring**: Real-time statistics and logging
- **Windows API Integration**: Uses native Windows GDI for fast pixel reading

## Technical Specifications
- **Scan Interval**: 1ms for maximum responsiveness
- **Click Cooldown**: 50ms to prevent spam
- **Color Space**: RGB with Euclidean distance calculation
- **Target Color**: RGB(128, 0, 128) - Standard purple
- **Tolerance**: 60% similarity threshold

## Usage
1. Run the script: `python experimental_triggerbot.py`
2. Press 'E' to enable/disable the triggerbot
3. Press 'Q' to quit the application

## Files
- `experimental_triggerbot.py` - Main triggerbot implementation
- `config.json` - Configuration settings
- `experimental_triggerbot_log.txt` - Runtime logs and statistics

## Performance Metrics
The system tracks:
- Scan times (average response time)
- Detection rate (detections per second)
- Click count (total automated clicks)
- Runtime statistics

## Requirements
- Windows OS
- Python 3.6+
- numpy
- Access to Windows API (ctypes)

## Disclaimer
This is an experimental proof-of-concept for color-based automation research. Use responsibly and in accordance with applicable terms of service and regulations.

## Safety Features
- Click cooldown to prevent excessive automation
- Manual toggle control
- Comprehensive logging for analysis
- Graceful shutdown handling

