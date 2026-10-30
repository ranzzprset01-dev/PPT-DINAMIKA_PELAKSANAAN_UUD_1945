# 🇮🇩 Web Presentation: Dinamika Pelaksanaan UUD 1945
> **Mata Kuliah:** Pendidikan Pancasila & Kewarganegaraan  
> **Format:** Web-based Interactive Slides (15 Menu Halaman Beranimasi)  
> **Platform:** Streamlit (Python)

---

## 👥 Susunan Anggota Kelompok
1. **RANDI PRASETYO**
2. **M. SAID HAYKAL**
4. **RAGIL PRAKHOSO**
5. **M. SYAUQI ALFA ILLIYIN**
6. **HARLAND RAMADHAN**
7. **DAFFA DWI AMANDA**

---

## 🌟 Fitur Utama Aplikasi Web PPT

1. **15 Menu Slide Interaktif & Beranimasi**:
   - Transisi *fade-in-slide*, *glow pulse*, *float*, serta efek hover kartu 3D yang elegan.
   - Dilengkapi grafis replika dan ilustrasi SVG lambang negara, timbangan keadilan, gedung parlemen, naskah dekrit, diagram amandemen, serta peta konsep.
2. **Navigasi Cepat & Lengkap**:
   - Tombol *Maju* / *Mundur* per slide.
   - Pilihan Menu Cepat Dropdown (langsung lompat ke slide mana pun dari 1-15).
   - Sidebar navigasi lengkap dengan progres presentasi dan pintasan periode sejarah.
3. **Fitur Khusus Presenter (Speaker Notes)**:
   - Toggle catatan presenter di sidebar yang memberikan teks panduan dan narasi berbicara untuk anggota kelompok saat melakukan presentasi di kelas.
4. **Kuis Interaktif Interaktif**:
   - Sesi mini-quiz di bagian bawah untuk melibatkan audiens/rekan kelas setelah pemaparan.
5. **Unduh Handout Rangkuman Materi**:
   - Tombol satu-klik untuk mengunduh resume materi PPT dalam format Markdown (.md).

---

## 📑 Struktur 15 Halaman Menu Slide

- **Slide 01**: **Cover / Halaman Utama** (Judul Resmi, Mata Kuliah, & Kartu Nama Anggota Kelompok Beranimasi)
- **Slide 02**: **Peta Struktur Pembahasan** (Agenda 15 Slide dalam 3 Babak Periode Sejarah)
- **Slide 03**: **Hakikat & Kedudukan UUD 1945** (Staatsfundamentalnorm & Hukum Dasar Tertinggi)
- **Slide 04**: **Periode I: UUD 1945 Era Awal Kemerdekaan** (18 Ags 1945 - 27 Des 1949 & Sidang PPKI)
- **Slide 05**: **Dinamika & Penyimpangan Awal** (Maklumat No. X, Maklumat 3 Nov, & Maklumat 14 Nov 1945)
- **Slide 06**: **Periode II: Konstitusi RIS 1949** (KMB Den Haag, Negara Federal, & Quasi-Parlementer)
- **Slide 07**: **Dinamika & Tuntutan Kembali ke NKRI** (Penolakan Negara Boneka & Mosi Integral Natsir 1950)
- **Slide 08**: **Periode III: UUDS 1950 & Demokrasi Liberal** (Jatuh Bangun 7 Kabinet & Sukses Pemilu 1955)
- **Slide 09**: **Kebuntuan Konstituante & Dekrit Presiden 5 Juli 1959** (Hukum Darurat Staatsnoodrecht)
- **Slide 10**: **Periode IV: UUD 1945 Masa Orde Lama** (Demokrasi Terpimpin, Nasakom, & Penyimpangan Konstitusi)
- **Slide 11**: **Periode V: UUD 1945 Masa Orde Baru** (Tekad Murni & Konsekuen, Sakralisasi, & Executive Heavy)
- **Slide 12**: **Periode VI: Gelombang Amandemen UUD 1945** (4 Tahap Amandemen 1999-2002 & 5 Kesepakatan Dasar)
- **Slide 13**: **Restrukturisasi Kelembagaan Pasca Amandemen** (Lahirnya MK, DPD, KY, & Piagam HAM Pasal 28A-28J)
- **Slide 14**: **Dinamika Konstitusi di Era Kontemporer** (Etika Peradilan, Ruang Digital, & Partisipasi Publik)
- **Slide 15**: **Refleksi Nilai Pancasila & Penutup** (Sintesis Kelompok, Nilai 5 Sila, & Sesi Tanya Jawab)

---

## 🚀 Panduan Menjalankan Secara Lokal

### 1. Prasyarat
Pastikan Python sudah terinstal di komputer.

### 2. Instalasi Dependensi
Buka Terminal atau PowerShell di folder proyek ini, lalu jalankan:
```bash
pip install -r requirements.txt
```

### 3. Menjalankan Aplikasi
```bash
streamlit run app.py
```
Aplikasi web PPT akan otomatis terbuka di browser Anda pada alamat `http://localhost:8501`.

---

## ☁️ Panduan Deploy ke Streamlit Cloud (Gratis)

Agar PPT web ini dapat diakses secara online oleh dosen dan rekan kelas melalui link web:

1. **Upload ke GitHub**:
   - Buat repositori baru di akun GitHub Anda (misal: `ppt-dinamika-uud-1945`).
   - Push seluruh file proyek (`app.py`, `requirements.txt`, `.streamlit/config.toml`, `README.md`) ke repositori GitHub tersebut.
   ```bash
   git init
   git add .
   git commit -m "Inisialisasi Web PPT Dinamika UUD 1945"
   git branch -M main
   git remote add origin https://github.com/USERNAME/ppt-dinamika-uud-1945.git
   git push -u origin main
   ```

2. **Deploy di Streamlit Community Cloud**:
   - Kunjungi [share.streamlit.io](https://share.streamlit.io/) dan login dengan akun GitHub Anda.
   - Klik tombol **"New app"**.
   - Pilih repository Anda: `USERNAME/ppt-dinamika-uud-1945`.
   - Branch: `main`.
   - Main file path: `app.py`.
   - Klik **"Deploy!"**.
   - Dalam 1-2 menit, presentasi web Anda sudah aktif secara global dengan tautan publik seperti `https://dinamika-uud-1945.streamlit.app`!
