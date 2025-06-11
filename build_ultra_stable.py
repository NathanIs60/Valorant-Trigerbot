#!/usr/bin/env python3
"""
Build script for Ultra Stable Triggerbot
"""

import subprocess
import sys
import os
import shutil

def main():
    print("🚀 Building Ultra Stable Triggerbot")
    print("=" * 40)
    print()
    
    try:
        # Step 1: Replace main GUI with ultra stable version
        print("Step 1: Applying Ultra Stable version")
        
        if os.path.exists("visual_detector_gui.py"):
            shutil.copy("visual_detector_gui.py", "visual_detector_gui_old.py")
            print("✓ Original GUI backed up")
        
        if os.path.exists("visual_detector_gui_ultra_stable.py"):
            shutil.copy("visual_detector_gui_ultra_stable.py", "visual_detector_gui.py")
            print("✓ Ultra Stable version applied")
        else:
            print("❌ Ultra Stable version not found!")
            return False
        
        # Step 2: Clean old build
        print("\nStep 2: Cleaning build files")
        
        if os.path.exists("dist"):
            shutil.rmtree("dist")
            print("✓ Old dist removed")
        
        if os.path.exists("build"):
            shutil.rmtree("build")
            print("✓ Old build removed")
            
        if os.path.exists("VisualDetector.spec"):
            os.remove("VisualDetector.spec")
            print("✓ Old spec removed")
        
        # Step 3: Build Ultra Stable version
        print("\nStep 3: Building Ultra Stable executable")
        
        # Updated PyInstaller command for ultra stable
        cmd = [
            "pyinstaller",
            "--onefile",
            "--windowed",
            "--name=UltraStableTriggerbot",
            "--optimize=2",
            "visual_detector_gui.py"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Build successful!")
            
            if os.path.exists("dist/UltraStableTriggerbot.exe"):
                file_size = os.path.getsize("dist/UltraStableTriggerbot.exe")
                print(f"✓ Ultra Stable executable created: {file_size/1024/1024:.1f} MB")
                
                print("\n🎉 ULTRA STABLE TRIGGERBOT READY!")
                print("\nFeatures:")
                print("- NEVER STOPS until manual intervention")
                print("- Maximum error recovery")
                print("- Handles all click errors gracefully")
                print("- Automatic device context recovery")
                print("- Emergency stop button")
                print("- Ultra safe parameter defaults")
                print("\nFile: dist/UltraStableTriggerbot.exe")
                return True
            else:
                print("❌ Executable not created")
                return False
        else:
            print("❌ Build failed")
            print(result.stdout)
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)

