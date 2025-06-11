# Valorant ve Anti-Cheat Sistemleri Hakkında

## Neden Çalışmıyor?

### 1. Vanguard Anti-Cheat
- **Kernel seviyesi koruma**: Ring 0 seviyesinde çalışır
- **API engelleme**: Windows API çağrılarını tespit eder
- **Bellek koruması**: Oyun belleğine erişimi engeller
- **Süreç izleme**: Şüpheli süreçleri tespit eder

### 2. Korumalı Fonksiyonlar
```
GetPixel()          -> Engellenir
mouse_event()       -> Tespit edilir
SetCursorPos()      -> İzlenir
GetDC()             -> Kısıtlanır
```

### 3. Algılama Yöntemleri
- **Timing analizi**: İnsan olmayan hızlarda tıklama
- **Pattern recognition**: Tekrarlayan davranışlar
- **Memory scanning**: Bellek değişiklikleri
- **Process monitoring**: Şüpheli süreçler

## Alternatif Yaklaşımlar (Sadece Eğitim Amaçlı)

### 1. Screenshot Tabanlı
```python
# PIL ile ekran görüntüsü
from PIL import ImageGrab
screenshot = ImageGrab.grab()
```

### 2. OpenCV Görüntü İşleme
```python
# Renk algılama
import cv2
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, lower, upper)
```

### 3. Hardware Tabanlı
- Arduino/Raspberry Pi
- Fiziksel kamera
- Hardware mouse/keyboard

## Yasal ve Etik Uyarılar

### ⚠️ Önemli Notlar
- Valorant ToS'u ihlal eder
- Hesap banına neden olur
- Vanguard tarafından tespit edilir
- Sadece eğitim amaçlı kullanın

### 🔒 Güvenlik
- Test ortamında çalıştırın
- Ana hesabınızda denemeyin
- Antivirus uyarılarına dikkat edin
- Sistem güvenliğini riske atmayın

## Test Ortamı Önerileri

### 1. Sanal Makine
- VMware/VirtualBox
- İzole test ortamı
- Güvenli deneme alanı

### 2. Test Oyunları
- Aim trainers
- Browser oyunları
- Offline oyunlar

### 3. Kendi Uygulamanız
- Test renkleri
- Kontrollü ortam
- Güvenli geliştirme

## Sonuç

Bu tür programlar **eğitim ve araştırma** amaçlı olarak değerlidir, ancak:

- Valorant gibi korumalı oyunlarda çalışmaz
- Anti-cheat sistemleri tarafından engellenir
- Hesap güvenliği riski oluşturur
- Sadece test ortamlarında kullanılmalıdır

**Sorumluluk kullanıcıya aittir!**