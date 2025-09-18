# 🥷 Game Shinombie - Petualangan Ninja Melawan Zombie!

## 🎮 Apa itu Game Shinombie?

Halo teman-teman! Selamat datang di dunia **Shinombie** - sebuah game seru di mana kamu akan berperan sebagai ninja keren yang harus melawan gerombolan zombie jahat! 

Game ini dibuat menggunakan bahasa pemrograman **Python** dan library **Pygame**. Dengan bermain game ini, kamu tidak hanya bersenang-senang, tapi juga belajar konsep-konsep matematika dan pemrograman yang keren!

## 🌟 Fitur-Fitur Keren dalam Game

### 1. 🥷 Karakter Ninja
- Ninja bisa bergerak ke kiri, kanan, melompat, dan menyerang
- Ada ninja laki-laki dan perempuan yang bisa dipilih
- Ninja punya nyawa dan bisa terluka kalau diserang zombie

### 2. 🧟 Zombie yang Menakutkan
- Zombie bergerak secara otomatis mengejar ninja
- Ada zombie laki-laki dan perempuan
- Zombie meninggalkan jejak darah saat bergerak (efek visual keren!)
- Zombie mengeluarkan suara menakutkan

### 3. 👹 Boss Monster
- Boss adalah musuh yang sangat kuat
- Boss bisa menembakkan proyektil ke ninja
- Boss punya animasi dan suara khusus

### 4. 🌦️ Efek Cuaca
- Hujan dengan suara yang realistis
- Petir yang menyambar secara acak
- Efek visual yang membuat game lebih hidup

### 5. 💥 Efek Visual Keren
- Distorsi layar saat diserang
- Efek ledakan dan percikan api
- Efek daun berguguran
- Efek bayangan bergerak

### 6. 🎵 Efek Suara
- Suara hujan dan petir
- Suara zombie yang menakutkan
- Efek suara serangan dan ledakan

## 🎯 Cara Bermain

1. **Gerakan Ninja:**
   - Panah kiri/kanan: Bergerak
   - Spasi: Melompat
   - Tombol serangan: Menyerang zombie

2. **Tujuan:**
   - Kalahkan semua zombie di setiap level
   - Hindari serangan zombie dan boss
   - Bertahan hidup selama mungkin

3. **Tips:**
   - Gunakan kunai (senjata ninja) untuk menyerang dari jarak jauh
   - Manfaatkan lompatan untuk menghindari serangan
   - Perhatikan pola serangan boss

## 🧮 Matematika dalam Game

Game ini menggunakan banyak konsep matematika yang menarik:

### 1. **Koordinat dan Posisi (x, y)**
- Setiap objek di game punya posisi x (horizontal) dan y (vertikal)
- Contoh: Ninja di posisi (100, 200) artinya 100 pixel dari kiri, 200 pixel dari atas

### 2. **Kecepatan dan Percepatan**
- Ninja bergerak dengan kecepatan tertentu (pixel per detik)
- Gravitasi membuat ninja jatuh ke bawah dengan percepatan

### 3. **Deteksi Tabrakan**
- Menggunakan rumus matematika untuk mengecek apakah dua objek bertabrakan
- Penting untuk gameplay (ninja vs zombie, kunai vs zombie, dll)

### 4. **Trigonometri**
- Digunakan untuk menghitung arah proyektil boss
- Efek visual seperti gerakan melingkar

### 5. **Probabilitas**
- Spawn zombie secara acak
- Efek cuaca yang muncul dengan peluang tertentu

## 🏗️ Struktur Project

Project ini terdiri dari beberapa file Python:

- `main.py` - File utama untuk menjalankan game
- `gameplay.py` - Logika utama permainan
- `ninja.py` - Kelas untuk karakter ninja
- `zombie.py` - Kelas untuk zombie
- `boss.py` - Kelas untuk boss monster
- `kunai.py` - Senjata ninja
- `rain_effect.py` - Efek hujan
- `lightning_effect.py` - Efek petir
- `blood_trail.py` - Efek jejak darah
- `screen_distortion.py` - Efek distorsi layar
- `horror_sounds.py` - Efek suara horor
- `weather_sounds.py` - Efek suara cuaca
- Dan masih banyak lagi!

## 🎓 Apa yang Bisa Dipelajari?

### Pemrograman:
- **Object-Oriented Programming (OOP)** - Membuat kelas dan objek
- **Game Loop** - Cara kerja game secara berulang
- **Event Handling** - Menangani input dari keyboard
- **Collision Detection** - Deteksi tabrakan antar objek
- **Animation** - Membuat animasi karakter

### Matematika:
- **Sistem Koordinat** - Posisi x dan y
- **Vektor** - Arah dan kecepatan
- **Trigonometri** - Sin, cos untuk gerakan melingkar
- **Probabilitas** - Kejadian acak dalam game
- **Geometri** - Bentuk dan ukuran objek

### Fisika:
- **Gravitasi** - Benda jatuh ke bawah
- **Momentum** - Gerakan dan kecepatan
- **Tumbukan** - Apa yang terjadi saat objek bertabrakan

## 🚀 Cara Menjalankan Game

1. Pastikan Python sudah terinstall di komputer
2. Install pygame dengan perintah: `pip install pygame`
3. Jalankan game dengan: `python3 main.py`
4. Selamat bermain!

## 🎉 Kesimpulan

Game Shinombie adalah contoh sempurna bagaimana pemrograman dan matematika bisa digabungkan untuk membuat sesuatu yang menyenangkan! Dengan mempelajari kode game ini, teman-teman bisa:

- Memahami konsep dasar pemrograman
- Belajar matematika dengan cara yang seru
- Mengembangkan kreativitas dalam membuat game
- Memahami bagaimana teknologi bekerja di balik layar

Selamat belajar dan bersenang-senang dengan coding! 🎮✨

---

*Game ini dibuat sebagai project pembelajaran dalam buku "Jadi Keren Dengan Coding" - Python untuk Anak-Anak*