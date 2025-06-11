import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
import threading
import time
import json
import os
from ctypes import windll, wintypes, byref, c_int32, c_uint32, Structure
import math
from collections import deque
import datetime
import traceback

# Windows API setup
user32 = windll.user32
gdi32 = windll.gdi32
kernel32 = windll.kernel32
user32.SetProcessDPIAware()

class UltraStableTriggerBot:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ultra Stable Triggerbot - Never Stops")
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        
        # Detection engine variables
        self.detection_active = False
        self.detection_thread = None
        self.running = False
        self.force_stop = False
        
        # Screen setup
        try:
            self.screen_width = user32.GetSystemMetrics(0)
            self.screen_height = user32.GetSystemMetrics(1)
            self.center_x = self.screen_width // 2
            self.center_y = self.screen_height // 2
            self.log(f"Screen initialized: {self.screen_width}x{self.screen_height}")
        except Exception as e:
            self.screen_width = 1920
            self.screen_height = 1080
            self.center_x = 960
            self.center_y = 540
            self.log(f"Screen setup error, using defaults: {e}")
        
        # 9 central pixels
        self.pixel_offsets = [
            (-1, -1), (0, -1), (1, -1),
            (-1,  0), (0,  0), (1,  0),
            (-1,  1), (0,  1), (1,  1)
        ]
        
        # Configuration variables
        self.target_color = [128, 0, 128]  # Purple RGB
        self.tolerance = tk.DoubleVar(value=0.6)  # 60%
        self.scan_interval = tk.DoubleVar(value=50.0)  # 50ms for stability
        self.click_cooldown = tk.DoubleVar(value=200.0)  # 200ms for safety
        
        # Statistics
        self.stats = {
            'detections': 0,
            'clicks': 0,
            'runtime': 0,
            'avg_scan_time': 0.0,
            'scan_times': deque(maxlen=100),
            'errors': 0,
            'recoveries': 0
        }
        
        # Device context
        self.hdc = None
        
        self.setup_gui()
        self.load_config()
        self.update_display()
        
    def setup_gui(self):
        """Setup the graphical user interface"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Ultra Stable Triggerbot - NEVER STOPS", 
                               font=("Arial", 16, "bold"), foreground="green")
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Status Section
        self.setup_status_section(main_frame, row=1)
        
        # Color Configuration Section
        self.setup_color_section(main_frame, row=2)
        
        # Detection Parameters Section
        self.setup_parameters_section(main_frame, row=3)
        
        # Control Buttons Section
        self.setup_controls_section(main_frame, row=4)
        
        # Statistics Section
        self.setup_statistics_section(main_frame, row=5)
        
        # Log Section
        self.setup_log_section(main_frame, row=6)
        
    def setup_status_section(self, parent, row):
        """Setup status display section"""
        status_frame = ttk.LabelFrame(parent, text="Status - Ultra Stable Mode", padding="10")
        status_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status indicator
        self.status_canvas = tk.Canvas(status_frame, width=20, height=20)
        self.status_canvas.grid(row=0, column=0, padx=(0, 10))
        self.status_indicator = self.status_canvas.create_oval(2, 2, 18, 18, fill="red")
        
        self.status_label = ttk.Label(status_frame, text="INACTIVE", 
                                     font=("Arial", 12, "bold"), foreground="red")
        self.status_label.grid(row=0, column=1, sticky=tk.W)
        
        # Screen info
        screen_info = ttk.Label(status_frame, 
                               text=f"Screen: {self.screen_width}x{self.screen_height} | Center: ({self.center_x}, {self.center_y})")
        screen_info.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
        # Stability info
        stability_info = ttk.Label(status_frame, 
                                  text="Ultra Stable Mode: Maximum error recovery, never stops until manual stop",
                                  foreground="green")
        stability_info.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(2, 0))
        
    def setup_color_section(self, parent, row):
        """Setup color configuration section"""
        color_frame = ttk.LabelFrame(parent, text="Color Configuration", padding="10")
        color_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Current color display
        ttk.Label(color_frame, text="Target Color:").grid(row=0, column=0, sticky=tk.W)
        
        self.color_canvas = tk.Canvas(color_frame, width=50, height=30, bg="purple")
        self.color_canvas.grid(row=0, column=1, padx=(10, 10))
        
        self.color_label = ttk.Label(color_frame, text=f"RGB({self.target_color[0]}, {self.target_color[1]}, {self.target_color[2]})")
        self.color_label.grid(row=0, column=2, sticky=tk.W)
        
        # Color picker button
        ttk.Button(color_frame, text="Choose Color", command=self.choose_color).grid(row=0, column=3, padx=(10, 0))
        
        # Tolerance slider
        ttk.Label(color_frame, text="Tolerance:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        tolerance_frame = ttk.Frame(color_frame)
        tolerance_frame.grid(row=1, column=1, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.tolerance_scale = ttk.Scale(tolerance_frame, from_=0.1, to=1.0, 
                                        variable=self.tolerance, orient=tk.HORIZONTAL, length=200)
        self.tolerance_scale.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.tolerance_value_label = ttk.Label(tolerance_frame, text=f"{self.tolerance.get()*100:.0f}%")
        self.tolerance_value_label.grid(row=0, column=1, padx=(10, 0))
        
        # Update tolerance display when changed
        self.tolerance.trace('w', self.update_tolerance_display)
        
    def setup_parameters_section(self, parent, row):
        """Setup detection parameters section"""
        params_frame = ttk.LabelFrame(parent, text="Ultra Stable Parameters", padding="10")
        params_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Scan interval
        ttk.Label(params_frame, text="Scan Interval (ms):").grid(row=0, column=0, sticky=tk.W)
        scan_spinbox = ttk.Spinbox(params_frame, from_=10.0, to=1000.0, width=10, 
                                  textvariable=self.scan_interval, increment=10.0)
        scan_spinbox.grid(row=0, column=1, padx=(10, 0), sticky=tk.W)
        ttk.Label(params_frame, text="(Stable: 50-100ms)", foreground="green").grid(row=0, column=2, padx=(10, 0), sticky=tk.W)
        
        # Click cooldown
        ttk.Label(params_frame, text="Click Cooldown (ms):").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        cooldown_spinbox = ttk.Spinbox(params_frame, from_=100.0, to=2000.0, width=10,
                                      textvariable=self.click_cooldown, increment=50.0)
        cooldown_spinbox.grid(row=1, column=1, padx=(10, 0), sticky=tk.W, pady=(5, 0))
        ttk.Label(params_frame, text="(Safe: 200-500ms)", foreground="green").grid(row=1, column=2, padx=(10, 0), sticky=tk.W, pady=(5, 0))
        
    def setup_controls_section(self, parent, row):
        """Setup control buttons section"""
        controls_frame = ttk.LabelFrame(parent, text="Controls", padding="10")
        controls_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Start/Stop button
        self.start_stop_button = ttk.Button(controls_frame, text="START ULTRA STABLE MODE", 
                                           command=self.toggle_detection)
        self.start_stop_button.grid(row=0, column=0, padx=(0, 10))
        
        # Emergency stop
        self.emergency_button = ttk.Button(controls_frame, text="EMERGENCY STOP", 
                                          command=self.emergency_stop)
        self.emergency_button.grid(row=0, column=1, padx=(0, 10))
        
        # Save/Load config buttons
        ttk.Button(controls_frame, text="Save Config", command=self.save_config).grid(row=0, column=2, padx=(0, 10))
        ttk.Button(controls_frame, text="Reset Stats", command=self.reset_stats).grid(row=0, column=3)
        
    def setup_statistics_section(self, parent, row):
        """Setup statistics display section"""
        stats_frame = ttk.LabelFrame(parent, text="Statistics", padding="10")
        stats_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Statistics labels
        self.stats_labels = {
            'runtime': ttk.Label(stats_frame, text="Runtime: 0s"),
            'detections': ttk.Label(stats_frame, text="Detections: 0"),
            'clicks': ttk.Label(stats_frame, text="Clicks: 0"),
            'scan_time': ttk.Label(stats_frame, text="Avg Scan: 0.0ms"),
            'errors': ttk.Label(stats_frame, text="Errors: 0"),
            'recoveries': ttk.Label(stats_frame, text="Recoveries: 0")
        }
        
        row_idx = 0
        for key, label in self.stats_labels.items():
            col = row_idx % 3
            row_pos = row_idx // 3
            label.grid(row=row_pos, column=col, sticky=tk.W, padx=(0, 20))
            row_idx += 1
            
    def setup_log_section(self, parent, row):
        """Setup log display section"""
        log_frame = ttk.LabelFrame(parent, text="Activity Log - Ultra Stable Mode", padding="10")
        log_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Log text widget with scrollbar
        log_text_frame = ttk.Frame(log_frame)
        log_text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.log_text = tk.Text(log_text_frame, height=8, width=60, wrap=tk.WORD)
        log_scrollbar = ttk.Scrollbar(log_text_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        log_text_frame.grid_rowconfigure(0, weight=1)
        log_text_frame.grid_columnconfigure(0, weight=1)
        
        # Configure main grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(row, weight=1)
        
    def choose_color(self):
        """Open color picker dialog"""
        current_color = f"#{self.target_color[0]:02x}{self.target_color[1]:02x}{self.target_color[2]:02x}"
        color = colorchooser.askcolor(title="Choose Target Color", initialcolor=current_color)
        
        if color[0]:  # If a color was selected
            self.target_color = [int(color[0][0]), int(color[0][1]), int(color[0][2])]
            self.update_color_display()
            self.log(f"Target color changed to RGB({self.target_color[0]}, {self.target_color[1]}, {self.target_color[2]})")
            
    def update_color_display(self):
        """Update the color display canvas and label"""
        color_hex = f"#{self.target_color[0]:02x}{self.target_color[1]:02x}{self.target_color[2]:02x}"
        self.color_canvas.configure(bg=color_hex)
        self.color_label.configure(text=f"RGB({self.target_color[0]}, {self.target_color[1]}, {self.target_color[2]})")
        
    def update_tolerance_display(self, *args):
        """Update tolerance percentage display"""
        self.tolerance_value_label.configure(text=f"{self.tolerance.get()*100:.0f}%")
        
    def toggle_detection(self):
        """Start or stop the detection process"""
        if not self.detection_active:
            self.start_detection()
        else:
            self.stop_detection()
            
    def emergency_stop(self):
        """Emergency stop - forces immediate shutdown"""
        self.log("EMERGENCY STOP activated!")
        self.force_stop = True
        self.stop_detection()
        
    def start_detection(self):
        """Start the ultra stable detection process"""
        try:
            self.log("Starting Ultra Stable Detection Mode...")
            self.force_stop = False
            
            # Get device context
            self.hdc = user32.GetDC(0)
            if not self.hdc:
                self.log("Warning: Could not get device context, but continuing...")
                
            self.detection_active = True
            self.running = True
            self.start_time = time.time()
            
            # Update UI
            self.status_canvas.itemconfig(self.status_indicator, fill="green")
            self.status_label.configure(text="ULTRA STABLE ACTIVE", foreground="green")
            self.start_stop_button.configure(text="STOP DETECTION")
            
            # Start detection thread
            self.detection_thread = threading.Thread(target=self.ultra_stable_loop, daemon=True)
            self.detection_thread.start()
            
            self.log("Ultra Stable Detection started - Will never stop until manual intervention!")
            
        except Exception as e:
            self.log(f"Start error (but continuing anyway): {e}")
            # Even if there's an error, try to continue
            self.detection_active = True
            self.running = True
            self.start_time = time.time()
            self.detection_thread = threading.Thread(target=self.ultra_stable_loop, daemon=True)
            self.detection_thread.start()
            
    def stop_detection(self):
        """Stop the detection process"""
        self.log("Stopping Ultra Stable Detection...")
        self.detection_active = False
        self.running = False
        
        # Release device context if we have one
        if self.hdc:
            try:
                user32.ReleaseDC(0, self.hdc)
            except:
                pass  # Ignore errors when releasing
            finally:
                self.hdc = None
            
        # Update UI
        self.status_canvas.itemconfig(self.status_indicator, fill="red")
        self.status_label.configure(text="INACTIVE", foreground="red")
        self.start_stop_button.configure(text="START ULTRA STABLE MODE")
        
        self.log("Ultra Stable Detection stopped")
        
    def ultra_stable_loop(self):
        """Ultra stable detection loop that never crashes"""
        last_click_time = 0
        total_errors = 0
        
        self.log("Ultra Stable Loop started - Maximum error recovery mode")
        
        while self.running and not self.force_stop:
            try:
                scan_start = time.time()
                
                # Try to scan pixels - if any error, just continue
                try:
                    purple_detected = False
                    detected_count = 0
                    
                    # Scan with maximum error tolerance
                    for offset_x, offset_y in self.pixel_offsets:
                        try:
                            pixel_x = self.center_x + offset_x
                            pixel_y = self.center_y + offset_y
                            
                            # Ensure coordinates are valid
                            if 0 <= pixel_x < self.screen_width and 0 <= pixel_y < self.screen_height:
                                color = self.get_pixel_color_ultra_safe(pixel_x, pixel_y)
                                
                                if color and self.is_target_color(color):
                                    purple_detected = True
                                    detected_count += 1
                        except:
                            # If individual pixel fails, just skip it
                            continue
                    
                    # Record scan time
                    scan_time = time.time() - scan_start
                    self.stats['scan_times'].append(scan_time)
                    
                    # Handle detection with maximum safety
                    if purple_detected:
                        self.stats['detections'] += 1
                        
                        # Only log occasionally to prevent spam
                        if self.stats['detections'] % 10 == 1:
                            self.log(f"Target detected! (Total: {self.stats['detections']})")
                        
                        # Try to click with maximum safety
                        current_time = time.time()
                        if current_time - last_click_time >= (self.click_cooldown.get() / 1000.0):
                            if self.perform_click_ultra_safe():
                                last_click_time = current_time
                                self.stats['clicks'] += 1
                    
                    # Reset error counter on successful scan
                    total_errors = 0
                    
                except Exception as scan_error:
                    # Handle scan errors gracefully
                    total_errors += 1
                    self.stats['errors'] += 1
                    
                    if total_errors % 10 == 1:  # Log every 10th error only
                        self.log(f"Scan error #{total_errors} (continuing anyway): {str(scan_error)[:50]}")
                    
                    # Even with errors, keep running!
                    time.sleep(0.1)  # Brief pause on error
                    
                # Sleep with error handling
                try:
                    time.sleep(self.scan_interval.get() / 1000.0)
                except:
                    time.sleep(0.05)  # Fallback sleep
                    
            except Exception as loop_error:
                # Even if the entire loop has an error, recover!
                self.stats['recoveries'] += 1
                self.log(f"Loop error #{self.stats['recoveries']} - RECOVERING: {str(loop_error)[:50]}")
                
                # Try to reinitialize device context
                try:
                    if self.hdc:
                        user32.ReleaseDC(0, self.hdc)
                    self.hdc = user32.GetDC(0)
                except:
                    pass
                
                # Continue anyway!
                time.sleep(0.5)  # Longer pause for recovery
        
        self.log("Ultra Stable Loop ended (manual stop or emergency)")
                
    def get_pixel_color_ultra_safe(self, x, y):
        """Get pixel color with maximum error tolerance"""
        try:
            # Try multiple methods
            if self.hdc:
                color_ref = gdi32.GetPixel(self.hdc, x, y)
                if color_ref != 0xFFFFFFFF:
                    r = color_ref & 0xFF
                    g = (color_ref >> 8) & 0xFF
                    b = (color_ref >> 16) & 0xFF
                    return (r, g, b)
            
            # Fallback: try to get new device context
            temp_hdc = user32.GetDC(0)
            if temp_hdc:
                color_ref = gdi32.GetPixel(temp_hdc, x, y)
                user32.ReleaseDC(0, temp_hdc)
                if color_ref != 0xFFFFFFFF:
                    r = color_ref & 0xFF
                    g = (color_ref >> 8) & 0xFF
                    b = (color_ref >> 16) & 0xFF
                    return (r, g, b)
                    
        except:
            pass  # Ignore all errors
            
        return None
            
    def is_target_color(self, color):
        """Check if color matches target within tolerance"""
        try:
            if not color:
                return False
                
            # Calculate color similarity using Euclidean distance
            diff_squared = sum((a - b) ** 2 for a, b in zip(color, self.target_color))
            distance = math.sqrt(diff_squared)
            max_distance = math.sqrt(3 * (255 ** 2))
            similarity = 1.0 - (distance / max_distance)
            
            return similarity >= self.tolerance.get()
        except:
            return False  # If calculation fails, assume no match
        
    def perform_click_ultra_safe(self):
        """Perform mouse click with maximum safety"""
        try:
            # Try multiple click methods
            try:
                user32.mouse_event(0x0002, 0, 0, 0, 0)  # MOUSEEVENTF_LEFTDOWN
                time.sleep(0.001)
                user32.mouse_event(0x0004, 0, 0, 0, 0)  # MOUSEEVENTF_LEFTUP
                return True
            except:
                # Alternative click method
                try:
                    import win32api
                    win32api.mouse_event(0x0002, 0, 0, 0, 0)
                    time.sleep(0.001)
                    win32api.mouse_event(0x0004, 0, 0, 0, 0)
                    return True
                except:
                    # If all methods fail, just continue
                    return False
        except:
            return False
            
    def update_display(self):
        """Update the display with current statistics"""
        try:
            if self.detection_active:
                runtime = time.time() - self.start_time
                self.stats['runtime'] = runtime
                
                # Calculate average scan time
                if self.stats['scan_times']:
                    avg_scan = sum(self.stats['scan_times']) / len(self.stats['scan_times'])
                    self.stats['avg_scan_time'] = avg_scan
                    
                # Update labels
                self.stats_labels['runtime'].configure(text=f"Runtime: {runtime:.1f}s")
                self.stats_labels['detections'].configure(text=f"Detections: {self.stats['detections']}")
                self.stats_labels['clicks'].configure(text=f"Clicks: {self.stats['clicks']}")
                self.stats_labels['scan_time'].configure(text=f"Avg Scan: {self.stats['avg_scan_time']*1000:.2f}ms")
                self.stats_labels['errors'].configure(text=f"Errors: {self.stats['errors']}")
                self.stats_labels['recoveries'].configure(text=f"Recoveries: {self.stats['recoveries']}")
        except:
            pass  # Even display updates shouldn't crash the app
            
        # Schedule next update
        try:
            self.root.after(500, self.update_display)
        except:
            pass
        
    def log(self, message):
        """Add message to log display with error tolerance"""
        try:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            log_message = f"[{timestamp}] {message}\n"
            
            # Update log in main thread
            self.root.after(0, self._update_log, log_message)
        except:
            pass  # Even logging shouldn't crash the app
        
    def _update_log(self, message):
        """Update log text widget (must be called from main thread)"""
        try:
            self.log_text.insert(tk.END, message)
            self.log_text.see(tk.END)
            
            # Limit log size
            lines = self.log_text.index(tk.END).split('.')[0]
            if int(lines) > 200:
                self.log_text.delete('1.0', '50.0')
        except:
            pass
            
    def reset_stats(self):
        """Reset all statistics"""
        try:
            self.stats['detections'] = 0
            self.stats['clicks'] = 0
            self.stats['errors'] = 0
            self.stats['recoveries'] = 0
            self.stats['scan_times'].clear()
            if hasattr(self, 'start_time'):
                self.start_time = time.time()
            self.log("Statistics reset")
        except Exception as e:
            self.log(f"Error resetting stats: {e}")
        
    def save_config(self):
        """Save current configuration to file"""
        config = {
            'target_color': self.target_color,
            'tolerance': self.tolerance.get(),
            'scan_interval': self.scan_interval.get(),
            'click_cooldown': self.click_cooldown.get()
        }
        
        try:
            with open('ultra_stable_config.json', 'w') as f:
                json.dump(config, f, indent=2)
            self.log("Ultra Stable configuration saved")
        except Exception as e:
            self.log(f"Error saving config: {e}")
            
    def load_config(self):
        """Load configuration from file"""
        try:
            config_files = ['ultra_stable_config.json', 'detector_config.json']
            config = None
            
            for config_file in config_files:
                if os.path.exists(config_file):
                    with open(config_file, 'r') as f:
                        config = json.load(f)
                    break
            
            if config:
                self.target_color = config.get('target_color', [128, 0, 128])
                self.tolerance.set(config.get('tolerance', 0.6))
                self.scan_interval.set(config.get('scan_interval', 50.0))
                self.click_cooldown.set(config.get('click_cooldown', 200.0))
                
                self.update_color_display()
        except:
            pass  # Use defaults if config fails
            
    def on_closing(self):
        """Handle application closing"""
        if self.detection_active:
            self.emergency_stop()
        self.root.destroy()
        
    def run(self):
        """Start the GUI application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.log("Ultra Stable Triggerbot started - NEVER STOPS mode!")
        self.root.mainloop()

if __name__ == "__main__":
    app = UltraStableTriggerBot()
    app.run()

