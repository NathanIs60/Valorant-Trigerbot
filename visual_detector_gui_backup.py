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

# Windows API setup
user32 = windll.user32
gdi32 = windll.gdi32
kernel32 = windll.kernel32
user32.SetProcessDPIAware()

class VisualDetectorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Visual Detection Control Panel")
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        
        # Detection engine variables
        self.detection_active = False
        self.detection_thread = None
        self.running = False
        
        # Screen setup
        self.screen_width = user32.GetSystemMetrics(0)
        self.screen_height = user32.GetSystemMetrics(1)
        self.center_x = self.screen_width // 2
        self.center_y = self.screen_height // 2
        
        # 9 central pixels
        self.pixel_offsets = [
            (-1, -1), (0, -1), (1, -1),
            (-1,  0), (0,  0), (1,  0),
            (-1,  1), (0,  1), (1,  1)
        ]
        
        # Configuration variables
        self.target_color = [128, 0, 128]  # Purple RGB
        self.tolerance = tk.DoubleVar(value=0.6)  # 60%
        self.scan_interval = tk.DoubleVar(value=1.0)  # 1ms
        self.click_cooldown = tk.DoubleVar(value=50.0)  # 50ms
        
        # Statistics
        self.stats = {
            'detections': 0,
            'clicks': 0,
            'runtime': 0,
            'avg_scan_time': 0.0,
            'scan_times': deque(maxlen=100)
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
        title_label = ttk.Label(main_frame, text="Visual Detection Control Panel", 
                               font=("Arial", 16, "bold"))
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
        status_frame = ttk.LabelFrame(parent, text="Status", padding="10")
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
        params_frame = ttk.LabelFrame(parent, text="Detection Parameters", padding="10")
        params_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Scan interval
        ttk.Label(params_frame, text="Scan Interval (ms):").grid(row=0, column=0, sticky=tk.W)
        scan_spinbox = ttk.Spinbox(params_frame, from_=0.1, to=100.0, width=10, 
                                  textvariable=self.scan_interval, increment=0.1)
        scan_spinbox.grid(row=0, column=1, padx=(10, 0), sticky=tk.W)
        
        # Click cooldown
        ttk.Label(params_frame, text="Click Cooldown (ms):").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        cooldown_spinbox = ttk.Spinbox(params_frame, from_=10.0, to=1000.0, width=10,
                                      textvariable=self.click_cooldown, increment=10.0)
        cooldown_spinbox.grid(row=1, column=1, padx=(10, 0), sticky=tk.W, pady=(5, 0))
        
    def setup_controls_section(self, parent, row):
        """Setup control buttons section"""
        controls_frame = ttk.LabelFrame(parent, text="Controls", padding="10")
        controls_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Start/Stop button
        self.start_stop_button = ttk.Button(controls_frame, text="START DETECTION", 
                                           command=self.toggle_detection)
        self.start_stop_button.grid(row=0, column=0, padx=(0, 10))
        
        # Save/Load config buttons
        ttk.Button(controls_frame, text="Save Config", command=self.save_config).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(controls_frame, text="Load Config", command=self.load_config).grid(row=0, column=2, padx=(0, 10))
        
        # Reset stats button
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
            'scan_time': ttk.Label(stats_frame, text="Avg Scan: 0.0ms")
        }
        
        row_idx = 0
        for key, label in self.stats_labels.items():
            label.grid(row=row_idx // 2, column=row_idx % 2, sticky=tk.W, padx=(0, 20))
            row_idx += 1
            
    def setup_log_section(self, parent, row):
        """Setup log display section"""
        log_frame = ttk.LabelFrame(parent, text="Activity Log", padding="10")
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
            
    def start_detection(self):
        """Start the detection process"""
        try:
            self.hdc = user32.GetDC(0)
            if not self.hdc:
                messagebox.showerror("Error", "Failed to get device context")
                return
                
            self.detection_active = True
            self.running = True
            self.start_time = time.time()
            
            # Update UI
            self.status_canvas.itemconfig(self.status_indicator, fill="green")
            self.status_label.configure(text="ACTIVE", foreground="green")
            self.start_stop_button.configure(text="STOP DETECTION")
            
            # Start detection thread
            self.detection_thread = threading.Thread(target=self.detection_loop, daemon=True)
            self.detection_thread.start()
            
            self.log("Detection started")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start detection: {e}")
            self.log(f"Error starting detection: {e}")
            
    def stop_detection(self):
        """Stop the detection process"""
        self.detection_active = False
        self.running = False
        
        # Release device context
        if self.hdc:
            user32.ReleaseDC(0, self.hdc)
            self.hdc = None
            
        # Update UI
        self.status_canvas.itemconfig(self.status_indicator, fill="red")
        self.status_label.configure(text="INACTIVE", foreground="red")
        self.start_stop_button.configure(text="START DETECTION")
        
        self.log("Detection stopped")
        
    def detection_loop(self):
        """Main detection loop running in separate thread"""
        last_click_time = 0
        
        while self.running:
            try:
                scan_start = time.time()
                
                # Scan 9 central pixels
                purple_detected = False
                detected_positions = []
                
                for offset_x, offset_y in self.pixel_offsets:
                    pixel_x = self.center_x + offset_x
                    pixel_y = self.center_y + offset_y
                    
                    if 0 <= pixel_x < self.screen_width and 0 <= pixel_y < self.screen_height:
                        color = self.get_pixel_color(pixel_x, pixel_y)
                        
                        if color and self.is_target_color(color):
                            purple_detected = True
                            detected_positions.append((pixel_x, pixel_y, color))
                
                scan_time = time.time() - scan_start
                self.stats['scan_times'].append(scan_time)
                
                # Handle detection
                if purple_detected:
                    self.stats['detections'] += 1
                    self.log(f"Target color detected at {len(detected_positions)} pixels")
                    
                    # Perform click if cooldown has passed
                    current_time = time.time()
                    if current_time - last_click_time >= (self.click_cooldown.get() / 1000.0):
                        self.perform_click()
                        last_click_time = current_time
                        self.stats['clicks'] += 1
                
                # Sleep for scan interval
                time.sleep(self.scan_interval.get() / 1000.0)
                
            except Exception as e:
                self.log(f"Detection error: {e}")
                time.sleep(0.1)
                
    def get_pixel_color(self, x, y):
        """Get RGB color of pixel at coordinates"""
        try:
            color_ref = gdi32.GetPixel(self.hdc, x, y)
            if color_ref == 0xFFFFFFFF:
                return None
                
            r = color_ref & 0xFF
            g = (color_ref >> 8) & 0xFF
            b = (color_ref >> 16) & 0xFF
            
            return (r, g, b)
        except:
            return None
            
    def is_target_color(self, color):
        """Check if color matches target within tolerance"""
        if not color:
            return False
            
        # Calculate color similarity using Euclidean distance
        diff_squared = sum((a - b) ** 2 for a, b in zip(color, self.target_color))
        distance = math.sqrt(diff_squared)
        max_distance = math.sqrt(3 * (255 ** 2))
        similarity = 1.0 - (distance / max_distance)
        
        return similarity >= self.tolerance.get()
        
    def perform_click(self):
        """Perform left mouse click"""
        try:
            user32.mouse_event(0x0002, 0, 0, 0, 0)  # MOUSEEVENTF_LEFTDOWN
            time.sleep(0.001)
            user32.mouse_event(0x0004, 0, 0, 0, 0)  # MOUSEEVENTF_LEFTUP
        except Exception as e:
            self.log(f"Click error: {e}")
            
    def update_display(self):
        """Update the display with current statistics"""
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
            
        # Schedule next update
        self.root.after(500, self.update_display)
        
    def log(self, message):
        """Add message to log display"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        # Update log in main thread
        self.root.after(0, self._update_log, log_message)
        
    def _update_log(self, message):
        """Update log text widget (must be called from main thread)"""
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)
        
        # Limit log size
        if self.log_text.index(tk.END).split('.')[0] > '100':
            self.log_text.delete('1.0', '10.0')
            
    def reset_stats(self):
        """Reset all statistics"""
        self.stats['detections'] = 0
        self.stats['clicks'] = 0
        self.stats['scan_times'].clear()
        if hasattr(self, 'start_time'):
            self.start_time = time.time()
        self.log("Statistics reset")
        
    def save_config(self):
        """Save current configuration to file"""
        config = {
            'target_color': self.target_color,
            'tolerance': self.tolerance.get(),
            'scan_interval': self.scan_interval.get(),
            'click_cooldown': self.click_cooldown.get()
        }
        
        try:
            with open('detector_config.json', 'w') as f:
                json.dump(config, f, indent=2)
            self.log("Configuration saved")
            messagebox.showinfo("Success", "Configuration saved successfully")
        except Exception as e:
            self.log(f"Error saving config: {e}")
            messagebox.showerror("Error", f"Failed to save configuration: {e}")
            
    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists('detector_config.json'):
                with open('detector_config.json', 'r') as f:
                    config = json.load(f)
                    
                self.target_color = config.get('target_color', [128, 0, 128])
                self.tolerance.set(config.get('tolerance', 0.6))
                self.scan_interval.set(config.get('scan_interval', 1.0))
                self.click_cooldown.set(config.get('click_cooldown', 50.0))
                
                self.update_color_display()
                self.log("Configuration loaded")
            else:
                self.log("No configuration file found, using defaults")
        except Exception as e:
            self.log(f"Error loading config: {e}")
            
    def on_closing(self):
        """Handle application closing"""
        if self.detection_active:
            self.stop_detection()
        self.root.destroy()
        
    def run(self):
        """Start the GUI application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.log("Visual Detection Control Panel started")
        self.root.mainloop()

if __name__ == "__main__":
    app = VisualDetectorGUI()
    app.run()

