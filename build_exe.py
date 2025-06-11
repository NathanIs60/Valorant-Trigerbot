#!/usr/bin/env python3
"""
Build script to create standalone .exe file
"""

import subprocess
import sys
import os

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("PyInstaller already installed")
        return True
    except ImportError:
        print("Installing PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to install PyInstaller: {e}")
            return False

def build_exe():
    """Build the .exe file using PyInstaller"""
    if not install_pyinstaller():
        return False
        
    print("Building standalone .exe file...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single .exe file
        "--windowed",                   # No console window
        "--name=VisualDetector",        # Output name
        "--icon=icon.ico",              # Icon (if exists)
        "--add-data=detector_config.json;.",  # Include config file
        "--optimize=2",                 # Optimize bytecode
        "--strip",                      # Strip debug symbols
        "visual_detector_gui.py"        # Main script
    ]
    
    # Remove icon option if file doesn't exist
    if not os.path.exists("icon.ico"):
        cmd = [arg for arg in cmd if not arg.startswith("--icon")]
        
    # Remove config data if file doesn't exist
    if not os.path.exists("detector_config.json"):
        cmd = [arg for arg in cmd if not arg.startswith("--add-data")]
    
    try:
        subprocess.check_call(cmd)
        print("\n" + "="*50)
        print("BUILD SUCCESSFUL!")
        print("="*50)
        print(f"Executable created: dist/VisualDetector.exe")
        print("You can now distribute this single .exe file")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        return False
    except FileNotFoundError:
        print("PyInstaller not found in PATH")
        return False

def create_icon():
    """Create a simple icon file if it doesn't exist"""
    if not os.path.exists("icon.ico"):
        print("Creating default icon...")
        try:
            # Try to create a simple icon using PIL if available
            from PIL import Image, ImageDraw
            
            # Create a 32x32 purple square icon
            img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            draw.rectangle([4, 4, 28, 28], fill=(128, 0, 128, 255))
            draw.rectangle([8, 8, 24, 24], outline=(255, 255, 255, 255), width=2)
            
            img.save('icon.ico', format='ICO')
            print("Icon created successfully")
            return True
        except ImportError:
            print("PIL not available, skipping icon creation")
            return False
        except Exception as e:
            print(f"Failed to create icon: {e}")
            return False
    return True

def main():
    print("Visual Detector GUI Build Script")
    print("=" * 40)
    
    # Check if main script exists
    if not os.path.exists("visual_detector_gui.py"):
        print("Error: visual_detector_gui.py not found!")
        return False
        
    # Create icon if possible
    create_icon()
    
    # Build the executable
    if build_exe():
        print("\nBuild completed successfully!")
        print("\nFiles created:")
        print("- dist/VisualDetector.exe (main executable)")
        print("- build/ (temporary build files)")
        print("- VisualDetector.spec (PyInstaller spec file)")
        print("\nYou can delete the 'build' folder and .spec file if desired.")
        print("The .exe file in 'dist' folder is all you need to distribute.")
        return True
    else:
        print("\nBuild failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)

