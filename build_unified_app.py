#!/usr/bin/env python3
"""
Build script for Unified Trading Bot Application
"""

import subprocess
import sys
import os
import shutil

def main():
    print("🚀 Building Unified Trading Bot Application")
    print("=" * 50)
    print()
    
    try:
        # Step 1: Clean old builds
        print("Step 1: Cleaning old build files")
        
        if os.path.exists("dist"):
            shutil.rmtree("dist")
            print("✓ Old dist folder removed")
        
        if os.path.exists("build"):
            shutil.rmtree("build")
            print("✓ Old build folder removed")
            
        for spec_file in ["UnifiedTradingBot.spec", "TradingBotManager.spec"]:
            if os.path.exists(spec_file):
                os.remove(spec_file)
                print(f"✓ Old spec file {spec_file} removed")
        
        # Step 2: Build the unified application
        print("\nStep 2: Building Unified Trading Bot executable")
        
        cmd = [
            "pyinstaller",
            "--onefile",
            "--windowed",
            "--name=UnifiedTradingBot",
            "--optimize=2",
            "--add-data=trading_bot_config.json;." if os.path.exists("trading_bot_config.json") else "",
            "unified_trading_bot.py"
        ]
        
        # Remove empty add-data if config doesn't exist
        cmd = [arg for arg in cmd if arg]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Build successful!")
            
            if os.path.exists("dist/UnifiedTradingBot.exe"):
                file_size = os.path.getsize("dist/UnifiedTradingBot.exe")
                print(f"✓ Unified Trading Bot executable created: {file_size/1024/1024:.1f} MB")
                
                print("\n🎉 UNIFIED TRADING BOT READY!")
                print("\nFeatures:")
                print("- Multiple trading bot selection")
                print("- Purple, Green, Red, Blue, and Multi-color bots")
                print("- Real-time bot switching")
                print("- Performance monitoring")
                print("- Emergency stop functionality")
                print("- Configuration save/load")
                print("- Activity logging")
                print("\nFile: dist/UnifiedTradingBot.exe")
                return True
            else:
                print("❌ Executable not created")
                return False
        else:
            print("❌ Build failed")
            print("Build output:")
            print(result.stdout)
            print("Build errors:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)