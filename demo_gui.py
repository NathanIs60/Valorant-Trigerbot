#!/usr/bin/env python3
"""
Demo script to show the GUI for a few seconds
"""

import sys
import time
import threading
from visual_detector_gui import VisualDetectorGUI

def auto_close_demo(app, delay=10):
    """Auto-close the demo after specified delay"""
    time.sleep(delay)
    print(f"Demo completed after {delay} seconds")
    app.root.quit()

def main():
    print("Visual Detection GUI Demo")
    print("=" * 30)
    print("Starting GUI demonstration...")
    print("The interface will open for 10 seconds to show functionality.")
    print("")
    
    try:
        # Create the GUI application
        app = VisualDetectorGUI()
        
        # Start auto-close timer
        timer_thread = threading.Thread(target=auto_close_demo, args=(app, 10), daemon=True)
        timer_thread.start()
        
        # Run the GUI
        app.run()
        
        print("\nGUI Demo completed successfully!")
        print("Features demonstrated:")
        print("- Real-time status indicators")
        print("- Color configuration controls")
        print("- Detection parameter settings")
        print("- Activity logging")
        print("- Statistics display")
        print("- Start/Stop controls")
        
        return True
        
    except Exception as e:
        print(f"Demo failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)

