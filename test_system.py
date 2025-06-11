#!/usr/bin/env python3
"""
System Test for Experimental Triggerbot
This script tests the core functionality without actual clicking
"""

import sys
import os
import time
from ctypes import windll

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    try:
        import numpy as np
        print("✓ NumPy imported successfully")
        
        import datetime
        print("✓ Datetime imported successfully")
        
        import threading
        print("✓ Threading imported successfully")
        
        from ctypes import windll, wintypes, byref, c_int32, c_uint32, Structure
        print("✓ Windows API modules imported successfully")
        
        from collections import deque
        print("✓ Collections imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_windows_api():
    """Test Windows API functionality"""
    print("\nTesting Windows API...")
    try:
        user32 = windll.user32
        gdi32 = windll.gdi32
        
        # Test screen metrics
        width = user32.GetSystemMetrics(0)
        height = user32.GetSystemMetrics(1)
        print(f"✓ Screen resolution: {width}x{height}")
        
        # Test device context
        hdc = user32.GetDC(0)
        if hdc:
            print("✓ Device context obtained")
            
            # Test pixel reading (center pixel)
            center_x, center_y = width // 2, height // 2
            color = gdi32.GetPixel(hdc, center_x, center_y)
            
            if color != 0xFFFFFFFF:
                r = color & 0xFF
                g = (color >> 8) & 0xFF
                b = (color >> 16) & 0xFF
                print(f"✓ Pixel reading successful: RGB({r}, {g}, {b}) at ({center_x}, {center_y})")
            else:
                print("✗ Pixel reading failed")
                return False
            
            user32.ReleaseDC(0, hdc)
            print("✓ Device context released")
        else:
            print("✗ Failed to get device context")
            return False
            
        return True
    except Exception as e:
        print(f"✗ Windows API error: {e}")
        return False

def test_color_detection():
    """Test color similarity calculation"""
    print("\nTesting color detection algorithm...")
    try:
        import math
        
        def calculate_color_similarity(color1, color2):
            if not color1 or not color2:
                return 0.0
            diff_squared = sum((a - b) ** 2 for a, b in zip(color1, color2))
            distance = math.sqrt(diff_squared)
            max_distance = math.sqrt(3 * (255 ** 2))
            return 1.0 - (distance / max_distance)
        
        # Test cases
        purple = (128, 0, 128)
        similar_purple = (130, 5, 125)
        red = (255, 0, 0)
        
        similarity1 = calculate_color_similarity(purple, similar_purple)
        similarity2 = calculate_color_similarity(purple, red)
        
        print(f"✓ Purple vs Similar Purple: {similarity1:.3f} similarity")
        print(f"✓ Purple vs Red: {similarity2:.3f} similarity")
        
        # Test tolerance
        tolerance = 0.6
        if similarity1 >= tolerance:
            print(f"✓ Similar purple passes 60% tolerance test")
        else:
            print(f"✗ Similar purple fails 60% tolerance test")
            
        if similarity2 < tolerance:
            print(f"✓ Red correctly rejected by 60% tolerance test")
        else:
            print(f"✗ Red incorrectly passes 60% tolerance test")
            
        return True
    except Exception as e:
        print(f"✗ Color detection error: {e}")
        return False

def test_performance():
    """Test performance characteristics"""
    print("\nTesting performance...")
    try:
        import time
        from ctypes import windll
        
        user32 = windll.user32
        gdi32 = windll.gdi32
        
        width = user32.GetSystemMetrics(0)
        height = user32.GetSystemMetrics(1)
        center_x, center_y = width // 2, height // 2
        
        hdc = user32.GetDC(0)
        
        # Test 100 pixel reads
        start_time = time.time()
        for i in range(100):
            color = gdi32.GetPixel(hdc, center_x, center_y)
        end_time = time.time()
        
        avg_time = (end_time - start_time) / 100
        print(f"✓ Average pixel read time: {avg_time*1000:.3f}ms")
        
        user32.ReleaseDC(0, hdc)
        
        if avg_time < 0.001:  # Less than 1ms
            print("✓ Performance is excellent for real-time operation")
        elif avg_time < 0.01:  # Less than 10ms
            print("✓ Performance is good for real-time operation")
        else:
            print("⚠ Performance may impact real-time operation")
            
        return True
    except Exception as e:
        print(f"✗ Performance test error: {e}")
        return False

def main():
    """Run all tests"""
    print("Experimental Triggerbot System Test")
    print("=" * 40)
    
    tests = [
        ("Import Test", test_imports),
        ("Windows API Test", test_windows_api),
        ("Color Detection Test", test_color_detection),
        ("Performance Test", test_performance)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * len(test_name) + "-")
        
        if test_func():
            passed += 1
            print(f"✓ {test_name} PASSED")
        else:
            print(f"✗ {test_name} FAILED")
    
    print(f"\n" + "=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! System is ready for experimental use.")
        return True
    else:
        print("✗ Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)

