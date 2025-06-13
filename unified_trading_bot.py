import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import json
import os
from ctypes import windll, wintypes, byref, c_int32, c_uint32, Structure, POINTER
import math
from collections import deque
import datetime
import random

# Windows API setup
user32 = windll.user32
gdi32 = windll.gdi32
kernel32 = windll.kernel32
user32.SetProcessDPIAware()

# Advanced Windows API structures for hardware simulation
class POINT(Structure):
    _fields_ = [("x", c_int32), ("y", c_int32)]

class MOUSEINPUT(Structure):
    _fields_ = [("dx", c_int32),
                ("dy", c_int32),
                ("mouseData", c_uint32),
                ("dwFlags", c_uint32),
                ("time", c_uint32),
                ("dwExtraInfo", POINTER(c_uint32))]

class INPUT(Structure):
    class _INPUT(Structure):
        _fields_ = [("mi", MOUSEINPUT)]
    
    _anonymous_ = ("_input",)
    _fields_ = [("type", c_uint32),
                ("_input", _INPUT)]

class HardwareClickSimulator:
    """Advanced hardware-level click simulation"""
    
    def __init__(self):
        self.user32 = windll.user32
        self.kernel32 = windll.kernel32
        
        # Hardware timing parameters (microseconds)
        self.HARDWARE_CLICK_DOWN_TIME = random.uniform(8000, 15000)  # 8-15ms
        self.HARDWARE_CLICK_UP_TIME = random.uniform(1000, 3000)     # 1-3ms
        self.HARDWARE_JITTER = random.uniform(500, 2000)             # 0.5-2ms
        
        # Mouse hardware constants
        self.INPUT_MOUSE = 0
        self.MOUSEEVENTF_LEFTDOWN = 0x0002
        self.MOUSEEVENTF_LEFTUP = 0x0004
        self.MOUSEEVENTF_MOVE = 0x0001
        self.MOUSEEVENTF_ABSOLUTE = 0x8000
        
    def simulate_hardware_click(self, method="advanced"):
        """Simulate hardware-level mouse click"""
        try:
            if method == "advanced":
                return self._advanced_hardware_click()
            elif method == "raw_input":
                return self._raw_input_click()
            elif method == "direct_injection":
                return self._direct_injection_click()
            elif method == "timing_simulation":
                return self._timing_simulation_click()
            else:
                return self._standard_click()
        except Exception as e:
            print(f"Hardware click error: {e}")
            return False
    
    def _advanced_hardware_click(self):
        """Advanced hardware simulation with micro-movements"""
        try:
            # Get current cursor position
            cursor_pos = POINT()
            self.user32.GetCursorPos(byref(cursor_pos))
            
            # Add micro-movement (hardware mice have slight imprecision)
            micro_x = random.uniform(-0.5, 0.5)
            micro_y = random.uniform(-0.5, 0.5)
            
            new_x = int(cursor_pos.x + micro_x)
            new_y = int(cursor_pos.y + micro_y)
            
            # Simulate hardware timing variations
            pre_click_delay = random.uniform(0.001, 0.005)  # Human reaction time
            time.sleep(pre_click_delay)
            
            # Move with hardware-like precision
            self.user32.SetCursorPos(new_x, new_y)
            time.sleep(random.uniform(0.0005, 0.002))  # Hardware settling time
            
            # Hardware-style click with variable timing
            click_down_time = random.uniform(0.008, 0.015)  # 8-15ms
            click_up_delay = random.uniform(0.001, 0.003)   # 1-3ms
            
            # Mouse down
            self.user32.mouse_event(self.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(click_down_time)
            
            # Mouse up
            self.user32.mouse_event(self.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            time.sleep(click_up_delay)
            
            return True
            
        except Exception as e:
            print(f"Advanced hardware click error: {e}")
            return False
    
    def _raw_input_click(self):
        """Raw input simulation"""
        try:
            # Simulate raw input device
            inputs = INPUT()
            inputs.type = self.INPUT_MOUSE
            
            # Mouse down
            inputs._input.mi.dx = 0
            inputs._input.mi.dy = 0
            inputs._input.mi.mouseData = 0
            inputs._input.mi.dwFlags = self.MOUSEEVENTF_LEFTDOWN
            inputs._input.mi.time = 0
            inputs._input.mi.dwExtraInfo = None
            
            self.user32.SendInput(1, byref(inputs), 28)
            
            # Hardware timing
            time.sleep(random.uniform(0.008, 0.015))
            
            # Mouse up
            inputs._input.mi.dwFlags = self.MOUSEEVENTF_LEFTUP
            self.user32.SendInput(1, byref(inputs), 28)
            
            return True
            
        except Exception as e:
            print(f"Raw input click error: {e}")
            return False
    
    def _direct_injection_click(self):
        """Direct message injection"""
        try:
            hwnd = self.user32.GetForegroundWindow()
            if not hwnd:
                return False
            
            # Get window coordinates
            rect = wintypes.RECT()
            self.user32.GetWindowRect(hwnd, byref(rect))
            
            # Calculate relative position
            cursor_pos = POINT()
            self.user32.GetCursorPos(byref(cursor_pos))
            
            rel_x = cursor_pos.x - rect.left
            rel_y = cursor_pos.y - rect.top
            lparam = (rel_y << 16) | rel_x
            
            # Hardware-style timing
            pre_delay = random.uniform(0.001, 0.003)
            time.sleep(pre_delay)
            
            # Send messages with hardware timing
            self.user32.SendMessageW(hwnd, 0x0201, 0x0001, lparam)  # WM_LBUTTONDOWN
            time.sleep(random.uniform(0.008, 0.015))
            self.user32.SendMessageW(hwnd, 0x0202, 0x0000, lparam)  # WM_LBUTTONUP
            
            return True
            
        except Exception as e:
            print(f"Direct injection click error: {e}")
            return False
    
    def _timing_simulation_click(self):
        """Precise timing simulation"""
        try:
            # Simulate electrical signal timing
            signal_propagation_delay = random.uniform(0.0001, 0.0005)  # 0.1-0.5ms
            time.sleep(signal_propagation_delay)
            
            # Simulate switch bounce (hardware mice have this)
            bounce_iterations = random.randint(1, 3)
            
            for i in range(bounce_iterations):
                # Mouse down with bounce
                self.user32.mouse_event(self.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                if i < bounce_iterations - 1:
                    time.sleep(random.uniform(0.0001, 0.0003))  # Bounce delay
            
            # Hold time (mechanical switch characteristic)
            hold_time = random.uniform(0.008, 0.015)
            time.sleep(hold_time)
            
            # Mouse up with bounce
            for i in range(bounce_iterations):
                self.user32.mouse_event(self.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
                if i < bounce_iterations - 1:
                    time.sleep(random.uniform(0.0001, 0.0003))
            
            return True
            
        except Exception as e:
            print(f"Timing simulation click error: {e}")
            return False
    
    def _standard_click(self):
        """Standard click as fallback"""
        try:
            self.user32.mouse_event(self.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(0.001)
            self.user32.mouse_event(self.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            return True
        except:
            return False

class TradingBot:
    """Base class for all trading bots"""
    def __init__(self, name, description, target_color, tolerance=0.6):
        self.name = name
        self.description = description
        self.target_color = target_color
        self.tolerance = tolerance
        self.active = False
        self.stats = {
            'detections': 0,
            'actions': 0,
            'runtime': 0,
            'errors': 0
        }
    
    def start(self):
        self.active = True
        self.start_time = time.time()
    
    def stop(self):
        self.active = False
        if hasattr(self, 'start_time'):
            self.stats['runtime'] = time.time() - self.start_time
    
    def detect_signal(self, colors):
        """Override this method in specific bots"""
        return False
    
    def execute_action(self):
        """Override this method in specific bots"""
        pass

class PurpleTriggerBot(TradingBot):
    """Purple color detection bot"""
    def __init__(self):
        super().__init__(
            name="Purple Trigger Bot",
            description="Detects purple colors and triggers actions",
            target_color=[128, 0, 128],
            tolerance=0.6
        )
    
    def detect_signal(self, colors):
        for color in colors:
            if color and self.calculate_similarity(color, self.target_color) >= self.tolerance:
                return True
        return False
    
    def calculate_similarity(self, color1, color2):
        diff_squared = sum((a - b) ** 2 for a, b in zip(color1, color2))
        distance = math.sqrt(diff_squared)
        max_distance = math.sqrt(3 * (255 ** 2))
        return 1.0 - (distance / max_distance)

class GreenTriggerBot(TradingBot):
    """Green color detection bot"""
    def __init__(self):
        super().__init__(
            name="Green Trigger Bot",
            description="Detects green colors for buy signals",
            target_color=[0, 255, 0],
            tolerance=0.7
        )
    
    def detect_signal(self, colors):
        green_count = 0
        for color in colors:
            if color and color[1] > 200 and color[0] < 100 and color[2] < 100:
                green_count += 1
        return green_count >= 3

class RedTriggerBot(TradingBot):
    """Red color detection bot"""
    def __init__(self):
        super().__init__(
            name="Red Trigger Bot",
            description="Detects red colors for sell signals",
            target_color=[255, 0, 0],
            tolerance=0.7
        )
    
    def detect_signal(self, colors):
        red_count = 0
        for color in colors:
            if color and color[0] > 200 and color[1] < 100 and color[2] < 100:
                red_count += 1
        return red_count >= 3

class BlueTriggerBot(TradingBot):
    """Blue color detection bot"""
    def __init__(self):
        super().__init__(
            name="Blue Trigger Bot",
            description="Detects blue colors for neutral signals",
            target_color=[0, 0, 255],
            tolerance=0.6
        )
    
    def detect_signal(self, colors):
        for color in colors:
            if color and color[2] > 180 and color[0] < 100 and color[1] < 100:
                return True
        return False

class MultiColorBot(TradingBot):
    """Multi-color pattern detection bot"""
    def __init__(self):
        super().__init__(
            name="Multi-Color Pattern Bot",
            description="Detects complex color patterns",
            target_color=[128, 128, 128],
            tolerance=0.5
        )
    
    def detect_signal(self, colors):
        # Look for specific color patterns
        if len(colors) >= 9:
            # Check for alternating pattern
            pattern_detected = False
            for i in range(0, len(colors)-2, 3):
                if (colors[i] and colors[i][0] > 150 and  # Red-ish
                    colors[i+1] and colors[i+1][1] > 150 and  # Green-ish
                    colors[i+2] and colors[i+2][2] > 150):  # Blue-ish
                    pattern_detected = True
                    break
            return pattern_detected
        return False

class UnifiedTradingBotApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Unified Trading Bot Manager - Hardware Click Edition")
        self.root.geometry("700x850")
        self.root.resizable(False, False)
        
        # Initialize hardware click simulator
        self.hardware_clicker = HardwareClickSimulator()
        
        # Initialize bots
        self.bots = {
            'purple': PurpleTriggerBot(),
            'green': GreenTriggerBot(),
            'red': RedTriggerBot(),
            'blue': BlueTriggerBot(),
            'multicolor': MultiColorBot()
        }
        
        self.current_bot = None
        self.detection_active = False
        self.detection_thread = None
        self.running = False
        
        # Screen setup
        try:
            self.screen_width = user32.GetSystemMetrics(0)
            self.screen_height = user32.GetSystemMetrics(1)
            self.center_x = self.screen_width // 2
            self.center_y = self.screen_height // 2
        except Exception as e:
            self.screen_width = 1920
            self.screen_height = 1080
            self.center_x = 960
            self.center_y = 540
        
        # 9 central pixels
        self.pixel_offsets = [
            (-1, -1), (0, -1), (1, -1),
            (-1,  0), (0,  0), (1,  0),
            (-1,  1), (0,  1), (1,  1)
        ]
        
        # Configuration
        self.scan_interval = tk.DoubleVar(value=50.0)  # 50ms
        self.action_cooldown = tk.DoubleVar(value=200.0)  # 200ms
        self.click_method = tk.StringVar(value="advanced")  # Hardware click method
        
        # Device context
        self.hdc = None
        
        self.setup_gui()
        self.update_display()
        
    def setup_gui(self):
        """Setup the main GUI"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Unified Trading Bot Manager - Hardware Click Edition", 
                               font=("Arial", 16, "bold"), foreground="blue")
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Bot Selection Section
        self.setup_bot_selection_section(main_frame, row=1)
        
        # Status Section
        self.setup_status_section(main_frame, row=2)
        
        # Hardware Click Section
        self.setup_hardware_click_section(main_frame, row=3)
        
        # Parameters Section
        self.setup_parameters_section(main_frame, row=4)
        
        # Control Section
        self.setup_control_section(main_frame, row=5)
        
        # Statistics Section
        self.setup_statistics_section(main_frame, row=6)
        
        # Log Section
        self.setup_log_section(main_frame, row=7)
        
    def setup_bot_selection_section(self, parent, row):
        """Setup bot selection interface"""
        selection_frame = ttk.LabelFrame(parent, text="Trading Bot Selection", padding="10")
        selection_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Bot selection dropdown
        ttk.Label(selection_frame, text="Select Trading Bot:").grid(row=0, column=0, sticky=tk.W)
        
        self.bot_var = tk.StringVar()
        self.bot_combo = ttk.Combobox(selection_frame, textvariable=self.bot_var, 
                                     values=list(self.bots.keys()), state="readonly", width=20)
        self.bot_combo.grid(row=0, column=1, padx=(10, 0), sticky=tk.W)
        self.bot_combo.bind('<<ComboboxSelected>>', self.on_bot_selected)
        
        # Bot description
        self.bot_description = ttk.Label(selection_frame, text="Select a bot to see description", 
                                        wraplength=400, foreground="gray")
        self.bot_description.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(10, 0))
        
        # Quick selection buttons
        button_frame = ttk.Frame(selection_frame)
        button_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        for i, (key, bot) in enumerate(self.bots.items()):
            btn = ttk.Button(button_frame, text=bot.name.split()[0], 
                           command=lambda k=key: self.quick_select_bot(k), width=12)
            btn.grid(row=0, column=i, padx=(0, 5))
    
    def setup_hardware_click_section(self, parent, row):
        """Setup hardware click method selection"""
        hardware_frame = ttk.LabelFrame(parent, text="🔧 Hardware Click Simulation", padding="10")
        hardware_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Method selection
        ttk.Label(hardware_frame, text="Click Method:").grid(row=0, column=0, sticky=tk.W)
        
        method_combo = ttk.Combobox(hardware_frame, textvariable=self.click_method, 
                                   values=["advanced", "raw_input", "direct_injection", "timing_simulation", "standard"], 
                                   state="readonly", width=20)
        method_combo.grid(row=0, column=1, padx=(10, 0), sticky=tk.W)
        
        # Test hardware click button
        ttk.Button(hardware_frame, text="Test Hardware Click", 
                  command=self.test_hardware_click).grid(row=0, column=2, padx=(10, 0))
        
        # Method descriptions
        method_descriptions = {
            "advanced": "🚀 Advanced: Micro-movements + variable timing",
            "raw_input": "⚡ Raw Input: Direct input device simulation",
            "direct_injection": "🎯 Direct: Message injection to window",
            "timing_simulation": "⏱️ Timing: Electrical signal simulation",
            "standard": "📱 Standard: Basic click (fallback)"
        }
        
        self.method_description = ttk.Label(hardware_frame, 
                                           text=method_descriptions.get(self.click_method.get(), ""),
                                           foreground="green")
        self.method_description.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(5, 0))
        
        # Update description when method changes
        method_combo.bind('<<ComboboxSelected>>', 
                         lambda e: self.method_description.configure(
                             text=method_descriptions.get(self.click_method.get(), "")))
        
    def setup_status_section(self, parent, row):
        """Setup status display"""
        status_frame = ttk.LabelFrame(parent, text="System Status", padding="10")
        status_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status indicator
        self.status_canvas = tk.Canvas(status_frame, width=20, height=20)
        self.status_canvas.grid(row=0, column=0, padx=(0, 10))
        self.status_indicator = self.status_canvas.create_oval(2, 2, 18, 18, fill="red")
        
        self.status_label = ttk.Label(status_frame, text="INACTIVE", 
                                     font=("Arial", 12, "bold"), foreground="red")
        self.status_label.grid(row=0, column=1, sticky=tk.W)
        
        # Current bot info
        self.current_bot_label = ttk.Label(status_frame, text="No bot selected", 
                                          font=("Arial", 10), foreground="gray")
        self.current_bot_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
        # Screen info
        screen_info = ttk.Label(status_frame, 
                               text=f"Screen: {self.screen_width}x{self.screen_height} | Center: ({self.center_x}, {self.center_y})")
        screen_info.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(2, 0))
        
    def setup_parameters_section(self, parent, row):
        """Setup parameter controls"""
        params_frame = ttk.LabelFrame(parent, text="Detection Parameters", padding="10")
        params_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Scan interval
        ttk.Label(params_frame, text="Scan Interval (ms):").grid(row=0, column=0, sticky=tk.W)
        scan_spinbox = ttk.Spinbox(params_frame, from_=10.0, to=1000.0, width=10, 
                                  textvariable=self.scan_interval, increment=10.0)
        scan_spinbox.grid(row=0, column=1, padx=(10, 0), sticky=tk.W)
        
        # Action cooldown
        ttk.Label(params_frame, text="Action Cooldown (ms):").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        cooldown_spinbox = ttk.Spinbox(params_frame, from_=50.0, to=2000.0, width=10,
                                      textvariable=self.action_cooldown, increment=50.0)
        cooldown_spinbox.grid(row=1, column=1, padx=(10, 0), sticky=tk.W, pady=(5, 0))
        
    def setup_control_section(self, parent, row):
        """Setup control buttons"""
        controls_frame = ttk.LabelFrame(parent, text="Bot Controls", padding="10")
        controls_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Main control buttons
        self.start_button = ttk.Button(controls_frame, text="START TRADING BOT", 
                                      command=self.start_bot, state="disabled")
        self.start_button.grid(row=0, column=0, padx=(0, 10))
        
        self.stop_button = ttk.Button(controls_frame, text="STOP BOT", 
                                     command=self.stop_bot, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=(0, 10))
        
        # Emergency stop
        self.emergency_button = ttk.Button(controls_frame, text="EMERGENCY STOP", 
                                          command=self.emergency_stop, 
                                          style="Emergency.TButton")
        self.emergency_button.grid(row=0, column=2, padx=(0, 10))
        
        # Configuration buttons
        ttk.Button(controls_frame, text="Save Config", 
                  command=self.save_config).grid(row=1, column=0, pady=(10, 0))
        ttk.Button(controls_frame, text="Load Config", 
                  command=self.load_config).grid(row=1, column=1, pady=(10, 0))
        ttk.Button(controls_frame, text="Reset Stats", 
                  command=self.reset_stats).grid(row=1, column=2, pady=(10, 0))
        
        # Configure emergency button style
        style = ttk.Style()
        style.configure("Emergency.TButton", foreground="red")
        
    def setup_statistics_section(self, parent, row):
        """Setup statistics display"""
        stats_frame = ttk.LabelFrame(parent, text="Performance Statistics", padding="10")
        stats_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Statistics labels
        self.stats_labels = {
            'runtime': ttk.Label(stats_frame, text="Runtime: 0s"),
            'detections': ttk.Label(stats_frame, text="Detections: 0"),
            'actions': ttk.Label(stats_frame, text="Actions: 0"),
            'errors': ttk.Label(stats_frame, text="Errors: 0"),
            'success_rate': ttk.Label(stats_frame, text="Success Rate: 0%"),
            'avg_response': ttk.Label(stats_frame, text="Avg Response: 0ms"),
            'click_method': ttk.Label(stats_frame, text="Click Method: Hardware", foreground="green")
        }
        
        row_idx = 0
        for key, label in self.stats_labels.items():
            col = row_idx % 3
            row_pos = row_idx // 3
            label.grid(row=row_pos, column=col, sticky=tk.W, padx=(0, 20))
            row_idx += 1
            
    def setup_log_section(self, parent, row):
        """Setup activity log"""
        log_frame = ttk.LabelFrame(parent, text="Activity Log", padding="10")
        log_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Log text widget with scrollbar
        log_text_frame = ttk.Frame(log_frame)
        log_text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.log_text = tk.Text(log_text_frame, height=8, width=80, wrap=tk.WORD)
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
    
    def test_hardware_click(self):
        """Test the selected hardware click method"""
        method = self.click_method.get()
        self.log(f"Testing hardware click method: {method}")
        
        try:
            success = self.hardware_clicker.simulate_hardware_click(method)
            if success:
                self.log(f"✓ Hardware click test successful ({method})")
                messagebox.showinfo("Test Success", f"Hardware click method '{method}' working correctly!")
            else:
                self.log(f"✗ Hardware click test failed ({method})")
                messagebox.showwarning("Test Failed", f"Hardware click method '{method}' failed!")
        except Exception as e:
            self.log(f"✗ Hardware click test error: {e}")
            messagebox.showerror("Test Error", f"Error testing hardware click: {e}")
        
    def on_bot_selected(self, event=None):
        """Handle bot selection from dropdown"""
        selected = self.bot_var.get()
        if selected in self.bots:
            self.select_bot(selected)
    
    def quick_select_bot(self, bot_key):
        """Quick select bot from buttons"""
        self.bot_var.set(bot_key)
        self.select_bot(bot_key)
    
    def select_bot(self, bot_key):
        """Select and configure a trading bot"""
        if self.detection_active:
            if not messagebox.askyesno("Switch Bot", 
                                     "A bot is currently running. Stop it and switch to the new bot?"):
                return
            self.stop_bot()
        
        self.current_bot = self.bots[bot_key]
        self.bot_description.configure(text=self.current_bot.description)
        self.current_bot_label.configure(text=f"Selected: {self.current_bot.name}")
        
        # Enable start button
        self.start_button.configure(state="normal")
        
        self.log(f"Selected bot: {self.current_bot.name}")
    
    def start_bot(self):
        """Start the selected trading bot"""
        if not self.current_bot:
            messagebox.showerror("Error", "Please select a trading bot first")
            return
        
        try:
            # Get device context
            self.hdc = user32.GetDC(0)
            if not self.hdc:
                self.log("Warning: Could not get device context")
            
            self.detection_active = True
            self.running = True
            self.current_bot.start()
            
            # Update UI
            self.status_canvas.itemconfig(self.status_indicator, fill="green")
            self.status_label.configure(text="ACTIVE", foreground="green")
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            
            # Start detection thread
            self.detection_thread = threading.Thread(target=self.detection_loop, daemon=True)
            self.detection_thread.start()
            
            self.log(f"Started {self.current_bot.name} with hardware click method: {self.click_method.get()}")
            
        except Exception as e:
            self.log(f"Error starting bot: {e}")
            messagebox.showerror("Error", f"Failed to start bot: {e}")
    
    def stop_bot(self):
        """Stop the current trading bot"""
        self.detection_active = False
        self.running = False
        
        if self.current_bot:
            self.current_bot.stop()
        
        # Release device context
        if self.hdc:
            try:
                user32.ReleaseDC(0, self.hdc)
            except:
                pass
            finally:
                self.hdc = None
        
        # Update UI
        self.status_canvas.itemconfig(self.status_indicator, fill="red")
        self.status_label.configure(text="INACTIVE", foreground="red")
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        
        self.log("Trading bot stopped")
    
    def emergency_stop(self):
        """Emergency stop all operations"""
        self.log("EMERGENCY STOP ACTIVATED!")
        self.stop_bot()
        messagebox.showwarning("Emergency Stop", "All trading bot operations have been stopped!")
    
    def detection_loop(self):
        """Main detection loop"""
        last_action_time = 0
        
        while self.running and self.detection_active:
            try:
                # Scan pixels
                colors = self.scan_pixels()
                
                # Check for signal with current bot
                if self.current_bot and self.current_bot.detect_signal(colors):
                    self.current_bot.stats['detections'] += 1
                    
                    # Execute action if cooldown passed
                    current_time = time.time()
                    if current_time - last_action_time >= (self.action_cooldown.get() / 1000.0):
                        if self.execute_hardware_trading_action():
                            last_action_time = current_time
                            self.current_bot.stats['actions'] += 1
                
                # Sleep
                time.sleep(self.scan_interval.get() / 1000.0)
                
            except Exception as e:
                if self.current_bot:
                    self.current_bot.stats['errors'] += 1
                self.log(f"Detection error: {e}")
                time.sleep(0.1)
    
    def scan_pixels(self):
        """Scan the 9 central pixels"""
        colors = []
        
        for offset_x, offset_y in self.pixel_offsets:
            pixel_x = self.center_x + offset_x
            pixel_y = self.center_y + offset_y
            
            if 0 <= pixel_x < self.screen_width and 0 <= pixel_y < self.screen_height:
                color = self.get_pixel_color(pixel_x, pixel_y)
                colors.append(color)
        
        return colors
    
    def get_pixel_color(self, x, y):
        """Get pixel color safely"""
        try:
            if not self.hdc:
                return None
                
            color_ref = gdi32.GetPixel(self.hdc, x, y)
            if color_ref == 0xFFFFFFFF:
                return None
                
            r = color_ref & 0xFF
            g = (color_ref >> 8) & 0xFF
            b = (color_ref >> 16) & 0xFF
            
            return (r, g, b)
        except:
            return None
    
    def execute_hardware_trading_action(self):
        """Execute hardware-simulated trading action"""
        try:
            method = self.click_method.get()
            success = self.hardware_clicker.simulate_hardware_click(method)
            
            if success:
                self.log(f"Hardware trading action executed by {self.current_bot.name} (method: {method})")
                return True
            else:
                self.log(f"Hardware action failed for {self.current_bot.name}")
                return False
            
        except Exception as e:
            self.log(f"Hardware action execution error: {e}")
            return False
    
    def update_display(self):
        """Update statistics display"""
        if self.current_bot and self.detection_active:
            bot = self.current_bot
            
            # Calculate success rate
            total_actions = bot.stats['detections'] + bot.stats['errors']
            success_rate = (bot.stats['actions'] / total_actions * 100) if total_actions > 0 else 0
            
            # Update labels
            self.stats_labels['runtime'].configure(text=f"Runtime: {bot.stats['runtime']:.1f}s")
            self.stats_labels['detections'].configure(text=f"Detections: {bot.stats['detections']}")
            self.stats_labels['actions'].configure(text=f"Actions: {bot.stats['actions']}")
            self.stats_labels['errors'].configure(text=f"Errors: {bot.stats['errors']}")
            self.stats_labels['success_rate'].configure(text=f"Success Rate: {success_rate:.1f}%")
            self.stats_labels['avg_response'].configure(text=f"Avg Response: {self.scan_interval.get():.0f}ms")
            self.stats_labels['click_method'].configure(text=f"Click Method: {self.click_method.get()}")
        
        # Schedule next update
        self.root.after(500, self.update_display)
    
    def log(self, message):
        """Add message to activity log"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        self.root.after(0, self._update_log, log_message)
    
    def _update_log(self, message):
        """Update log text widget"""
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)
        
        # Limit log size
        lines = self.log_text.index(tk.END).split('.')[0]
        if int(lines) > 100:
            self.log_text.delete('1.0', '20.0')
    
    def reset_stats(self):
        """Reset all statistics"""
        for bot in self.bots.values():
            bot.stats = {
                'detections': 0,
                'actions': 0,
                'runtime': 0,
                'errors': 0
            }
        self.log("All statistics reset")
    
    def save_config(self):
        """Save configuration"""
        config = {
            'scan_interval': self.scan_interval.get(),
            'action_cooldown': self.action_cooldown.get(),
            'current_bot': self.bot_var.get() if self.current_bot else None,
            'click_method': self.click_method.get()
        }
        
        try:
            with open('trading_bot_config.json', 'w') as f:
                json.dump(config, f, indent=2)
            self.log("Configuration saved")
            messagebox.showinfo("Success", "Configuration saved successfully")
        except Exception as e:
            self.log(f"Error saving config: {e}")
            messagebox.showerror("Error", f"Failed to save configuration: {e}")
    
    def load_config(self):
        """Load configuration"""
        try:
            if os.path.exists('trading_bot_config.json'):
                with open('trading_bot_config.json', 'r') as f:
                    config = json.load(f)
                
                self.scan_interval.set(config.get('scan_interval', 50.0))
                self.action_cooldown.set(config.get('action_cooldown', 200.0))
                self.click_method.set(config.get('click_method', 'advanced'))
                
                if config.get('current_bot'):
                    self.bot_var.set(config['current_bot'])
                    self.select_bot(config['current_bot'])
                
                self.log("Configuration loaded")
            else:
                self.log("No configuration file found")
        except Exception as e:
            self.log(f"Error loading config: {e}")
    
    def on_closing(self):
        """Handle application closing"""
        if self.detection_active:
            self.stop_bot()
        self.root.destroy()
    
    def run(self):
        """Start the application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.log("Unified Trading Bot Manager started with Hardware Click Simulation")
        self.log("Select a trading bot and configure hardware click method to begin")
        self.root.mainloop()

if __name__ == "__main__":
    app = UnifiedTradingBotApp()
    app.run()