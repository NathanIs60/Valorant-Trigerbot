#!/usr/bin/env python3
"""
Installer script for GUI requirements
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a Python package using pip"""
    try:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ {package} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install {package}: {e}")
        return False
    except Exception as e:
        print(f"✗ Error installing {package}: {e}")
        return False

def check_package(package):
    """Check if a package is already installed"""
    try:
        __import__(package.split('>=')[0].split('==')[0])
        print(f"✓ {package} already installed")
        return True
    except ImportError:
        return False

def main():
    print("Visual Detection GUI - Requirements Installer")
    print("=" * 50)
    print()
    
    # List of required packages
    packages = [
        "numpy>=1.19.0",
        "pyinstaller>=4.0",
        "pillow>=8.0.0"
    ]
    
    installed = 0
    total = len(packages)
    
    print("Checking and installing required packages...")
    print()
    
    for package in packages:
        package_name = package.split('>=')[0].split('==')[0]
        
        if not check_package(package_name):
            if install_package(package):
                installed += 1
        else:
            installed += 1
    
    print()
    print("=" * 50)
    print(f"Installation Results: {installed}/{total} packages ready")
    
    if installed == total:
        print("✓ All requirements installed successfully!")
        print()
        print("You can now:")
        print("1. Run the GUI: python visual_detector_gui.py")
        print("2. Launch demo: python demo_gui.py")
        print("3. Build .exe: python build_exe.py")
        print("4. Use batch file: launch_gui.bat")
        return True
    else:
        print("✗ Some packages failed to install.")
        print("Please check the errors above and try again.")
        return False

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)

