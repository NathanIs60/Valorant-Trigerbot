import numpy as np
import time
import threading
import sys
import os
from ctypes import windll, wintypes, byref, c_int32, c_uint32, Structure, POINTER
import datetime
import math
from collections import deque

# Windows API structures and functions for optimized pixel reading
class POINT(Structure):
    _fields_ = [("x", c_int32), ("y", c_int32)]

class COLORREF(Structure):
    _fields_ = [("rgb", c_uint32)]

# Windows API setup
user32 = windll.user32
gdi32 = windll.gdi32
kernel32 = windll.kernel32

# DPI awareness for accurate pixel coordinates
user32.SetProcessDPIAware()

class ExperimentalTriggerBot:
    """Experimental triggerbot for real-time purple detection in 9 central pixels"""
    
    def __init__(self):
        self.running = False
        self.enabled = False
        self.click_count = 0
        self.detection_count = 0
        self.start_time = time.time()
        
        # Screen dimensions
        self.screen_width = user32.GetSystemMetrics(0)
        self.screen_height = user32.GetSystemMetrics(1)
        self.center_x = self.screen_width // 2
        self.center_y = self.screen_height // 2
        
        # Define 9 central pixels in 3x3 grid
        self.pixel_offsets = [
            (-1, -1), (0, -1), (1, -1),
            (-1,  0), (0,  0), (1,  0),
            (-1,  1), (0,  1), (1,  1)
        ]
        
        # Purple color configuration
        self.base_purple_rgb = (128, 0, 128)  # Standard purple
        self.tolerance = 0.6  # 60% tolerance
        
        # Performance optimization settings
        self.scan_interval = 0.001  # 1ms scan interval for responsiveness
        self.click_cooldown = 0.05  # 50ms between clicks to prevent spam
        self.last_click_time = 0
        
        # Statistics tracking
        self.performance_stats = {
            'scan_times': deque(maxlen=1000),
            'detection_rate': 0.0,
            'avg_scan_time': 0.0
        }
        
        # Get device context for fast pixel reading
        self.hdc = user32.GetDC(0)
        
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging to file"""
        try:
            log_path = os.path.join(os.getcwd(), "experimental_triggerbot_log.txt")
            self.log_file = open(log_path, 'w', encoding='utf-8')
            self.log("Experimental Triggerbot System Initialized")
            self.log(f"Screen Resolution: {self.screen_width}x{self.screen_height}")
            self.log(f"Center Point: ({self.center_x}, {self.center_y})")
            self.log(f"Target Color: RGB{self.base_purple_rgb}")
            self.log(f"Tolerance: {self.tolerance * 100}%")
            self.log("Controls: 'E' to toggle, 'Q' to quit")
        except Exception as e:
            print(f"Logging setup failed: {e}")
            self.log_file = None
    
    def log(self, message):
        """Log message with timestamp"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        if self.log_file:
            self.log_file.write(log_message + "\n")
            self.log_file.flush()
    
    def get_pixel_color_fast(self, x, y):
        """Optimized pixel color retrieval using Windows GDI"""
        try:
            color_ref = gdi32.GetPixel(self.hdc, x, y)
            if color_ref == 0xFFFFFFFF:  # Invalid pixel
                return None
            
            # Extract RGB components from COLORREF
            r = color_ref & 0xFF
            g = (color_ref >> 8) & 0xFF
            b = (color_ref >> 16) & 0xFF
            
            return (r, g, b)
        except Exception:
            return None
    
    def calculate_color_similarity(self, color1, color2):
        """Calculate color similarity using optimized Euclidean distance"""
        if not color1 or not color2:
            return 0.0
        
        # Vectorized calculation for speed
        diff_squared = sum((a - b) ** 2 for a, b in zip(color1, color2))
        distance = math.sqrt(diff_squared)
        max_distance = math.sqrt(3 * (255 ** 2))
        
        return 1.0 - (distance / max_distance)
    
    def is_purple_detected(self, rgb_color):
        """Check if color matches purple within tolerance"""
        if not rgb_color:
            return False
        
        similarity = self.calculate_color_similarity(rgb_color, self.base_purple_rgb)
        return similarity >= self.tolerance
    
    def scan_central_pixels(self):
        """Scan the 9 central pixels for purple detection"""
        scan_start = time.time()
        purple_pixels = 0
        detected_colors = []
        
        for offset_x, offset_y in self.pixel_offsets:
            pixel_x = self.center_x + offset_x
            pixel_y = self.center_y + offset_y
            
            # Ensure pixel is within screen bounds
            if 0 <= pixel_x < self.screen_width and 0 <= pixel_y < self.screen_height:
                color = self.get_pixel_color_fast(pixel_x, pixel_y)
                
                if self.is_purple_detected(color):
                    purple_pixels += 1
                    detected_colors.append((pixel_x, pixel_y, color))
        
        scan_time = time.time() - scan_start
        self.performance_stats['scan_times'].append(scan_time)
        
        if purple_pixels > 0:
            self.detection_count += 1
            return True, detected_colors
        
        return False, []
    
    def perform_click(self):
        """Execute left mouse click with optimized timing"""
        current_time = time.time()
        
        # Check cooldown to prevent click spam
        if current_time - self.last_click_time < self.click_cooldown:
            return False
        
        try:
            # Get current cursor position
            cursor_pos = POINT()
            user32.GetCursorPos(byref(cursor_pos))
            
            # Perform click at current position
            user32.SetCursorPos(cursor_pos.x, cursor_pos.y)
            user32.mouse_event(0x0002, 0, 0, 0, 0)  # MOUSEEVENTF_LEFTDOWN
            time.sleep(0.001)  # Minimal delay
            user32.mouse_event(0x0004, 0, 0, 0, 0)  # MOUSEEVENTF_LEFTUP
            
            self.click_count += 1
            self.last_click_time = current_time
            
            return True
        except Exception as e:
            self.log(f"Click error: {e}")
            return False
    
    def update_performance_stats(self):
        """Update performance statistics"""
        if self.performance_stats['scan_times']:
            self.performance_stats['avg_scan_time'] = sum(self.performance_stats['scan_times']) / len(self.performance_stats['scan_times'])
        
        elapsed_time = time.time() - self.start_time
        if elapsed_time > 0:
            self.performance_stats['detection_rate'] = self.detection_count / elapsed_time
    
    def print_stats(self):
        """Print current performance statistics"""
        self.update_performance_stats()
        elapsed = time.time() - self.start_time
        
        stats_msg = (
            f"Runtime: {elapsed:.1f}s | "
            f"Clicks: {self.click_count} | "
            f"Detections: {self.detection_count} | "
            f"Avg Scan: {self.performance_stats['avg_scan_time']*1000:.2f}ms | "
            f"Detection Rate: {self.performance_stats['detection_rate']:.2f}/s"
        )
        
        self.log(stats_msg)
    
    def handle_input(self):
        """Handle keyboard input in a separate thread"""
        try:
            import msvcrt
            while self.running:
                if msvcrt.kbhit():
                    key = msvcrt.getch().decode('utf-8').lower()
                    
                    if key == 'e':
                        self.enabled = not self.enabled
                        status = "ENABLED" if self.enabled else "DISABLED"
                        self.log(f"Triggerbot {status}")
                        # Audio feedback
                        frequency = 800 if self.enabled else 400
                        kernel32.Beep(frequency, 100)
                    
                    elif key == 'q':
                        self.log("Shutdown requested")
                        self.running = False
                        break
                
                time.sleep(0.01)
        except ImportError:
            self.log("msvcrt not available, using alternative input method")
            # Fallback for non-Windows or different Python environments
            time.sleep(1)
    
    def run_experiment(self):
        """Main experimental loop"""
        self.log("Starting experimental triggerbot system...")
        self.log("Press 'E' to toggle bot, 'Q' to quit")
        
        self.running = True
        self.start_time = time.time()
        
        # Start input handler thread
        input_thread = threading.Thread(target=self.handle_input, daemon=True)
        input_thread.start()
        
        stats_timer = time.time()
        
        try:
            while self.running:
                if self.enabled:
                    # Perform scan
                    purple_detected, detected_colors = self.scan_central_pixels()
                    
                    if purple_detected:
                        # Log detection details
                        color_info = ", ".join([f"({x},{y}):{rgb}" for x, y, rgb in detected_colors])
                        self.log(f"Purple detected at: {color_info}")
                        
                        # Perform click
                        if self.perform_click():
                            self.log(f"Click executed #{self.click_count}")
                    
                    # Minimal delay for CPU efficiency
                    time.sleep(self.scan_interval)
                else:
                    # Longer sleep when disabled to save CPU
                    time.sleep(0.1)
                
                # Print stats every 10 seconds
                if time.time() - stats_timer > 10:
                    self.print_stats()
                    stats_timer = time.time()
        
        except KeyboardInterrupt:
            self.log("Keyboard interrupt received")
        except Exception as e:
            self.log(f"Unexpected error: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.running = False
        
        if hasattr(self, 'hdc'):
            user32.ReleaseDC(0, self.hdc)
        
        self.print_stats()
        self.log("Experimental triggerbot system stopped")
        
        if self.log_file:
            self.log_file.close()

# Entry point
if __name__ == "__main__":
    print("Experimental Triggerbot System")
    print("==============================")
    print("This is an experimental color detection system.")
    print("It monitors 9 central pixels for purple color detection.")
    print("")
    
    try:
        bot = ExperimentalTriggerBot()
        bot.run_experiment()
    except Exception as e:
        print(f"Fatal error: {e}")
        input("Press Enter to exit...")

