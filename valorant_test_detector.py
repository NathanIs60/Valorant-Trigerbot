import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import json
import os
from PIL import ImageGrab
import numpy as np
import cv2
import math
from collections import deque
import datetime

class ValorantTestDetector:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Valorant Test Detector - Eğitim Amaçlı")
        self.root.geometry("600x800")
        self.root.resizable(False, False)
        
        # Uyarı mesajı
        self.show_warning()
        
        # Detection engine variables
        self.detection_active = False
        self.detection_thread = None
        self.running = False
        
        # Screen setup
        self.screen_width = 1920
        self.screen_height = 1080
        self.center_x = self.screen_width // 2
        self.center_y = self.screen_height // 2
        
        # Detection area (crosshair bölgesi)
        self.detection_size = 20  # 20x20 pixel alan
        
        # Configuration variables
        self.target_color = [255, 0, 255]  # Magenta (test için)
        self.tolerance = tk.DoubleVar(value=0.8)  # 80%
        self.scan_interval = tk.DoubleVar(value=100.0)  # 100ms
        self.detection_method = tk.StringVar(value="screenshot")
        
        # Statistics
        self.stats = {
            'detections': 0,
            'scans': 0,
            'runtime': 0,
            'avg_scan_time': 0.0,
            'scan_times': deque(maxlen=100)
        }
        
        self.setup_gui()
        self.update_display()
        
    def show_warning(self):
        """Uyarı mesajı göster"""
        warning_msg = """
⚠️ ÖNEMLİ UYARI ⚠️

Bu program sadece EĞİTİM ve TEST amaçlıdır.

Valorant gibi anti-cheat sistemli oyunlarda:
• Vanguard tarafından tespit edilebilir
• Hesap banına neden olabilir
• Oyun içinde çalışmayabilir

Sadece test ortamlarında kullanın!
Sorumluluk kullanıcıya aittir.
        """
        messagebox.showwarning("Önemli Uyarı", warning_msg)
        
    def setup_gui(self):
        """GUI kurulumu"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Valorant Test Detector - EĞİTİM AMAÇLI", 
                               font=("Arial", 16, "bold"), foreground="red")
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Warning section
        self.setup_warning_section(main_frame, row=1)
        
        # Status Section
        self.setup_status_section(main_frame, row=2)
        
        # Method Selection
        self.setup_method_section(main_frame, row=3)
        
        # Color Configuration Section
        self.setup_color_section(main_frame, row=4)
        
        # Detection Parameters Section
        self.setup_parameters_section(main_frame, row=5)
        
        # Control Buttons Section
        self.setup_controls_section(main_frame, row=6)
        
        # Statistics Section
        self.setup_statistics_section(main_frame, row=7)
        
        # Log Section
        self.setup_log_section(main_frame, row=8)
        
    def setup_warning_section(self, parent, row):
        """Uyarı bölümü"""
        warning_frame = ttk.LabelFrame(parent, text="⚠️ UYARI", padding="10")
        warning_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        warning_text = """Bu program Valorant'da ÇALIŞMAZ!
Vanguard anti-cheat sistemi tarafından engellenir.
Sadece test ve eğitim amaçlı kullanın."""
        
        warning_label = ttk.Label(warning_frame, text=warning_text, 
                                 foreground="red", font=("Arial", 10, "bold"))
        warning_label.grid(row=0, column=0, sticky=tk.W)
        
    def setup_status_section(self, parent, row):
        """Status bölümü"""
        status_frame = ttk.LabelFrame(parent, text="Durum", padding="10")
        status_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status indicator
        self.status_canvas = tk.Canvas(status_frame, width=20, height=20)
        self.status_canvas.grid(row=0, column=0, padx=(0, 10))
        self.status_indicator = self.status_canvas.create_oval(2, 2, 18, 18, fill="red")
        
        self.status_label = ttk.Label(status_frame, text="INACTIVE", 
                                     font=("Arial", 12, "bold"), foreground="red")
        self.status_label.grid(row=0, column=1, sticky=tk.W)
        
        # Detection area info
        area_info = ttk.Label(status_frame, 
                             text=f"Algılama Alanı: {self.detection_size}x{self.detection_size} pixel (merkez)")
        area_info.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
    def setup_method_section(self, parent, row):
        """Algılama yöntemi seçimi"""
        method_frame = ttk.LabelFrame(parent, text="Algılama Yöntemi", padding="10")
        method_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Method selection
        ttk.Label(method_frame, text="Yöntem:").grid(row=0, column=0, sticky=tk.W)
        
        method_combo = ttk.Combobox(method_frame, textvariable=self.detection_method, 
                                   values=["screenshot", "opencv"], state="readonly")
        method_combo.grid(row=0, column=1, padx=(10, 0), sticky=tk.W)
        
        # Method descriptions
        desc_text = """
screenshot: PIL ile ekran görüntüsü (daha güvenli)
opencv: OpenCV ile görüntü işleme (daha hızlı)
        """
        ttk.Label(method_frame, text=desc_text, font=("Arial", 8)).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
    def setup_color_section(self, parent, row):
        """Renk konfigürasyonu"""
        color_frame = ttk.LabelFrame(parent, text="Renk Konfigürasyonu", padding="10")
        color_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Current color display
        ttk.Label(color_frame, text="Hedef Renk:").grid(row=0, column=0, sticky=tk.W)
        
        self.color_canvas = tk.Canvas(color_frame, width=50, height=30, bg="magenta")
        self.color_canvas.grid(row=0, column=1, padx=(10, 10))
        
        self.color_label = ttk.Label(color_frame, text=f"RGB({self.target_color[0]}, {self.target_color[1]}, {self.target_color[2]})")
        self.color_label.grid(row=0, column=2, sticky=tk.W)
        
        # Tolerance slider
        ttk.Label(color_frame, text="Tolerans:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        tolerance_frame = ttk.Frame(color_frame)
        tolerance_frame.grid(row=1, column=1, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.tolerance_scale = ttk.Scale(tolerance_frame, from_=0.1, to=1.0, 
                                        variable=self.tolerance, orient=tk.HORIZONTAL, length=200)
        self.tolerance_scale.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.tolerance_value_label = ttk.Label(tolerance_frame, text=f"{self.tolerance.get()*100:.0f}%")
        self.tolerance_value_label.grid(row=0, column=1, padx=(10, 0))
        
        self.tolerance.trace('w', self.update_tolerance_display)
        
    def setup_parameters_section(self, parent, row):
        """Parametreler"""
        params_frame = ttk.LabelFrame(parent, text="Parametreler", padding="10")
        params_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Scan interval
        ttk.Label(params_frame, text="Tarama Aralığı (ms):").grid(row=0, column=0, sticky=tk.W)
        scan_spinbox = ttk.Spinbox(params_frame, from_=50.0, to=1000.0, width=10, 
                                  textvariable=self.scan_interval, increment=10.0)
        scan_spinbox.grid(row=0, column=1, padx=(10, 0), sticky=tk.W)
        ttk.Label(params_frame, text="(Önerilen: 100-500ms)").grid(row=0, column=2, padx=(10, 0), sticky=tk.W)
        
    def setup_controls_section(self, parent, row):
        """Kontrol butonları"""
        controls_frame = ttk.LabelFrame(parent, text="Kontroller", padding="10")
        controls_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Start/Stop button
        self.start_stop_button = ttk.Button(controls_frame, text="TEST BAŞLAT", 
                                           command=self.toggle_detection)
        self.start_stop_button.grid(row=0, column=0, padx=(0, 10))
        
        # Test area button
        ttk.Button(controls_frame, text="Test Alanı Göster", 
                  command=self.show_test_area).grid(row=0, column=1, padx=(0, 10))
        
        # Reset stats button
        ttk.Button(controls_frame, text="İstatistikleri Sıfırla", 
                  command=self.reset_stats).grid(row=0, column=2)
        
    def setup_statistics_section(self, parent, row):
        """İstatistikler"""
        stats_frame = ttk.LabelFrame(parent, text="İstatistikler", padding="10")
        stats_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.stats_labels = {
            'runtime': ttk.Label(stats_frame, text="Çalışma Süresi: 0s"),
            'scans': ttk.Label(stats_frame, text="Tarama: 0"),
            'detections': ttk.Label(stats_frame, text="Algılama: 0"),
            'scan_time': ttk.Label(stats_frame, text="Ort. Tarama: 0.0ms")
        }
        
        row_idx = 0
        for key, label in self.stats_labels.items():
            col = row_idx % 2
            row_pos = row_idx // 2
            label.grid(row=row_pos, column=col, sticky=tk.W, padx=(0, 20))
            row_idx += 1
            
    def setup_log_section(self, parent, row):
        """Log bölümü"""
        log_frame = ttk.LabelFrame(parent, text="Aktivite Logu", padding="10")
        log_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        log_text_frame = ttk.Frame(log_frame)
        log_text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.log_text = tk.Text(log_text_frame, height=8, width=70, wrap=tk.WORD)
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
        
    def update_tolerance_display(self, *args):
        """Tolerans gösterimini güncelle"""
        self.tolerance_value_label.configure(text=f"{self.tolerance.get()*100:.0f}%")
        
    def show_test_area(self):
        """Test alanını göster"""
        test_window = tk.Toplevel(self.root)
        test_window.title("Test Alanı")
        test_window.geometry("300x300")
        test_window.configure(bg="black")
        
        # Test rengi göster
        test_canvas = tk.Canvas(test_window, width=280, height=280, bg="black")
        test_canvas.pack(padx=10, pady=10)
        
        # Merkez kare
        color_hex = f"#{self.target_color[0]:02x}{self.target_color[1]:02x}{self.target_color[2]:02x}"
        test_canvas.create_rectangle(130, 130, 150, 150, fill=color_hex, outline="white")
        test_canvas.create_text(140, 160, text="Test Rengi", fill="white")
        
        self.log("Test alanı açıldı - Bu rengi algılamaya çalışacak")
        
    def toggle_detection(self):
        """Algılamayı başlat/durdur"""
        if not self.detection_active:
            self.start_detection()
        else:
            self.stop_detection()
            
    def start_detection(self):
        """Algılamayı başlat"""
        try:
            self.log("Test algılama başlatılıyor...")
            
            # Valorant kontrolü
            if self.is_valorant_running():
                messagebox.showwarning("Uyarı", 
                    "Valorant çalışıyor! Bu program Valorant'da çalışmaz.\n"
                    "Vanguard anti-cheat sistemi tarafından engellenir.")
                return
            
            self.detection_active = True
            self.running = True
            self.start_time = time.time()
            
            # Update UI
            self.status_canvas.itemconfig(self.status_indicator, fill="green")
            self.status_label.configure(text="TEST AKTIF", foreground="green")
            self.start_stop_button.configure(text="TEST DURDUR")
            
            # Start detection thread
            self.detection_thread = threading.Thread(target=self.detection_loop, daemon=True)
            self.detection_thread.start()
            
            self.log("Test algılama başlatıldı")
            
        except Exception as e:
            self.log(f"Başlatma hatası: {e}")
            
    def stop_detection(self):
        """Algılamayı durdur"""
        self.log("Test algılama durduruluyor...")
        self.detection_active = False
        self.running = False
        
        # Update UI
        self.status_canvas.itemconfig(self.status_indicator, fill="red")
        self.status_label.configure(text="INACTIVE", foreground="red")
        self.start_stop_button.configure(text="TEST BAŞLAT")
        
        self.log("Test algılama durduruldu")
        
    def is_valorant_running(self):
        """Valorant çalışıyor mu kontrol et"""
        try:
            import psutil
            for proc in psutil.process_iter(['name']):
                if 'valorant' in proc.info['name'].lower():
                    return True
        except:
            pass
        return False
        
    def detection_loop(self):
        """Ana algılama döngüsü"""
        while self.running:
            try:
                scan_start = time.time()
                
                # Screenshot al
                detected = self.scan_area()
                
                scan_time = time.time() - scan_start
                self.stats['scan_times'].append(scan_time)
                self.stats['scans'] += 1
                
                if detected:
                    self.stats['detections'] += 1
                    self.log(f"Hedef renk algılandı! (Toplam: {self.stats['detections']})")
                
                # Sleep
                time.sleep(self.scan_interval.get() / 1000.0)
                
            except Exception as e:
                self.log(f"Algılama hatası: {e}")
                time.sleep(0.1)
                
    def scan_area(self):
        """Merkez alanı tara"""
        try:
            if self.detection_method.get() == "screenshot":
                return self.scan_with_screenshot()
            else:
                return self.scan_with_opencv()
        except Exception as e:
            self.log(f"Tarama hatası: {e}")
            return False
            
    def scan_with_screenshot(self):
        """PIL ile tarama"""
        try:
            # Merkez alanın koordinatları
            left = self.center_x - self.detection_size // 2
            top = self.center_y - self.detection_size // 2
            right = left + self.detection_size
            bottom = top + self.detection_size
            
            # Screenshot al
            screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
            
            # Numpy array'e çevir
            img_array = np.array(screenshot)
            
            # Hedef rengi ara
            return self.find_target_color(img_array)
            
        except Exception as e:
            self.log(f"Screenshot hatası: {e}")
            return False
            
    def scan_with_opencv(self):
        """OpenCV ile tarama"""
        try:
            # Bu yöntem daha gelişmiş ama daha riskli
            # Valorant'da kesinlikle çalışmaz
            screenshot = ImageGrab.grab()
            img_array = np.array(screenshot)
            
            # BGR'ye çevir (OpenCV için)
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            # Merkez alanı kes
            h, w = img_bgr.shape[:2]
            center_x, center_y = w // 2, h // 2
            
            roi = img_bgr[center_y - self.detection_size//2:center_y + self.detection_size//2,
                         center_x - self.detection_size//2:center_x + self.detection_size//2]
            
            return self.find_target_color_opencv(roi)
            
        except Exception as e:
            self.log(f"OpenCV hatası: {e}")
            return False
            
    def find_target_color(self, img_array):
        """Hedef rengi bul (PIL yöntemi)"""
        try:
            target = np.array(self.target_color)
            
            # Her pixel için renk benzerliği hesapla
            for y in range(img_array.shape[0]):
                for x in range(img_array.shape[1]):
                    pixel = img_array[y, x, :3]  # RGB
                    
                    # Renk benzerliği hesapla
                    similarity = self.calculate_color_similarity(pixel, target)
                    
                    if similarity >= self.tolerance.get():
                        return True
                        
            return False
            
        except Exception as e:
            self.log(f"Renk arama hatası: {e}")
            return False
            
    def find_target_color_opencv(self, roi):
        """OpenCV ile renk bulma"""
        try:
            # HSV'ye çevir
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            
            # Hedef rengin HSV değerlerini hesapla
            target_bgr = np.uint8([[self.target_color[::-1]]])  # RGB -> BGR
            target_hsv = cv2.cvtColor(target_bgr, cv2.COLOR_BGR2HSV)[0][0]
            
            # Renk aralığı belirle
            tolerance_val = int((1 - self.tolerance.get()) * 50)
            lower = np.array([max(0, target_hsv[0] - tolerance_val), 50, 50])
            upper = np.array([min(179, target_hsv[0] + tolerance_val), 255, 255])
            
            # Mask oluştur
            mask = cv2.inRange(hsv, lower, upper)
            
            # Eşleşme var mı kontrol et
            return np.any(mask > 0)
            
        except Exception as e:
            self.log(f"OpenCV renk arama hatası: {e}")
            return False
            
    def calculate_color_similarity(self, color1, color2):
        """Renk benzerliği hesapla"""
        try:
            diff_squared = np.sum((color1.astype(float) - color2.astype(float)) ** 2)
            distance = np.sqrt(diff_squared)
            max_distance = np.sqrt(3 * (255 ** 2))
            return 1.0 - (distance / max_distance)
        except:
            return 0.0
            
    def update_display(self):
        """Ekranı güncelle"""
        try:
            if self.detection_active:
                runtime = time.time() - self.start_time
                self.stats['runtime'] = runtime
                
                if self.stats['scan_times']:
                    avg_scan = sum(self.stats['scan_times']) / len(self.stats['scan_times'])
                    self.stats['avg_scan_time'] = avg_scan
                    
                self.stats_labels['runtime'].configure(text=f"Çalışma Süresi: {runtime:.1f}s")
                self.stats_labels['scans'].configure(text=f"Tarama: {self.stats['scans']}")
                self.stats_labels['detections'].configure(text=f"Algılama: {self.stats['detections']}")
                self.stats_labels['scan_time'].configure(text=f"Ort. Tarama: {self.stats['avg_scan_time']*1000:.2f}ms")
        except:
            pass
            
        self.root.after(500, self.update_display)
        
    def log(self, message):
        """Log mesajı ekle"""
        try:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            log_message = f"[{timestamp}] {message}\n"
            self.root.after(0, self._update_log, log_message)
        except:
            pass
        
    def _update_log(self, message):
        """Log widget'ını güncelle"""
        try:
            self.log_text.insert(tk.END, message)
            self.log_text.see(tk.END)
            
            lines = self.log_text.index(tk.END).split('.')[0]
            if int(lines) > 100:
                self.log_text.delete('1.0', '20.0')
        except:
            pass
            
    def reset_stats(self):
        """İstatistikleri sıfırla"""
        try:
            self.stats['detections'] = 0
            self.stats['scans'] = 0
            self.stats['scan_times'].clear()
            if hasattr(self, 'start_time'):
                self.start_time = time.time()
            self.log("İstatistikler sıfırlandı")
        except Exception as e:
            self.log(f"Sıfırlama hatası: {e}")
        
    def on_closing(self):
        """Uygulama kapanırken"""
        if self.detection_active:
            self.stop_detection()
        self.root.destroy()
        
    def run(self):
        """Uygulamayı başlat"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.log("Valorant Test Detector başlatıldı - Sadece test amaçlı!")
        self.log("UYARI: Bu program Valorant'da ÇALIŞMAZ!")
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = ValorantTestDetector()
        app.run()
    except Exception as e:
        print(f"Uygulama hatası: {e}")
        input("Çıkmak için Enter'a basın...")