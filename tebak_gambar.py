import pygame

# Inisialisasi Pygame
pygame.init()

# Ukuran Jendela Game
LEBAR = 1000
TINGGI = 650
layar = pygame.display.set_mode((LEBAR, TINGGI))
pygame.display.set_caption("Spot the Differences DAA - Unlimited Matrix Component Search")
clock = pygame.time.Clock()

# Warna (RGB)
HITAM = (15, 15, 15)
PUTIH = (255, 255, 255)
MERAH_LINGKARAN = (255, 50, 50)
HIJAU_SUKSES = (50, 205, 50)
KUNING_TEKS = (255, 215, 0)

# ================= CONFIGURATION DATA LEVEL =================
# AKTIF 3 LEVEL: Pastikan nama file gambar_asli3.png dan gambar_modifikasi3.png sudah ada di folder Anda.
DAFTAR_STAGE = [
    {"level": 1, "asli": "gambar_asli.png", "modif": "gambar_modifikasi.png"},
    {"level": 2, "asli": "gambar_asli2.png", "modif": "gambar_modifikasi2.png"},
    {"level": 3, "asli": "gambar_asli3.png", "modif": "gambar_modifikasi3.png"}
]

# ================= ALGORITMA DAA: UNLIMITED COMPONENT SCAN =================
def auto_scan_perbedaan(imgA, imgB):
    """
    Algoritma DAA memindai seluruh matriks gambar secara utuh tanpa batasan kuota.
    Every isolated stroke will be fairly registered into the array.
    """
    titik_berbeda = []
    STEP = 6 # Langkah scanning rapat agar coretan tipis/kecil tidak terlewat
    
    arrA = pygame.PixelArray(imgA)
    arrB = pygame.PixelArray(imgB)
    
    for y in range(0, 460, STEP):
        for x in range(0, 460, STEP):
            pixelA = arrA[x, y]
            pixelB = arrB[x, y]
            
            if pixelA != pixelB:
                colorA = imgA.unmap_rgb(pixelA)
                colorB = imgB.unmap_rgb(pixelB)
                selisih = abs(colorA.r - colorB.r) + abs(colorA.g - colorB.g) + abs(colorA.b - colorB.b)
                
                # Toleransi warna coretan agar sensitif terhadap editan kuas
                if selisih > 30: 
                    terlalu_dekat = False
                    for p in titik_berbeda:
                        jarak = ((x - p["x"])**2 + (y - p["y"])**2)**0.5
                        # Jarak penggabungan kluster titik piksel terdekat
                        if jarak < 25: 
                            terlalu_dekat = True
                            break
                    
                    # Batasan kuas maksimal '< 5' dilepas agar area dasi/jas bawah ikut terdeteksi
                    if not terlalu_dekat:
                        titik_berbeda.append({"x": x, "y": y, "r": 40, "ketemu": False})
                        
    arrA.close()
    arrB.close()
    return titik_berbeda

# ================= FUNGSIONALITAS PEMUATAN LEVEL =================
def muat_dan_scan_level(config_stage):
    try:
        img_asli = pygame.image.load(config_stage["asli"]).convert()
        img_asli = pygame.transform.scale(img_asli, (460, 460))
        
        img_modif = pygame.image.load(config_stage["modif"]).convert()
        img_modif = pygame.transform.scale(img_modif, (460, 460))
        
        print(f"\n[DAA SCANNER] Memindai Matriks Gambar Level {config_stage['level']}...")
        perbedaan_terdeteksi = auto_scan_perbedaan(img_asli, img_modif)
        print(f"[DAA STATUS] Sukses mendeteksi otomatis {len(perbedaan_terdeteksi)} area perbedaan riil!")
        
        return img_asli, img_modif, perbedaan_terdeteksi
    except Exception as e:
        print(f"Gagal memuat gambar Level {config_stage['level']}: {e}")
        surf_asli = pygame.Surface((460, 460))
        surf_asli.fill((40, 40, 40))
        surf_modif = surf_asli.copy()
        pygame.draw.circle(surf_modif, (255, 0, 0), (230, 230), 40)
        return surf_asli, surf_modif, [{"x": 230, "y": 230, "r": 40, "ketemu": False}]

# ================= ALGORITMA EVALUASI KLIK =================
def cek_klik_perbedaan(mx, my, daftar_target, side_offset=500):
    if mx >= side_offset:
        mx -= side_offset
    mx -= 20
    my -= 80

    for p in daftar_target:
        if not p["ketemu"]:
            jarak = ((mx - p["x"])**2 + (my - p["y"])**2)**0.5
            if jarak <= p["r"]:
                return p 
    return None

# ================= MAIN GAME LOOP =================
def main():
    stage_idx = 0
    max_stage = len(DAFTAR_STAGE)
    
    img_asli, img_modifikasi, daftar_perbedaan = muat_dan_scan_level(DAFTAR_STAGE[stage_idx])
    target_aktif_count = len(daftar_perbedaan)

    skor = 0
    jumlah_ketemu = 0
    nyawa = 5
    game_over = False
    menang_total = False
    pesan_status = f"Level {DAFTAR_STAGE[stage_idx]['level']}: Temukan semua perbedaan gambar!"

    font_hud = pygame.font.SysFont('Arial', 18, bold=True)
    font_status = pygame.font.SysFont('Arial', 18, bold=True)
    font_besar = pygame.font.SysFont('Arial', 36, bold=True)

    running = True
    while running:
        layar.fill(HITAM)
        mx, my = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over and not menang_total:
                klik_di_gambar_kiri = (20 <= mx <= 480 and 80 <= my <= 540)
                klik_di_gambar_kanan = (520 <= mx <= 980 and 80 <= my <= 540)
                
                if klik_di_gambar_kiri or klik_di_gambar_kanan:
                    komponen_cocok = cek_klik_perbedaan(mx, my, daftar_perbedaan)
                    
                    if komponen_cocok:
                        komponen_cocok["ketemu"] = True
                        jumlah_ketemu += 1
                        skor += 200
                        pesan_status = f"Hebat! Ketemu {jumlah_ketemu}/{target_aktif_count} perbedaan."
                        
                        # Cek apakah semua target riil pada level ini sudah ditemukan
                        if jumlah_ketemu == target_aktif_count:
                            stage_idx += 1
                            if stage_idx < max_stage:
                                pesan_status = "Luar biasa! Bersiap menuju gambar selanjutnya..."
                                pygame.draw.rect(layar, (25, 25, 25), (0, 590, LEBAR, 60))
                                layar.blit(font_status.render(pesan_status, True, KUNING_TEKS), (20, 610))
                                pygame.display.flip()
                                pygame.time.wait(1500)
                                
                                # Muat level berikutnya secara dinamis sesuai DAFTAR_STAGE
                                img_asli, img_modifikasi, daftar_perbedaan = muat_dan_scan_level(DAFTAR_STAGE[stage_idx])
                                target_aktif_count = len(daftar_perbedaan)
                                jumlah_ketemu = 0
                                pesan_status = f"Level {DAFTAR_STAGE[stage_idx]['level']}: Cari {target_aktif_count} perbedaan baru!"
                            else:
                                menang_total = True
                    else:
                        nyawa -= 1
                        pesan_status = f"Salah klik! Area itu sama. Nyawa berkurang!"
                        if nyawa <= 0:
                            game_over = True

        if not running:
            break

        # --- PANEL ATAS (HUD) ---
        pygame.draw.rect(layar, (30, 30, 30), (0, 0, LEBAR, 60))
        layar.blit(font_hud.render(f"SKOR: {skor}", True, PUTIH), (20, 20))
        layar.blit(font_hud.render(f"NYAWA: {'♥ ' * max(0, nyawa)}", True, MERAH_LINGKARAN), (180, 20))
        layar.blit(font_hud.render(f"STAGE: {stage_idx + 1}/{max_stage} (Target Valid: {target_aktif_count})", True, KUNING_TEKS), (450, 20))

        # --- RENDERING GAMBAR ---
        layar.blit(img_asli, (20, 80))        
        layar.blit(img_modifikasi, (520, 80)) 
        
        pygame.draw.rect(layar, PUTIH, (20, 80, 460, 460), 2)
        pygame.draw.rect(layar, PUTIH, (520, 80, 460, 460), 2)

        # --- RENDERING LINGKARAN HIJAU ---
        for p in daftar_perbedaan:
            if p["ketemu"]:
                pygame.draw.circle(layar, HIJAU_SUKSES, (20 + p["x"], 80 + p["y"]), p["r"], 3)
                pygame.draw.circle(layar, HIJAU_SUKSES, (520 + p["x"], 80 + p["y"]), p["r"], 3)

        # --- PANEL BAWAH (STATUS BAR) ---
        pygame.draw.rect(layar, (25, 25, 25), (0, 590, LEBAR, 60))
        if game_over:
            layar.blit(font_besar.render("GAME OVER - NYAWA HABIS!", True, MERAH_LINGKARAN), (20, 600))
        elif menang_total:
            layar.blit(font_besar.render("CONGRATULATIONS! KAMU MENANGKAN SELURUH LEVEL!", True, HIJAU_SUKSES), (20, 600))
        else:
            layar.blit(font_status.render(pesan_status, True, KUNING_TEKS if "Hebat" in pesan_status or "Level" in pesan_status or "Luar" in pesan_status else MERAH_LINGKARAN), (20, 610))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()