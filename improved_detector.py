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

class ImprovedDetector:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Geliştirilmiş Algılama Sistemi")
        self.root.geometry("600x800")
        self.root.resizable(False, False)
        
        # Detection engine variables
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
        
        # Geliştirilmiş pixel grid - daha hassas algılama
        self.pixel_grid = self.create_detection_grid()
        
        # Configuration variables
        self.target_color = [128, 0, 128]  # Purple RGB
        self.tolerance = tk.DoubleVar(value=0.4)  # Daha düşük tolerans
        self.scan_interval = tk.DoubleVar(value=50.0)  # 50ms
        self.click_cooldown = tk.DoubleVar(value=200.0)  # 200ms
        self.min_pixels_required = tk.IntVar(value=3)  # Minimum pixel sayısı
        
        # Click method selection
        self.click_method = tk.StringVar(value="mouse_event")
        
        # Statistics
        self.stats = {
            'detections': 0,
            'clicks': 0,
            'false_positives': 0,
            'runtime': 0,
            'avg_scan_time': 0.0,
            'scan_times': deque(maxlen=100),
            'color_samples': deque(maxlen=50)
        }
        
        # Device context
        self.hdc = None
        
        self.setup_gui()
        self.load_config()
        self.update_display()
        
    def create_detection_grid(self):
        """Geliştirilmiş algılama grid'i oluştur"""
        # 5x5 grid daha hassas algılama için
        grid = []
        for y in range(-2, 3):
            for x in range(-2, 3):
                # Merkez pixel'e daha fazla ağırlık ver
                weight = 1.0
                if x == 0 and y == 0:
                    weight = 2.0
                elif abs(x) <= 1 and abs(y) <= 1:
                    weight = 1.5
                    
                grid.append({
                    'offset': (x, y),
                    'weight': weight
                })
        return grid
        
    def setup_gui(self):
        """GUI kurulumu"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Geliştirilmiş Algılama Sistemi", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Status Section
        self.setup_status_section(main_frame, row=1)
        
        # Color Configuration Section
        self.setup_color_section(main_frame, row=2)
        
        # Advanced Parameters Section
        self.setup_advanced_parameters_section(main_frame, row=3)
        
        # Click Method Section
        self.setup_click_method_section(main_frame, row=4)
        
        # Control Buttons Section
        self.setup_controls_section(main_frame, row=5)
        
        # Statistics Section
        self.setup_statistics_section(main_frame, row=6)
        
        # Debug Section
        self.setup_debug_section(main_frame, row=7)
        
        # Log Section
        self.setup_log_section(main_frame, row=8)
        
    def setup_status_section(self, parent, row):
        """Status bölümü"""
        status_frame = ttk.LabelFrame(parent, text="Sistem Durumu", padding="10")
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
                               text=f"Ekran: {self.screen_width}x{self.screen_height} | Merkez: ({self.center_x}, {self.center_y})")
        screen_info.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
        # Grid info
        grid_info = ttk.Label(status_frame, 
                             text=f"Algılama Grid'i: 5x5 ({len(self.pixel_grid)} pixel)")
        grid_info.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(2, 0))
        
    def setup_color_section(self, parent, row):
        """Renk konfigürasyonu"""
        color_frame = ttk.LabelFrame(parent, text="Renk Konfigürasyonu", padding="10")
        color_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Current color display
        ttk.Label(color_frame, text="Hedef Renk:").grid(row=0, column=0, sticky=tk.W)
        
        self.color_canvas = tk.Canvas(color_frame, width=50, height=30, bg="purple")
        self.color_canvas.grid(row=0, column=1, padx=(10, 10))
        
        self.color_label = ttk.Label(color_frame, text=f"RGB({self.target_color[0]}, {self.target_color[1]}, {self.target_color[2]})")
        self.color_label.grid(row=0, column=2, sticky=tk.W)
        
        # Color picker button
        ttk.Button(color_frame, text="Renk Seç", command=self.choose_color).grid(row=0, column=3, padx=(10, 0))
        
        # Tolerance slider
        ttk.Label(color_frame, text="Tolerans:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        tolerance_frame = ttk.Frame(color_frame)
        tolerance_frame.grid(row=1, column=1, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.tolerance_scale = ttk.Scale(tolerance_frame, from_=0.1, to=0.8, 
                                        variable=self.tolerance, orient=tk.HORIZONTAL, length=200)
        self.tolerance_scale.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.tolerance_value_label = ttk.Label(tolerance_frame, text=f"{self.tolerance.get()*100:.0f}%")
        self.tolerance_value_label.grid(row=0, column=1, padx=(10, 0))
        
        self.tolerance.trace('w', self.update_tolerance_display)
        
    def setup_advanced_parameters_section(self, parent, row):
        """Gelişmiş parametreler"""
        params_frame = ttk.LabelFrame(parent, text="Gelişmiş Parametreler", padding="10")
        params_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Scan interval
        ttk.Label(params_frame, text="Tarama Aralığı (ms):").grid(row=0, column=0, sticky=tk.W)
        scan_spinbox = ttk.Spinbox(params_frame, from_=10.0, to=1000.0, width=10, 
                                  textvariable=self.scan_interval, increment=10.0)
        scan_spinbox.grid(row=0, column=1, padx=(10, 0), sticky=tk.W)
        
        # Click cooldown
        ttk.Label(params_frame, text="Tıklama Bekleme (ms):").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        cooldown_spinbox = ttk.Spinbox(params_frame, from_=50.0, to=2000.0, width=10,
                                      textvariable=self.click_cooldown, increment=50.0)
        cooldown_spinbox.grid(row=1, column=1, padx=(10, 0), sticky=tk.W, pady=(5, 0))
        
        # Minimum pixels required
        ttk.Label(params_frame, text="Min. Pixel Sayısı:").grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
        min_pixels_spinbox = ttk.Spinbox(params_frame, from_=1, to=10, width=10,
                                        textvariable=self.min_pixels_required, increment=1)
        min_pixels_spinbox.grid(row=2, column=1, padx=(10, 0), sticky=tk.W, pady=(5, 0))
        
    def setup_click_method_section(self, parent, row):
        """Tıklama yöntemi seçimi"""
        click_frame = ttk.LabelFrame(parent, text="Tıklama Yöntemi", padding="10")
        click_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Method selection
        ttk.Label(click_frame, text="Yöntem:").grid(row=0, column=0, sticky=tk.W)
        
        method_combo = ttk.Combobox(click_frame, textvariable=self.click_method, 
                                   values=["mouse_event", "sendmessage", "postmessage", "simulate"], 
                                   state="readonly")
        method_combo.grid(row=0, column=1, padx=(10, 0), sticky=tk.W)
        
        # Test click button
        ttk.Button(click_frame, text="Tıklama Testi", 
                  command=self.test_click).grid(row=0, column=2, padx=(10, 0))
        
    def setup_controls_section(self, parent, row):
        """Kontrol butonları"""
        controls_frame = ttk.LabelFrame(parent, text="Kontroller", padding="10")
        controls_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Start/Stop button
        self.start_stop_button = ttk.Button(controls_frame, text="ALGILAMA BAŞLAT", 
                                           command=self.toggle_detection)
        self.start_stop_button.grid(row=0, column=0, padx=(0, 10))
        
        # Calibrate button
        ttk.Button(controls_frame, text="Renk Kalibrasyonu", 
                  command=self.calibrate_color).grid(row=0, column=1, padx=(0, 10))
        
        # Save/Load config buttons
        ttk.Button(controls_frame, text="Ayarları Kaydet", 
                  command=self.save_config).grid(row=0, column=2, padx=(0, 10))
        ttk.Button(controls_frame, text="İstatistik Sıfırla", 
                  command=self.reset_stats).grid(row=0, column=3)
        
    def setup_statistics_section(self, parent, row):
        """İstatistikler"""
        stats_frame = ttk.LabelFrame(parent, text="İstatistikler", padding="10")
        stats_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.stats_labels = {
            'runtime': ttk.Label(stats_frame, text="Çalışma Süresi: 0s"),
            'detections': ttk.Label(stats_frame, text="Algılama: 0"),
            'clicks': ttk.Label(stats_frame, text="Tıklama: 0"),
            'false_positives': ttk.Label(stats_frame, text="Yanlış Pozitif: 0"),
            'scan_time': ttk.Label(stats_frame, text="Ort. Tarama: 0.0ms"),
            'accuracy': ttk.Label(stats_frame, text="Doğruluk: 0%")
        }
        
        row_idx = 0
        for key, label in self.stats_labels.items():
            col = row_idx % 3
            row_pos = row_idx // 3
            label.grid(row=row_pos, column=col, sticky=tk.W, padx=(0, 15))
            row_idx += 1
            
    def setup_debug_section(self, parent, row):
        """Debug bölümü"""
        debug_frame = ttk.LabelFrame(parent, text="Debug Bilgileri", padding="10")
        debug_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Current pixel color
        self.current_color_label = ttk.Label(debug_frame, text="Mevcut Pixel: RGB(0, 0, 0)")
        self.current_color_label.grid(row=0, column=0, sticky=tk.W)
        
        # Color similarity
        self.similarity_label = ttk.Label(debug_frame, text="Benzerlik: 0%")
        self.similarity_label.grid(row=0, column=1, padx=(20, 0), sticky=tk.W)
        
        # Matching pixels
        self.matching_pixels_label = ttk.Label(debug_frame, text="Eşleşen Pixel: 0/25")
        self.matching_pixels_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
    def setup_log_section(self, parent, row):
        """Log bölümü"""
        log_frame = ttk.LabelFrame(parent, text="Aktivite Logu", padding="10")
        log_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        log_text_frame = ttk.Frame(log_frame)
        log_text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.log_text = tk.Text(log_text_frame, height=6, width=70, wrap=tk.WORD)
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
        """Renk seçici"""
        current_color = f"#{self.target_color[0]:02x}{self.target_color[1]:02x}{self.target_color[2]:02x}"
        color = colorchooser.askcolor(title="Hedef Renk Seç", initialcolor=current_color)
        
        if color[0]:
            self.target_color = [int(color[0][0]), int(color[0][1]), int(color[0][2])]
            self.update_color_display()
            self.log(f"Hedef renk değiştirildi: RGB({self.target_color[0]}, {self.target_color[1]}, {self.target_color[2]})")
            
    def update_color_display(self):
        """Renk gösterimini güncelle"""
        color_hex = f"#{self.target_color[0]:02x}{self.target_color[1]:02x}{self.target_color[2]:02x}"
        self.color_canvas.configure(bg=color_hex)
        self.color_label.configure(text=f"RGB({self.target_color[0]}, {self.target_color[1]}, {self.target_color[2]})")
        
    def update_tolerance_display(self, *args):
        """Tolerans gösterimini güncelle"""
        self.tolerance_value_label.configure(text=f"{self.tolerance.get()*100:.0f}%")
        
    def calibrate_color(self):
        """Renk kalibrasyonu - mevcut pixel rengini al"""
        try:
            if not self.hdc:
                self.hdc = user32.GetDC(0)
                
            if self.hdc:
                color_ref = gdi32.GetPixel(self.hdc, self.center_x, self.center_y)
                if color_ref != 0xFFFFFFFF:
                    r = color_ref & 0xFF
                    g = (color_ref >> 8) & 0xFF
                    b = (color_ref >> 16) & 0xFF
                    
                    self.target_color = [r, g, b]
                    self.update_color_display()
                    self.log(f"Renk kalibre edildi: RGB({r}, {g}, {b})")
                else:
                    self.log("Kalibrasyon hatası: Geçersiz pixel")
            else:
                self.log("Kalibrasyon hatası: Device context alınamadı")
                
        except Exception as e:
            self.log(f"Kalibrasyon hatası: {e}")
            
    def test_click(self):
        """Tıklama testi"""
        try:
            success = self.perform_click_advanced()
            if success:
                self.log(f"Tıklama testi başarılı ({self.click_method.get()})")
            else:
                self.log(f"Tıklama testi başarısız ({self.click_method.get()})")
        except Exception as e:
            self.log(f"Tıklama testi hatası: {e}")
            
    def toggle_detection(self):
        """Algılamayı başlat/durdur"""
        if not self.detection_active:
            self.start_detection()
        else:
            self.stop_detection()
            
    def start_detection(self):
        """Algılamayı başlat"""
        try:
            self.log("Gelişmiş algılama başlatılıyor...")
            
            # Device context al
            self.hdc = user32.GetDC(0)
            if not self.hdc:
                raise Exception("Device context alınamadı")
                
            self.detection_active = True
            self.running = True
            self.start_time = time.time()
            
            # Update UI
            self.status_canvas.itemconfig(self.status_indicator, fill="green")
            self.status_label.configure(text="AKTIF", foreground="green")
            self.start_stop_button.configure(text="ALGILAMA DURDUR")
            
            # Start detection thread
            self.detection_thread = threading.Thread(target=self.advanced_detection_loop, daemon=True)
            self.detection_thread.start()
            
            self.log("Gelişmiş algılama başlatıldı")
            
        except Exception as e:
            self.log(f"Başlatma hatası: {e}")
            
    def stop_detection(self):
        """Algılamayı durdur"""
        self.log("Algılama durduruluyor...")
        self.detection_active = False
        self.running = False
        
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
        self.start_stop_button.configure(text="ALGILAMA BAŞLAT")
        
        self.log("Algılama durduruldu")
        
    def advanced_detection_loop(self):
        """Gelişmiş algılama döngüsü"""
        last_click_time = 0
        
        while self.running:
            try:
                scan_start = time.time()
                
                # Gelişmiş tarama
                detection_result = self.advanced_scan()
                
                scan_time = time.time() - scan_start
                self.stats['scan_times'].append(scan_time)
                
                if detection_result['detected']:
                    self.stats['detections'] += 1
                    
                    # Debug bilgilerini güncelle
                    self.update_debug_info(detection_result)
                    
                    # Tıklama kontrolü
                    current_time = time.time()
                    if current_time - last_click_time >= (self.click_cooldown.get() / 1000.0):
                        if self.perform_click_advanced():
                            last_click_time = current_time
                            self.stats['clicks'] += 1
                            self.log(f"Tıklama gerçekleştirildi (Eşleşen pixel: {detection_result['matching_pixels']})")
                else:
                    # Yanlış pozitif kontrolü
                    if detection_result['similarity'] > 0.3:  # Yakın ama yeterli değil
                        self.stats['false_positives'] += 1
                
                # Sleep
                time.sleep(self.scan_interval.get() / 1000.0)
                
            except Exception as e:
                self.log(f"Algılama hatası: {e}")
                time.sleep(0.1)
                
    def advanced_scan(self):
        """Gelişmiş tarama algoritması"""
        try:
            matching_pixels = 0
            total_similarity = 0.0
            best_similarity = 0.0
            sample_colors = []
            
            for pixel_info in self.pixel_grid:
                offset_x, offset_y = pixel_info['offset']
                weight = pixel_info['weight']
                
                pixel_x = self.center_x + offset_x
                pixel_y = self.center_y + offset_y
                
                # Ekran sınırları kontrolü
                if 0 <= pixel_x < self.screen_width and 0 <= pixel_y < self.screen_height:
                    color = self.get_pixel_color_safe(pixel_x, pixel_y)
                    
                    if color:
                        similarity = self.calculate_color_similarity_advanced(color, self.target_color)
                        weighted_similarity = similarity * weight
                        
                        total_similarity += weighted_similarity
                        best_similarity = max(best_similarity, similarity)
                        sample_colors.append(color)
                        
                        if similarity >= self.tolerance.get():
                            matching_pixels += 1
            
            # Ortalama benzerlik hesapla
            avg_similarity = total_similarity / len(self.pixel_grid) if self.pixel_grid else 0.0
            
            # Algılama kriteri: yeterli pixel eşleşmesi VE yüksek ortalama benzerlik
            detected = (matching_pixels >= self.min_pixels_required.get() and 
                       avg_similarity >= self.tolerance.get())
            
            return {
                'detected': detected,
                'matching_pixels': matching_pixels,
                'avg_similarity': avg_similarity,
                'best_similarity': best_similarity,
                'sample_colors': sample_colors
            }
            
        except Exception as e:
            self.log(f"Tarama hatası: {e}")
            return {
                'detected': False,
                'matching_pixels': 0,
                'avg_similarity': 0.0,
                'best_similarity': 0.0,
                'sample_colors': []
            }
            
    def get_pixel_color_safe(self, x, y):
        """Güvenli pixel rengi alma"""
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
            
    def calculate_color_similarity_advanced(self, color1, color2):
        """Gelişmiş renk benzerliği hesaplama"""
        try:
            # Euclidean distance in RGB space
            diff_squared = sum((a - b) ** 2 for a, b in zip(color1, color2))
            distance = math.sqrt(diff_squared)
            max_distance = math.sqrt(3 * (255 ** 2))
            
            # Normalize to 0-1 range
            similarity = 1.0 - (distance / max_distance)
            
            return max(0.0, min(1.0, similarity))
        except:
            return 0.0
            
    def perform_click_advanced(self):
        """Gelişmiş tıklama yöntemleri"""
        try:
            method = self.click_method.get()
            
            if method == "mouse_event":
                # Standart mouse_event
                user32.mouse_event(0x0002, 0, 0, 0, 0)  # MOUSEEVENTF_LEFTDOWN
                time.sleep(0.001)
                user32.mouse_event(0x0004, 0, 0, 0, 0)  # MOUSEEVENTF_LEFTUP
                return True
                
            elif method == "sendmessage":
                # SendMessage ile tıklama
                hwnd = user32.GetForegroundWindow()
                if hwnd:
                    user32.SendMessageW(hwnd, 0x0201, 0x0001, 0)  # WM_LBUTTONDOWN
                    time.sleep(0.001)
                    user32.SendMessageW(hwnd, 0x0202, 0x0000, 0)  # WM_LBUTTONUP
                    return True
                    
            elif method == "postmessage":
                # PostMessage ile tıklama
                hwnd = user32.GetForegroundWindow()
                if hwnd:
                    user32.PostMessageW(hwnd, 0x0201, 0x0001, 0)  # WM_LBUTTONDOWN
                    time.sleep(0.001)
                    user32.PostMessageW(hwnd, 0x0202, 0x0000, 0)  # WM_LBUTTONUP
                    return True
                    
            elif method == "simulate":
                # Simulated input
                try:
                    # Bu yöntem daha gelişmiş ama daha karmaşık
                    user32.SetCursorPos(self.center_x, self.center_y)
                    time.sleep(0.001)
                    user32.mouse_event(0x0002, 0, 0, 0, 0)
                    time.sleep(0.001)
                    user32.mouse_event(0x0004, 0, 0, 0, 0)
                    return True
                except:
                    return False
                    
            return False
            
        except Exception as e:
            self.log(f"Tıklama hatası: {e}")
            return False
            
    def update_debug_info(self, detection_result):
        """Debug bilgilerini güncelle"""
        try:
            # Sample color from center
            if detection_result['sample_colors']:
                center_color = detection_result['sample_colors'][len(detection_result['sample_colors'])//2]
                self.current_color_label.configure(
                    text=f"Mevcut Pixel: RGB({center_color[0]}, {center_color[1]}, {center_color[2]})")
            
            # Similarity
            self.similarity_label.configure(
                text=f"Benzerlik: {detection_result['avg_similarity']*100:.1f}%")
            
            # Matching pixels
            self.matching_pixels_label.configure(
                text=f"Eşleşen Pixel: {detection_result['matching_pixels']}/{len(self.pixel_grid)}")
                
        except:
            pass
            
    def update_display(self):
        """Ekranı güncelle"""
        try:
            if self.detection_active:
                runtime = time.time() - self.start_time
                self.stats['runtime'] = runtime
                
                if self.stats['scan_times']:
                    avg_scan = sum(self.stats['scan_times']) / len(self.stats['scan_times'])
                    self.stats['avg_scan_time'] = avg_scan
                
                # Accuracy calculation
                total_actions = self.stats['detections'] + self.stats['false_positives']
                accuracy = (self.stats['detections'] / total_actions * 100) if total_actions > 0 else 0
                
                self.stats_labels['runtime'].configure(text=f"Çalışma Süresi: {runtime:.1f}s")
                self.stats_labels['detections'].configure(text=f"Algılama: {self.stats['detections']}")
                self.stats_labels['clicks'].configure(text=f"Tıklama: {self.stats['clicks']}")
                self.stats_labels['false_positives'].configure(text=f"Yanlış Pozitif: {self.stats['false_positives']}")
                self.stats_labels['scan_time'].configure(text=f"Ort. Tarama: {self.stats['avg_scan_time']*1000:.2f}ms")
                self.stats_labels['accuracy'].configure(text=f"Doğruluk: {accuracy:.1f}%")
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
            self.stats['clicks'] = 0
            self.stats['false_positives'] = 0
            self.stats['scan_times'].clear()
            self.stats['color_samples'].clear()
            if hasattr(self, 'start_time'):
                self.start_time = time.time()
            self.log("İstatistikler sıfırlandı")
        except Exception as e:
            self.log(f"Sıfırlama hatası: {e}")
        
    def save_config(self):
        """Ayarları kaydet"""
        config = {
            'target_color': self.target_color,
            'tolerance': self.tolerance.get(),
            'scan_interval': self.scan_interval.get(),
            'click_cooldown': self.click_cooldown.get(),
            'min_pixels_required': self.min_pixels_required.get(),
            'click_method': self.click_method.get()
        }
        
        try:
            with open('improved_detector_config.json', 'w') as f:
                json.dump(config, f, indent=2)
            self.log("Ayarlar kaydedildi")
        except Exception as e:
            self.log(f"Kaydetme hatası: {e}")
            
    def load_config(self):
        """Ayarları yükle"""
        try:
            if os.path.exists('improved_detector_config.json'):
                with open('improved_detector_config.json', 'r') as f:
                    config = json.load(f)
                    
                self.target_color = config.get('target_color', [128, 0, 128])
                self.tolerance.set(config.get('tolerance', 0.4))
                self.scan_interval.set(config.get('scan_interval', 50.0))
                self.click_cooldown.set(config.get('click_cooldown', 200.0))
                self.min_pixels_required.set(config.get('min_pixels_required', 3))
                self.click_method.set(config.get('click_method', 'mouse_event'))
                
                self.update_color_display()
        except:
            pass
            
    def on_closing(self):
        """Uygulama kapanırken"""
        if self.detection_active:
            self.stop_detection()
        self.root.destroy()
        
    def run(self):
        """Uygulamayı başlat"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.log("Geliştirilmiş Algılama Sistemi başlatıldı")
        self.root.mainloop()

if __name__ == "__main__":
    app = ImprovedDetector()
    app.run()