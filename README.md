# Spot the Differences DAA - Unlimited Matrix Component Search

Sebuah game mencari perbedaan gambar (*Spot the Differences*) multi-level yang dibangun menggunakan Python dan library Pygame. Proyek ini menerapkan pendekatan otomatisasi pemindaian gambar berbasis Desain dan Analisis Algoritma (DAA) untuk mendeteksi area perbedaan secara dinamis tanpa koordinat manual (*hardcoded*).

## 🚀 Fitur Utama
- **Automated Matrix Scan:** Gambar asli dan modifikasi langsung dipindai secara otomatis saat level dimuat.
- **Dynamic Multi-Level:** Mendukung arsitektur tiga tingkatan level (Stage 1: Neon Horizon, Stage 2: Cozy Interior, Stage 3: Workspace Table).
- **Unlimited Component Scan:** Optimalisasi kerapatan scanning (`STEP = 6`) untuk mendeteksi objek kecil atau berdekatan (seperti area dasi & jas pada Level 2).
- **Responsive HUD & Status Bar:** Menampilkan skor, nyawa, tingkat level, dan jumlah target riil secara *real-time*.

## 🧠 Algoritma DAA yang Digunakan

1. **Brute Force (Matrix Subtraction):** Melakukan perulangan menyeluruh terhadap matriks piksel gambar ($460 \times 460$ px). Perbedaan warna dihitung menggunakan rumus *Manhattan Distance*:
   $$\text{Selisih} = |R_{\text{asli}} - R_{\text{modif}}| + |G_{\text{asli}} - G_{\text{modif}}| + |B_{\text{asli}} - B_{\text{modif}}|$$

2. **Greedy (Distance-Based Clustering):**
   Mengelompokkan ribuan titik piksel hasil *Brute Force* yang berbeda menjadi satu objek lingkaran target tunggal menggunakan rumus *Euclidean Distance*. Jika jarak antar titik $< 25$ piksel, titik tersebut secara *greedy* digabungkan ke kluster terdekat demi efisiensi area klik pemain.

## 🛠️ Cara Menjalankan Game

### Prasyarat
Pastikan Anda sudah menginstal Python (versi 3.x) dan library Pygame di komputer Anda.

```bash
pip install pygame