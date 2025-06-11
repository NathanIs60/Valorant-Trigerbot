# Visual Detection Control Panel

## Overview
A lightweight desktop application with a graphical user interface (GUI) for controlling visual detection parameters. The application monitors 9 central pixels of the screen and responds to user-defined color thresholds with adjustable tolerance settings.

## Features

### Real-time Control
- **Live Status Display**: Visual indicators showing detection active/inactive state
- **Instant Start/Stop**: Toggle detection with a single button click
- **Real-time Statistics**: Live updates of detections, clicks, and performance metrics

### Color Configuration
- **Color Picker**: Interactive color selection dialog
- **Tolerance Slider**: Adjustable similarity threshold (0-100%)
- **Live Preview**: Real-time color display with RGB values
- **60% Purple Detection**: Pre-configured for purple color detection

### Detection Parameters
- **Scan Interval**: Adjustable scanning frequency (0.1-100ms)
- **Click Cooldown**: Configurable delay between automated clicks (10-1000ms)
- **9-Pixel Monitoring**: Monitors 3x3 grid of central screen pixels

### Performance Optimization
- **Low CPU Usage**: Optimized scanning algorithms
- **Background Operation**: Runs seamlessly in background
- **Efficient Memory Management**: Circular buffers for statistics
- **Native Windows API**: Direct pixel access for maximum speed

### User Interface
- **Intuitive Design**: Clean, organized layout with labeled sections
- **Activity Log**: Real-time logging of all detection events
- **Statistics Panel**: Performance metrics and operation counters
- **Configuration Management**: Save/load settings to file

## Installation & Usage

### Method 1: Standalone Executable
1. Download `VisualDetector.exe`
2. Double-click to run
3. No installation required!

### Method 2: Python Source
1. Install requirements: `pip install -r requirements_gui.txt`
2. Run: `python visual_detector_gui.py`

### Method 3: Build Your Own
1. Run the build script: `python build_exe.py`
2. Find the executable in `dist/VisualDetector.exe`

## Controls

### Main Controls
- **START/STOP DETECTION**: Toggle the monitoring system
- **Choose Color**: Open color picker to select target color
- **Tolerance Slider**: Adjust color similarity threshold
- **Save/Load Config**: Persist settings between sessions
- **Reset Stats**: Clear all statistics counters

### Status Indicators
- **Green Circle**: Detection is active
- **Red Circle**: Detection is inactive
- **Activity Log**: Real-time event logging
- **Statistics Panel**: Live performance metrics

## Configuration

### Color Settings
- **Target Color**: RGB color to detect (default: purple 128,0,128)
- **Tolerance**: Similarity threshold 0-100% (default: 60%)

### Performance Settings
- **Scan Interval**: Time between scans in milliseconds (default: 1ms)
- **Click Cooldown**: Minimum time between clicks (default: 50ms)

### Monitoring Area
- **Region**: 9 central pixels in 3x3 grid
- **Location**: Automatically calculated screen center
- **Coverage**: 3x3 pixel area around center point

## Technical Specifications

### System Requirements
- **Operating System**: Windows 7/8/10/11
- **RAM**: 50MB minimum
- **CPU**: Any modern processor
- **Permissions**: Standard user (no admin required)

### Performance Characteristics
- **Scan Speed**: <10ms average per scan
- **CPU Usage**: <1% on modern systems
- **Memory Usage**: <50MB RAM
- **Response Time**: <1ms detection latency

### Detection Algorithm
- **Color Space**: RGB with Euclidean distance
- **Similarity**: Mathematical color distance calculation
- **Tolerance**: Percentage-based threshold system
- **Precision**: Sub-millisecond timing accuracy

## Building from Source

### Prerequisites
```bash
pip install numpy pyinstaller pillow
```

### Build Process
```bash
python build_exe.py
```

### Build Output
- `dist/VisualDetector.exe` - Standalone executable
- `build/` - Temporary build files (can be deleted)
- `VisualDetector.spec` - PyInstaller configuration

## Configuration Files

### detector_config.json
```json
{
  "target_color": [128, 0, 128],
  "tolerance": 0.6,
  "scan_interval": 1.0,
  "click_cooldown": 50.0
}
```

## Safety Features

### Built-in Protections
- **Click Cooldown**: Prevents excessive automation
- **Manual Control**: Easy start/stop functionality
- **Error Handling**: Graceful error recovery
- **Resource Management**: Automatic cleanup on exit

### User Controls
- **Immediate Stop**: Instant detection termination
- **Visual Feedback**: Clear status indicators
- **Activity Logging**: Complete operation history
- **Configuration Backup**: Settings persistence

## Troubleshooting

### Common Issues
1. **"Failed to get device context"**
   - Restart the application
   - Check Windows permissions

2. **"No detections occurring"**
   - Verify target color is correct
   - Adjust tolerance settings
   - Check if detection is active

3. **"High CPU usage"**
   - Increase scan interval
   - Close unnecessary applications

### Performance Tips
- Use scan intervals ≥1ms for best performance
- Set appropriate click cooldown to prevent spam
- Monitor statistics for optimal settings
- Save configurations for different use cases

## Disclaimer
This application is designed for experimental and educational purposes. It demonstrates real-time color detection and automated interaction capabilities. Use responsibly and in accordance with applicable terms of service and regulations.

## Version Information
- **Version**: 1.0
- **Build Date**: 2025
- **Platform**: Windows x64
- **Framework**: Tkinter + Windows API

