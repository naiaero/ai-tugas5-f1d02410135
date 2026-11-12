# README: Sistem Pakar Penentuan Strategi Pit Stop dan Pemilihan Ban Formula 1

## 1. Identitas Pengembang
* **Nama**: [Salsabila Nailafahdi]
* **NIM**: [F1D02410135]

---

## 2. Topik dan Cara Menjalankan Program

### Topik
Sistem Pakar berbasis **Forward Chaining** untuk memprediksi penentuan strategi *pit stop* dan pemilihan *compound* ban Formula 1 berdasarkan regulasi olahraga **FIA 2026** serta pemodelan strategi balapan taktis.

### Cara Menjalankan Program
* **Bahasa Pemrograman**: Python
* **Versi Minimal**: Python 3.10+ (Direkomendasikan Python 3.12)
* **Kebutuhan Pustaka**: Tidak memerlukan dependensi eksternal (menggunakan *built-in standard library* Python).
* **Perintah Eksekusi**:
  ```bash
  python main.py
  ```

---

## 3. Daftar Sumber dan Tabel Aturan

### Daftar Sumber Referensi
1. **S1 (Sumber 1)**: FIA 2026 F1 Regulations - Section B [Sporting] - Issue 09.
   * **Penerbit**: Fédération Internationale de l’Automobile (FIA).
   * **URL**: `https://www.fia.com/regulation/category/110`
   * **Tanggal Diterbitkan**: 1 Oktober 2026.
   * **Tanggal Akses**: 3 November 2026.
2. **S2 (Sumber 2)**: *Optimizing pit stop strategies in Formula 1 with dynamic programming and game theory*.
   * **Penerbit**: European Journal of Operational Research (Elsevier B.V.).
   * **Penulis**: Felipe Aguad & Charles Thraves.
   * **URL**: `https://doi.org/10.1016/j.ejor.2024.07.011`.
   * **Tanggal Diterbitkan**: 11 Juli 2024.
   * **Tanggal Akses**: 3 November 2026.

---

### Tabel Aturan (*Rule Base Table*)
Berikut adalah 19 aturan *IF-THEN* yang direpresentasikan dalam sistem pakar:

| Aturan | IF | THEN | Sumber |
| :--- | :--- | :--- | :--- |
| **R1** | Sesi = Balapan AND Kondisi Lintasan = Kering AND Deklarasi Basah FIA = Tidak AND Jumlah Compound Kering = 1 Jenis AND Sisa Lap <= Batas Stint | Mandat FIA = Wajib Pit Ganti Ban Lain | S1 |
| **R2** | Sesi = Balapan AND (Deklarasi Basah FIA = Ya OR Ban Saat Ini IN (Intermediate, Full Wet)) | Mandat FIA = Bebas Aturan Dua Compound | S1 |
| **R3** | Status Safety Car = Wajib Ban Basah SC | Pilihan Ban = Full Wet AND Mandat FIA = Wajib Full Wet | S1 |
| **R4** | Sesi = Kualifikasi AND Fase Quali IN (Q1, Q2) AND Kondisi Lintasan = Kering | Pilihan Ban = Soft | S1 |
| **R5** | Sesi = Kualifikasi AND Fase Quali = Q3 AND Kondisi Lintasan = Kering | Pilihan Ban = Soft Baru | S1 |
| **R6** | Kondisi Lintasan = Basah Deras | Pilihan Ban = Full Wet | S1, S2 |
| **R7** | Kondisi Lintasan = Lembap | Pilihan Ban = Intermediate | S1, S2 |
| **R8** | Kondisi Lintasan = Kering AND Target Stint = Hemat Panjang | Pilihan Ban = Hard | S2 |
| **R9** | Kondisi Lintasan = Kering AND Target Stint = Sedang Seimbang | Pilihan Ban = Medium | S2 |
| **R10** | Kondisi Lintasan = Kering AND Target Stint = Push Pendek | Pilihan Ban = Soft | S2 |
| **R11** | Degradasi Ban = Aus Parah | Keputusan Pit = Masuk Pit Sekarang | S2 |
| **R12** | Status Safety Car IN (VSC, Safety Car) AND Degradasi Ban IN (Tinggi, Aus Parah) | Keputusan Pit = Momen Pit Hemat Waktu | S2 |
| **R13** | Ancaman Rival = Ancaman Undercut AND Degradasi Ban IN (Tinggi, Aus Parah) | Keputusan Pit = Tangkis Undercut | S2 |
| **R14** | Degradasi Ban = Rendah AND Mandat FIA != Wajib Pit Ganti Ban Lain | Keputusan Pit = Stay Out | S2 |
| **R15** | Mandat FIA = Wajib Pit Ganti Ban Lain AND Pilihan Ban = \<Jenis Ban\> | Goal = "Box Box Box! Pasang Ban \<Jenis Ban\> - Memenuhi Wajib Regulasi FIA" | S1 |
| **R16** | Keputusan Pit = Momen Pit Hemat Waktu AND Pilihan Ban = \<Jenis Ban\> | Goal = "Box Lap Ini! Manfaatkan VSC/Safety Car -> Pasang Ban \<Jenis Ban\>" | S2 |
| **R17** | Keputusan Pit = Tangkis Undercut AND Pilihan Ban = \<Jenis Ban\> | Goal = "Box Lap Ini! Cover Undercut Rival -> Pasang Ban \<Jenis Ban\>" | S2 |
| **R18** | Sesi = Kualifikasi AND Pilihan Ban = Soft Baru | Goal = "Push Lap! Gas Pake Ban Soft Baru Buat Kualifikasi" | S1 |
| **R19** | Keputusan Pit = Stay Out | Goal = "Stay Out! Ban Masih Bagus, Lanjut Push di Trekan" | S2 |

---

## 4. Metode Inferensi dan Alur Penelusuran

### Metode yang Dipilih: Forward Chaining (Pelacakan Maju)
Metode inferensi yang digunakan adalah **Forward Chaining** (pelacakan maju). 

### Alasan Pemilihan Metode
Metode *Forward Chaining* dipilih karena sistem pakar ini berorientasi pada data telemetri real-time (*data-driven*). Pada situasi balapan F1, fakta-fakta lapangan (seperti status sesi, kondisi trek, tingkat degradasi ban, status Safety Car, dan posisi rival) sudah diketahui terlebih dahulu di *working memory*. Sistem kemudian secara bertahap mencocokkan fakta-fakta tersebut dengan premis *IF* dari aturan yang ada untuk menghasilkan fakta-fakta intermediate (seperti `Mandat FIA`, `Pilihan Ban`, `Keputusan Pit`) sampai mencapai kesimpulan akhir (*THEN / Goal*).

### Contoh Penelusuran Fakta (Trace Perhitungan Tangan)

* **Fakta Awal Input (Working Memory)**:
  1. `Sesi` = `Balapan`
  2. `Kondisi Lintasan` = `Kering`
  3. `Deklarasi Basah FIA` = `Tidak`
  4. `Jumlah Compound Kering` = `1 Jenis`
  5. `Sisa Lap <= Batas Stint` = `True`
  6. `Target Stint` = `Hemat Panjang`
  7. `Ancaman Rival` = `Ancaman Undercut`
  8. `Degradasi Ban` = `Tinggi`

* **Langkah Inferensi Forward Chaining**:
  1. **Siklus 1**: Mengevaluasi **R1** \\(\rightarrow\\) Premis `Sesi = Balapan AND Kondisi Lintasan = Kering AND Deklarasi Basah FIA = Tidak AND Jumlah Compound Kering = 1 Jenis AND Sisa Lap <= Batas Stint` terpenuhi.
     * *Fakta Baru Ditambahkan*: `Mandat FIA` = `Wajib Pit Ganti Ban Lain`.
  2. **Siklus 2**: Mengevaluasi **R8** \\(\rightarrow\\) Premis `Kondisi Lintasan = Kering AND Target Stint = Hemat Panjang` terpenuhi.
     * *Fakta Baru Ditambahkan*: `Pilihan Ban` = `Hard`.
  3. **Siklus 3**: Mengevaluasi **R13** \\(\rightarrow\\) Premis `Ancaman Rival = Ancaman Undercut AND Degradasi Ban IN (Tinggi, Aus Parah)` terpenuhi.
     * *Fakta Baru Ditambahkan*: `Keputusan Pit` = `Tangkis Undercut`.
  4. **Siklus 4**: Mengevaluasi **R15** & **R17** \\(\rightarrow\\) Premis `Keputusan Pit = Tangkis Undercut AND Pilihan Ban = Hard` terpenuhi.
     * *Goal Terbentuk*: **`"Box Lap Ini! Cover Undercut Rival -> Pasang Ban Hard"`**.

---

## 5. Kasus Uji dan Hasil Output (Screenshot)

### Kasus Uji 1: Penanganan Ancaman Undercut saat Balapan Kering
* **Input Fact**: Balapan utama, trek kering, baru pakai 1 jenis ban kering, target stint panjang, ada ancaman undercut rival, degradasi ban tinggi.
![Hasil Output Terminal (`kesimpulan1.png`)](screenshoot/kesimpulan1.png)

### Kasus Uji 2: Strategi Stay Out pada Sesi Kualifikasi Q3
* **Input Fact**: Sesi kualifikasi Q3, kondisi trek kering, target stint push pendek, degradasi ban rendah.
![Hasil Output Terminal (`kesimpulan2.png`)](screenshoot/kesimpulan2.png)

### Kasus Uji 3: Kondisi Ban Aus Parah Tanpa Match Goal Spesifik
* **Input Fact**: Sesi kualifikasi Q1, target stint panjang, degradasi ban aus parah.
![Hasil Output Terminal (`tidak-ada-kesimpulan.png`)](screenshoot/tidak-ada-kesimpulan.png)

---

## 6. Batas Keberlakuan Pengetahuan (*Scope & Limitation*)

Pengetahuan yang digunakan dalam sistem pakar ini disarikan dari Regulasi Olahraga Resmi FIA Formula 1 2026 (Section B) dan hasil riset optimasi strategi pit stop berbasis riset operasi (Aguad & Thraves, 2024), yang khusus dirancang untuk penentuan strategi pit stop dan pemilihan ban pada sesi kualifikasi dan balapan utama Formula 1 dalam kondisi balapan standar maupun kondisi dinamis (seperti Safety Car dan ancaman undercut). Hasil inferensi yang dikeluarkan oleh sistem ini bersifat rekomendasi atau saran teknis pendukung keputusan *race engineer*, bukan keputusan mutlak yang mengikat instruksi *pit wall* secara otomatis.

### Tampilan Batas Keberlakuan pada Program (Console Disclaimer)
```text
================================================================================
BATAS KEBERLAKUAN SISTEM:
Sistem pakar ini berbasis pada Regulasi FIA F1 2026 (Section B) dan model 
strategi balapan Aguad & Thraves (2024). Output yang dihasilkan bersifat 
rekomendasi/saran teknis pendukung keputusan, bukan keputusan akhir balapan.
================================================================================
```

---

## 7. Penggunaan Alat Bantu AI

Alat bantu AI (**Gemini / Gemini Notebook**) digunakan dalam pengembangan proyek ini sebagai sarana asistensi untuk:
1. Membantu pemetaan dan ekstraksi basis pengetahuan dari dokumen Regulasi FIA F1 2026 serta jurnal ilmiah strategi pit stop.
2. Merestrukturisasi aturan inferensi *Forward Chaining* agar konsisten dengan istilah domain Formula 1.
3. Membantu pembentukan format dokumentasi *README* dan penyusunan tabel aturan.