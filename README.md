#  Flow-Shop Scheduling — Tabu Search ile Optimizasyon

**ENM404 Üretim Çizelgeleme | İstanbul Kültür Üniversitesi | 2024–2025**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Benchmark](https://img.shields.io/badge/Benchmark-Taillard%201993-orange.svg)](http://mistic.heig-vd.ch/taillard/)

---

##  Proje Hakkında

Bu proje, **Flow-Shop Scheduling** probleminin **Tabu Search (TS)** metasezgisel algoritması ile çözümünü içermektedir. Taillard (1993) benchmark instance'ları kullanılarak 5 farklı boyutta test edilmiş, 2/5 instance'da literatürdeki en iyi çözümün (BKS) altına inilmiştir.

| | |
|---|---|
| **Grup** | 9 |
| **Problem** | Flow-Shop Scheduling (Makespan Minimizasyonu) |
| **Algoritma** | Tabu Search (TS) |
| **Başlangıç** | NEH Sezgiseli (Nawaz-Enscore-Ham, 1983) |
| **Benchmark** | Taillard (1993) — 5 Instance |
| **Dil** | Python 3.8+ |

---

##  Sonuçlar

| Instance | Boyut | BKS | En İyi | Gap (%) | Süre (s) |
|---|---|---|---|---|---|
| tai20x5 | 20 × 5 | 1278 | 1187 | **-7.12%** ✅ | 1.81 |
| tai50x10 | 50 × 10 | 2724 | 2979 | +9.36% | 1.94 |
| tai100x10 | 100 × 10 | 5770 | 5604 | **-2.88%** ✅ | 3.96 |
| tai100x20 | 100 × 20 | 6286 | 6625 | +5.39% | 5.19 |
| tai200x20 | 200 × 20 | 11294 | 11492 | +1.75% | 23.16 |

> ✅ = BKS (Best Known Solution) altına inildi

**Seçilen Parametreler:** `tenure=50`, `max_iter=600`, `no_improve_limit=120`

---

##  Dosya Yapısı

```
flowshop_ts/
│
├── main.py                # Ana çalıştırma dosyası
├── tabu_search.py         # Tabu Search algoritması
├── neh.py                 # NEH başlangıç sezgiseli
├── makespan.py            # Cmax hesaplama
├── neighbourhood.py       # Komşuluk yapısı (Swap)
├── generate_taillard.py   # Taillard instance üretici
├── instance_loader.py     # Instance yükleme
├── plotter.py             # Yakınsama grafikleri
├── results_logger.py      # Sonuç kaydetme
│
├── instances/             # Taillard benchmark dosyaları
├── results/               # Deney sonuçları (CSV)
└── plots/                 # Yakınsama grafikleri (PNG)
```

---

##  Kurulum ve Çalıştırma

### 1. Gereksinimleri yükle
```bash
pip install numpy matplotlib
```

### 2. Çalıştır
```bash
python main.py
```

### Beklenen çıktı:
```
ENM404 Grup 9 | Flow-Shop + Tabu Search
============================================================
[Kolay] tai20x5 (20x5)  BKS=1278
  Çalıştırma  1: Cmax=1187  t=1.8s
  Çalıştırma  2: Cmax=1187  t=1.8s
  ...
Tamamlandı! Sonuçlar: results/ ve plots/ klasörlerinde.
```

---

##  Algoritma Tasarımı

### Tabu Search Bileşenleri

| Bileşen | Açıklama |
|---|---|
| **Çözüm Temsili** | İş permütasyonu: `[3, 1, 4, 2, 5]` |
| **Başlangıç Çözümü** | NEH Sezgiseli |
| **Komşuluk** | Swap hamlesi (n>30 için rastgele örnekleme) |
| **Tabu Listesi** | Son `tenure=50` hamle yasaklanır |
| **Aspirasyon** | BKS'yi geçen tabu hamle kabul edilir |
| **Durdurma** | Max 600 iter veya 120 iter iyileşme yok |

### NEH Algoritması
1. İşleri toplam işlem süresine göre azalan sırada sırala
2. İlk iki işi en iyi sırada yerleştir
3. Her yeni işi mevcut dizinin en iyi pozisyonuna ekle

---

##  Parametre Tuning

`tai50x10` instance'ı üzerinde sistematik tuning yapılmıştır:

| Tenure | Gap (%) | Std Dev | Seçildi? |
|---|---|---|---|
| 5 | +9.62% | 17.2 | |
| 10 | +9.36% | 27.9 | |
| 20 | +9.40% | 18.4 | |
| 30 | +9.47% | 18.1 | |
| **50** | **+9.32%** | **7.3** | **✅** |

`tenure=50` hem en düşük gap hem de en düşük standart sapmayı vermiştir.

---

##  Kaynaklar

- Taillard, E. (1993). Benchmarks for basic scheduling problems. *European Journal of Operational Research*, 64(2), 278–285.
- Nawaz, M., Enscore, E. E., & Ham, I. (1983). A heuristic algorithm for the m-machine, n-job flow-shop sequencing problem. *Omega*, 11(1), 91–95.
- Glover, F. (1989). Tabu Search — Part I. *ORSA Journal on Computing*, 1(3), 190–206.

---

##  Grup 9

İstanbul Kültür Üniversitesi — ENM404 Üretim Çizelgeleme — 2024–2025
