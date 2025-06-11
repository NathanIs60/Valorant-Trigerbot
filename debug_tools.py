import tkinter as tk
from tkinter import ttk
import time
from ctypes import windll
import threading

class DebugTools:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Debug Araçları")
        self.root.geometry("400x500")
        
        # Windows API
        self.user32 = windll.user32
        self.gdi32 = windll.gdi32
        self.user32.SetProcessDPIAware()
        
        # Variables
        self.monitoring = False
        self.hdc = None
        
        self.setup_gui()
        
    def setup_gui(self):
        """GUI kurulumu"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(main_frame, text="Debug Araçları", 
                 font=("Arial", 16, "bold")).pack(pady=(0, 20))
        
        # Mouse position
        pos_frame = ttk.LabelFrame(main_frame, text="Mouse Pozisyonu", padding="10")
        pos_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.pos_label = ttk.Label(pos_frame, text="X: 0, Y: 0")
        self.pos_label.pack()
        
        # Pixel color
        color_frame = ttk.LabelFrame(main_frame, text="Pixel Rengi", padding="10")
        color_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.color_label = ttk.Label(color_frame, text="RGB(0, 0, 0)")
        self.color_label.pack()
        
        self.color_canvas = tk.Canvas(color_frame, width=50, height=30, bg="black")
        self.color_canvas.pack(pady=5)
        
        # Controls
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.monitor_button = ttk.Button(control_frame, text="İzlemeyi Başlat", 
                                        command=self.toggle_monitoring)
        self.monitor_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(control_frame, text="Tıklama Testi", 
                  command=self.test_click).pack(side=tk.LEFT)
        
        # Click test results
        test_frame = ttk.LabelFrame(main_frame, text="Tıklama Test Sonuçları", padding="10")
        test_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.test_text = tk.Text(test_frame, height=10, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(test_frame, orient=tk.VERTICAL, command=self.test_text.yview)
        self.test_text.configure(yscrollcommand=scrollbar.set)
        
        self.test_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Start monitoring
        self.update_info()
        
    def toggle_monitoring(self):
        """İzlemeyi başlat/durdur"""
        self.monitoring = not self.monitoring
        
        if self.monitoring:
            self.monitor_button.configure(text="İzlemeyi Durdur")
            self.hdc = self.user32.GetDC(0)
        else:
            self.monitor_button.configure(text="İzlemeyi Başlat")
            if self.hdc:
                self.user32.ReleaseDC(0, self.hdc)
                self.hdc = None
                
    def update_info(self):
        """Bilgileri güncelle"""
        try:
            # Mouse position
            point = wintypes.POINT()
            self.user32.GetCursorPos(byref(point))
            self.pos_label.configure(text=f"X: {point.x}, Y: {point.y}")
            
            # Pixel color if monitoring
            if self.monitoring and self.hdc:
                color_ref = self.gdi32.GetPixel(self.hdc, point.x, point.y)
                if color_ref != 0xFFFFFFFF:
                    r = color_ref & 0xFF
                    g = (color_ref >> 8) & 0xFF
                    b = (color_ref >> 16) & 0xFF
                    
                    self.color_label.configure(text=f"RGB({r}, {g}, {b})")
                    
                    # Update color canvas
                    color_hex = f"#{r:02x}{g:02x}{b:02x}"
                    self.color_canvas.configure(bg=color_hex)
                    
        except Exception as e:
            self.log_test(f"Güncelleme hatası: {e}")
            
        # Schedule next update
        self.root.after(50, self.update_info)
        
    def test_click(self):
        """Tıklama testleri"""
        self.log_test("=== Tıklama Testleri Başlıyor ===")
        
        # Test 1: mouse_event
        try:
            start_time = time.time()
            self.user32.mouse_event(0x0002, 0, 0, 0, 0)  # MOUSEEVENTF_LEFTDOWN
            time.sleep(0.001)
            self.user32.mouse_event(0x0004, 0, 0, 0, 0)  # MOUSEEVENTF_LEFTUP
            duration = time.time() - start_time
            self.log_test(f"✓ mouse_event: Başarılı ({duration*1000:.2f}ms)")
        except Exception as e:
            self.log_test(f"✗ mouse_event: Hata - {e}")
            
        time.sleep(0.1)
        
        # Test 2: SendMessage
        try:
            hwnd = self.user32.GetForegroundWindow()
            if hwnd:
                start_time = time.time()
                self.user32.SendMessageW(hwnd, 0x0201, 0x0001, 0)  # WM_LBUTTONDOWN
                time.sleep(0.001)
                self.user32.SendMessageW(hwnd, 0x0202, 0x0000, 0)  # WM_LBUTTONUP
                duration = time.time() - start_time
                self.log_test(f"✓ SendMessage: Başarılı ({duration*1000:.2f}ms)")
            else:
                self.log_test("✗ SendMessage: Pencere bulunamadı")
        except Exception as e:
            self.log_test(f"✗ SendMessage: Hata - {e}")
            
        time.sleep(0.1)
        
        # Test 3: PostMessage
        try:
            hwnd = self.user32.GetForegroundWindow()
            if hwnd:
                start_time = time.time()
                self.user32.PostMessageW(hwnd, 0x0201, 0x0001, 0)  # WM_LBUTTONDOWN
                time.sleep(0.001)
                self.user32.PostMessageW(hwnd, 0x0202, 0x0000, 0)  # WM_LBUTTONUP
                duration = time.time() - start_time
                self.log_test(f"✓ PostMessage: Başarılı ({duration*1000:.2f}ms)")
            else:
                self.log_test("✗ PostMessage: Pencere bulunamadı")
        except Exception as e:
            self.log_test(f"✗ PostMessage: Hata - {e}")
            
        self.log_test("=== Test Tamamlandı ===\n")
        
    def log_test(self, message):
        """Test sonucunu logla"""
        timestamp = time.strftime("%H:%M:%S")
        self.test_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.test_text.see(tk.END)
        
    def run(self):
        """Uygulamayı başlat"""
        self.root.mainloop()

if __name__ == "__main__":
    from ctypes import wintypes, byref
    app = DebugTools()
    app.run()