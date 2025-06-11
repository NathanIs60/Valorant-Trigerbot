# 🔧 Sorun Giderme Kılavuzu

## Yaygın Problemler ve Çözümleri

### 1. "Tıklama Gösteriyor Ama Oyunda Çalışmıyor"

#### Neden Oluyor?
- **Anti-cheat sistemi**: Valorant'ın Vanguard sistemi mouse olaylarını filtreler
- **Input validation**: Oyun sadece gerçek hardware input'ları kabul eder
- **Timing issues**: Çok hızlı tıklamalar spam olarak algılanır

#### Çözümler:
```python
# 1. Farklı tıklama yöntemleri dene
methods = ["mouse_event", "sendmessage", "postmessage", "simulate"]

# 2. Tıklama gecikmesini artır
click_cooldown = 200-500  # ms

# 3. Hardware simulation
# Fiziksel cihaz kullan (Arduino, vb.)
```

### 2. "Yanlış Renkte de Çalışıyor"

#### Neden Oluyor?
- **Yüksek tolerans**: %60+ tolerans çok gevşek
- **Kötü renk algoritması**: Basit RGB karşılaştırması yetersiz
- **Tek pixel kontrolü**: 1 pixel yeterli bilgi vermiyor

#### Çözümler:
```python
# 1. Toleransı düşür
tolerance = 0.3-0.4  # %30-40

# 2. Çoklu pixel kontrolü
min_pixels_required = 3-5

# 3. Gelişmiş renk algoritması
def advanced_color_match(color1, color2, tolerance):
    # HSV color space kullan
    # Weighted similarity
    # Multiple criteria
```

### 3. "Algılama Çok Yavaş/Hızlı"

#### Optimizasyon:
```python
# Hızlı tarama için
scan_interval = 10-50  # ms

# Kararlı tarama için  
scan_interval = 100-200  # ms

# CPU kullanımını azalt
scan_interval = 500+  # ms
```

## Valorant Özel Problemleri

### Vanguard Engelleme
```
GetPixel()      -> ❌ Engellenir
mouse_event()   -> ❌ Tespit edilir
Screenshot      -> ⚠️ Yavaş/riskli
Hardware        -> ✅ Çalışabilir
```

### Alternatif Yaklaşımlar
1. **Test ortamı kullan**
2. **Aim trainer'larda test et**
3. **Hardware çözümler araştır**
4. **Eğitim amaçlı kullan**

## Debug Araçları

### 1. Pixel İzleme
```python
# Gerçek zamanlı pixel rengi
debug_tools.py  # Çalıştır
```

### 2. Tıklama Testi
```python
# Farklı yöntemleri test et
test_click()  # Her yöntemi dene
```

### 3. Renk Kalibrasyonu
```python
# Mevcut pixel rengini al
calibrate_color()  # Otomatik ayar
```

## Önerilen Ayarlar

### Kararlı Kullanım
```json
{
  "tolerance": 0.4,
  "scan_interval": 100,
  "click_cooldown": 300,
  "min_pixels": 3,
  "method": "mouse_event"
}
```

### Hızlı Kullanım
```json
{
  "tolerance": 0.3,
  "scan_interval": 50,
  "click_cooldown": 150,
  "min_pixels": 2,
  "method": "sendmessage"
}
```

### Test Kullanımı
```json
{
  "tolerance": 0.6,
  "scan_interval": 200,
  "click_cooldown": 500,
  "min_pixels": 5,
  "method": "simulate"
}
```

## Güvenlik Uyarıları

### ⚠️ Riskler
- Hesap banı
- Anti-cheat tespiti
- Sistem güvenliği
- Yasal sorunlar

### ✅ Güvenli Kullanım
- Test ortamında çalıştır
- Ana hesabında kullanma
- Eğitim amaçlı kullan
- Yasal sınırlara uy

## Sonuç

Bu programlar **eğitim ve test** amaçlıdır. Valorant gibi korumalı oyunlarda çalışması beklenmemelidir. Güvenli test ortamlarında kullanın ve sorumlu davranın.