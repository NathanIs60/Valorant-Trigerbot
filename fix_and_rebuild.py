#!/usr/bin/env python3
"""
Quick fix and rebuild script for the visual detector
"""

import shutil
import os
import subprocess
import sys

def main():
    print("🔧 Visual Detector - Quick Fix & Rebuild")
    print("=" * 45)
    print()
    
    try:
        # Step 1: Replace the original GUI with the fixed version
        print("Step 1: Applying fixes to visual_detector_gui.py")
        
        # Backup original
        if os.path.exists("visual_detector_gui.py"):
            shutil.copy("visual_detector_gui.py", "visual_detector_gui_backup.py")
            print("✓ Original GUI backed up")
        
        # Replace with fixed version
        if os.path.exists("visual_detector_gui_fixed.py"):
            shutil.copy("visual_detector_gui_fixed.py", "visual_detector_gui.py")
            print("✓ Fixed version applied")
        else:
            print("❌ Fixed version not found!")
            return False
        
        # Step 2: Clean old build
        print("\nStep 2: Cleaning old build files")
        
        if os.path.exists("dist"):
            shutil.rmtree("dist")
            print("✓ Old dist folder removed")
        
        if os.path.exists("build"):
            shutil.rmtree("build")
            print("✓ Old build folder removed")
            
        if os.path.exists("VisualDetector.spec"):
            os.remove("VisualDetector.spec")
            print("✓ Old spec file removed")
        
        # Step 3: Rebuild
        print("\nStep 3: Building new executable")
        
        result = subprocess.run([sys.executable, "build_exe.py"], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Build successful!")
            
            # Check if exe was created
            if os.path.exists("dist/VisualDetector.exe"):
                file_size = os.path.getsize("dist/VisualDetector.exe")
                print(f"✓ New executable created: {file_size/1024/1024:.1f} MB")
                
                print("\n🎉 Fix and rebuild completed successfully!")
                print("\nWhat was fixed:")
                print("- Enhanced error handling")
                print("- Better Windows API initialization")
                print("- Improved device context management")
                print("- Added diagnostics and API testing")
                print("- Slower, more stable default settings")
                print("- Better recovery from errors")
                print("\nThe new executable should work more reliably.")
                return True
            else:
                print("❌ Executable not found after build")
                return False
        else:
            print("❌ Build failed")
            print("Build output:")
            print(result.stdout)
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error during fix and rebuild: {e}")
        return False

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)

