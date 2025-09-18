# 🏗️ Class Diagram Game Shinombie

## 📋 Penjelasan Class Diagram

Class diagram adalah seperti **peta** yang menunjukkan bagaimana semua bagian dalam program kita saling berhubungan. Bayangkan seperti denah rumah yang menunjukkan di mana letak kamar, dapur, dan ruang tamu!

Dalam game Shinombie, kita punya banyak "kelas" (class) yang masing-masing punya tugas khusus, seperti:
- Kelas Ninja (untuk karakter utama)
- Kelas Zombie (untuk musuh)
- Kelas Boss (untuk musuh besar)
- Dan masih banyak lagi!

## 🎯 Class Diagram Utama Game Shinombie

```mermaid
classDiagram
    class GamePlay {
        +screen: Surface
        +clock: Clock
        +ninja: Ninja
        +zombies: List
        +boss: Boss
        +kunais: List
        +score: int
        +level: int
        +run_game()
        +handle_events()
        +update_game()
        +draw_everything()
        +check_collisions()
    }
    
    class Ninja {
        +x: int
        +y: int
        +health: int
        +speed: int
        +is_jumping: bool
        +animation_frames: List
        +move_left()
        +move_right()
        +jump()
        +attack()
        +take_damage()
        +update_animation()
    }
    
    class Zombie {
        +x: int
        +y: int
        +health: int
        +speed: int
        +target_x: int
        +target_y: int
        +is_dead: bool
        +move_towards_ninja()
        +attack_ninja()
        +take_damage()
        +die()
        +update_animation()
    }
    
    class Boss {
        +x: int
        +y: int
        +health: int
        +max_health: int
        +attack_power: int
        +projectiles: List
        +attack_ninja()
        +shoot_projectile()
        +take_damage()
        +update_ai()
        +draw_health_bar()
    }
    
    class Kunai {
        +x: int
        +y: int
        +velocity_x: int
        +velocity_y: int
        +damage: int
        +is_active: bool
        +update_position()
        +check_bounds()
        +hit_target()
    }
    
    class BossProjectile {
        +x: int
        +y: int
        +velocity_x: int
        +velocity_y: int
        +damage: int
        +update_position()
        +explode()
    }
    
    class BloodTrail {
        +trails: Dict
        +add_blood_drop()
        +update_trails()
        +cleanup_zombie()
        +render()
        +clear_all()
    }
    
    class ScreenDistortion {
        +shake_intensity: int
        +wave_intensity: int
        +shake_duration: int
        +apply_shake()
        +apply_wave()
        +update()
        +reset()
    }
    
    class RainEffect {
        +raindrops: List
        +intensity: int
        +create_raindrop()
        +update_rain()
        +draw_rain()
    }
    
    class LightningEffect {
        +is_active: bool
        +duration: int
        +brightness: int
        +strike()
        +update()
        +draw_flash()
    }
    
    class HorrorSounds {
        +ambient_sounds: List
        +zombie_sounds: List
        +play_ambient()
        +play_zombie_growl()
        +play_attack_sound()
        +stop_all()
    }
    
    class WeatherSounds {
        +rain_sound: Sound
        +thunder_sounds: List
        +play_rain()
        +play_thunder()
        +stop_rain()
    }
    
    %% Hubungan antar kelas
    GamePlay ||--o{ Ninja : "memiliki 1"
    GamePlay ||--o{ Zombie : "memiliki banyak"
    GamePlay ||--o| Boss : "memiliki 0-1"
    GamePlay ||--o{ Kunai : "memiliki banyak"
    GamePlay ||--o| BloodTrail : "menggunakan"
    GamePlay ||--o| ScreenDistortion : "menggunakan"
    GamePlay ||--o| RainEffect : "menggunakan"
    GamePlay ||--o| LightningEffect : "menggunakan"
    GamePlay ||--o| HorrorSounds : "menggunakan"
    GamePlay ||--o| WeatherSounds : "menggunakan"
    
    Boss ||--o{ BossProjectile : "menembakkan"
    Ninja ||--o{ Kunai : "melemparkan"
    Zombie ||--o| BloodTrail : "meninggalkan jejak"
```

## 🔍 Penjelasan Hubungan Antar Kelas

### 1. **GamePlay (Kelas Utama) 🎮**
Ini adalah "sutradara" dari seluruh game! Kelas ini:
- Mengatur semua kelas lainnya
- Menjalankan game loop (perulangan game)
- Menangani input dari pemain
- Menggambar semua objek ke layar

### 2. **Ninja (Karakter Utama) 🥷**
Kelas ini mengatur:
- Posisi ninja di layar (x, y)
- Gerakan (kiri, kanan, lompat)
- Animasi ninja
- Nyawa dan kesehatan
- Serangan dengan kunai

### 3. **Zombie (Musuh) 🧟**
Kelas ini mengatur:
- Posisi zombie
- Gerakan mengejar ninja
- Animasi zombie
- Serangan ke ninja
- Kematian zombie

### 4. **Boss (Musuh Besar) 👹**
Kelas ini mengatur:
- Boss yang lebih kuat dari zombie biasa
- Serangan khusus dengan proyektil
- Health bar (bar kesehatan)
- AI (kecerdasan buatan) yang lebih kompleks

### 5. **Kunai (Senjata Ninja) 🗡️**
Kelas ini mengatur:
- Proyektil yang dilempar ninja
- Gerakan kunai di udara
- Damage (kerusakan) yang diberikan
- Deteksi tabrakan dengan musuh

### 6. **Efek Visual dan Suara 🎨🔊**
Kelas-kelas ini membuat game lebih hidup:
- **BloodTrail**: Jejak darah zombie
- **ScreenDistortion**: Efek guncangan layar
- **RainEffect**: Efek hujan
- **LightningEffect**: Efek petir
- **HorrorSounds**: Suara menakutkan
- **WeatherSounds**: Suara cuaca

## 🧩 Cara Kerja Hubungan Kelas

### Analogi Rumah 🏠
Bayangkan game seperti sebuah rumah:
- **GamePlay** = Arsitek yang mengatur semua ruangan
- **Ninja** = Penghuni utama rumah
- **Zombie** = Tamu tidak diundang yang masuk
- **Boss** = Pencuri besar yang berbahaya
- **Kunai** = Alat pertahanan
- **Efek** = Dekorasi dan suasana rumah

### Hubungan "Memiliki" (Has-A) 📦
- GamePlay **memiliki** 1 Ninja
- GamePlay **memiliki** banyak Zombie
- GamePlay **memiliki** 0 atau 1 Boss
- Ninja **memiliki** banyak Kunai
- Boss **memiliki** banyak Proyektil

### Hubungan "Menggunakan" (Uses-A) 🔧
- GamePlay **menggunakan** BloodTrail untuk efek darah
- GamePlay **menggunakan** ScreenDistortion untuk efek guncangan
- GamePlay **menggunakan** berbagai efek suara dan visual

## 🎯 Mengapa Class Diagram Penting?

1. **Organisasi Kode** 📚
   - Membantu kita mengatur kode dengan rapi
   - Setiap kelas punya tugas yang jelas

2. **Mudah Dipahami** 🧠
   - Programmer lain bisa dengan mudah memahami struktur kode
   - Seperti peta yang memudahkan navigasi

3. **Mudah Dikembangkan** 🚀
   - Kalau mau menambah fitur baru, kita tahu di mana harus meletakkannya
   - Bisa menambah kelas baru tanpa merusak yang sudah ada

4. **Debugging Lebih Mudah** 🐛
   - Kalau ada bug, kita tahu harus mencari di kelas mana
   - Hubungan antar kelas membantu melacak masalah

## 🎓 Pelajaran untuk Anak-Anak

Dari class diagram ini, kalian bisa belajar:

1. **Pemecahan Masalah** 🧩
   - Masalah besar (membuat game) dipecah jadi bagian-bagian kecil (kelas-kelas)

2. **Organisasi** 📋
   - Setiap bagian punya tugas dan tanggung jawab masing-masing

3. **Kerja Sama** 🤝
   - Semua kelas bekerja sama untuk membuat game yang utuh

4. **Perencanaan** 📝
   - Sebelum coding, kita merencanakan struktur dulu

Class diagram adalah fondasi yang kuat untuk membangun program yang besar dan kompleks! 🏗️✨