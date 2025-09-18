# 🧮 Matematika dalam Game Shinombie

## 🎯 Pengantar: Matematika itu Seru!

Halo teman-teman! Tahukah kalian bahwa di balik game Shinombie yang seru ini, tersembunyi banyak sekali konsep matematika yang keren? Mari kita jelajahi dunia matematika dalam game dengan cara yang menyenangkan! 🚀

## 📍 1. Sistem Koordinat (Posisi x, y)

### 🔍 Apa itu Koordinat?
Koordinat adalah seperti **alamat** untuk setiap objek di layar game. Setiap karakter, zombie, dan objek lainnya punya alamat unik!

### 📐 Rumus Dasar:
```
P = (x, y)

di mana:
• x ∈ ℝ = koordinat horizontal (jarak dari kiri layar)
• y ∈ ℝ = koordinat vertikal (jarak dari atas layar)
```

### 🎮 Contoh dalam Game:
```python
# Dari file ninja.py - Posisi ninja di layar
class Ninja:
    def __init__(self, sprite_folder, screen, ninja_ground, ninja_speed):
        # Posisi ninja di layar (koordinat x, y)
        self.x = 0                      # Posisi horizontal (kiri-kanan)
        self.y = self.ninja_ground      # Posisi vertikal (atas-bawah)
        
    def get_x(self):
        """Mendapatkan posisi horizontal ninja (kiri-kanan)"""
        return self.x

    def get_y(self):
        """Mendapatkan posisi vertikal ninja (atas-bawah)"""
        return self.y

# Contoh penggunaan koordinat
ninja_x = 100  # 100 pixel dari kiri
ninja_y = 200  # 200 pixel dari atas

# Posisi zombie
zombie_x = 300
zombie_y = 200
```

### 🧮 Latihan Perhitungan:
**Soal:** Jika ninja berada di posisi P₀ = (50, 150) dan bergerak Δx = 30 pixel ke kanan, di mana posisi barunya?

**Jawab:**
```
Diketahui:
P₀ = (x₀, y₀) = (50, 150)
Δx = +30, Δy = 0

Penyelesaian:
P₁ = P₀ + Δ = (x₀ + Δx, y₀ + Δy)
P₁ = (50 + 30, 150 + 0) = (80, 150)

∴ Posisi baru ninja adalah P₁ = (80, 150)
```

## 🏃 2. Kecepatan dan Gerakan

### 🔍 Konsep Kecepatan:
Kecepatan adalah seberapa cepat objek bergerak dalam waktu tertentu.

### 📐 Rumus Kecepatan:
```
v = Δd/Δt

di mana:
• v = kecepatan (velocity)
• Δd = perubahan jarak (displacement)
• Δt = perubahan waktu (time interval)

Posisi baru:
x₁ = x₀ + vₓ · Δt
y₁ = y₀ + vᵧ · Δt

di mana:
• (x₀, y₀) = posisi awal
• (x₁, y₁) = posisi akhir
• vₓ, vᵧ = komponen kecepatan pada sumbu x dan y
```

### 🎮 Contoh dalam Game:
```python
# Dari file ninja.py - Sistem kecepatan ninja
class Ninja:
    def __init__(self, sprite_folder, screen, ninja_ground, ninja_speed):
        self.ninja_speed = ninja_speed  # Seberapa cepat ninja bergerak
        self.x = 0                      # Posisi horizontal
        
    def _handle_movement_keys(self):
        """Menangani pergerakan ninja berdasarkan tombol yang ditekan"""
        keys = pygame.key.get_pressed()
        
        # Gerakan ke kiri (tombol A)
        if keys[pygame.K_a]:
            self.x -= self.ninja_speed  # x = x - ninja_speed
            self.facing_left = True
            
        # Gerakan ke kanan (tombol D)  
        if keys[pygame.K_d]:
            self.x += self.ninja_speed  # x = x + ninja_speed
            self.facing_left = False

# Contoh perhitungan kecepatan
ninja_speed = 5  # 5 pixel per frame

# Gerakan ke kanan: posisi_baru = posisi_lama + kecepatan
ninja_x = ninja_x + ninja_speed

# Gerakan ke kiri: posisi_baru = posisi_lama - kecepatan
ninja_x = ninja_x - ninja_speed
```

### 🧮 Latihan Perhitungan:
**Soal:** Ninja bergerak dengan kecepatan v = 8 pixel/frame. Dalam Δt = 10 frame, seberapa jauh ninja bergerak?

**Jawab:**
```
Diketahui:
v = 8 pixel/frame
Δt = 10 frame

Penyelesaian:
Δd = v · Δt
Δd = 8 × 10 = 80 pixel

∴ Ninja bergerak sejauh 80 pixel
```

## 🌍 3. Gravitasi dan Lompatan

### 🔍 Konsep Gravitasi:
Gravitasi membuat semua objek "jatuh" ke bawah, seperti di dunia nyata!

### 📐 Rumus Gravitasi:
```
Persamaan gerak dengan percepatan konstan:

vᵧ(t) = v₀ᵧ + g·t
y(t) = y₀ + v₀ᵧ·t + ½g·t²

di mana:
• g = 0.8 pixel/frame² (percepatan gravitasi)
• v₀ᵧ = kecepatan awal vertikal
• vᵧ(t) = kecepatan vertikal pada waktu t
• y₀ = posisi awal vertikal
• y(t) = posisi vertikal pada waktu t
```

### 🎮 Contoh Lompatan Ninja:
```python
# Dari file ninja.py - Sistem gravitasi dan lompatan
class Ninja:
    def __init__(self, sprite_folder, screen, ninja_ground, ninja_speed):
        # Pengaturan untuk melompat dan gravitasi
        self.vel_y = 0                  # Kecepatan vertikal (naik/turun)
        self.on_ground = True           # Apakah ninja sedang berdiri di tanah?
        self.jump_power = -20           # Seberapa kuat ninja melompat (minus = ke atas)
        self.gravity = 1                # Gaya gravitasi yang menarik ninja ke bawah
        
    def _handle_keydown_event(self, event):
        """Menangani tombol yang ditekan"""
        if event.key == pygame.K_w:  # Tombol W untuk melompat
            if self.on_ground:  # Jika karakter ada di tanah
                self.vel_y = self.jump_power  # Memberikan gaya lompat
                self.on_ground = False        # Karakter tidak lagi di tanah
                self.set_action('Jump')       # Set aksi ke Jump
                
    def apply_gravity(self):
        """Menambahkan gravitasi pada karakter"""
        if not self.on_ground:
            self.vel_y += self.gravity  # Menambahkan kecepatan vertikal karena gravitasi
            self.y += self.vel_y        # Posisi berubah sesuai kecepatan
            
            # Jika karakter mencapai tanah
            if self.y >= self.ninja_ground:
                self.y = self.ninja_ground  # Set posisi y agar tetap di tanah
                self.vel_y = 0              # Reset kecepatan vertikal
                self.on_ground = True       # Karakter kembali ke tanah

# Contoh perhitungan gravitasi sederhana
jump_power = -15  # Kecepatan awal ke atas (negatif karena ke atas)
gravity = 0.8     # Gravitasi ke bawah

# Setiap frame:
velocity_y = velocity_y + gravity  # vᵧ(t) = v₀ᵧ + g·t
ninja_y = ninja_y + velocity_y     # y(t) = y₀ + vᵧ·t
```

### 🧮 Latihan Perhitungan:
**Soal:** Ninja melompat dengan kecepatan awal v₀ᵧ = -12 pixel/frame. Dengan gravitasi g = 0.5 pixel/frame², berapa kecepatan ninja setelah t = 3 frame?

**Jawab:**
```
Diketahui:
v₀ᵧ = -12 pixel/frame
g = 0.5 pixel/frame²
t = 3 frame

Penyelesaian:
vᵧ(t) = v₀ᵧ + g·t
vᵧ(3) = -12 + (0.5)(3)
vᵧ(3) = -12 + 1.5 = -10.5 pixel/frame

∴ Kecepatan ninja setelah 3 frame adalah -10.5 pixel/frame
```

## 📏 4. Jarak dan Deteksi Tabrakan

### 🔍 Menghitung Jarak:
Untuk mengetahui seberapa jauh dua objek, kita gunakan **Teorema Pythagoras**!

### 📐 Rumus Jarak (Teorema Pythagoras):
```
d = ||P₂ - P₁|| = √[(x₂ - x₁)² + (y₂ - y₁)²]

di mana:
• P₁ = (x₁, y₁) ∈ ℝ² = posisi objek pertama
• P₂ = (x₂, y₂) ∈ ℝ² = posisi objek kedua
• d ∈ ℝ⁺ = jarak Euclidean antara dua titik
• ||·|| = norma Euclidean (magnitude vektor)
```

### 🎮 Contoh dalam Game:
```python
# Dari file zombie.py - Menghitung jarak untuk AI zombie
import math

class Zombie:
    def calculate_distance_to_ninja(self, ninja_x, ninja_y):
        """Menghitung jarak zombie ke ninja menggunakan teorema Pythagoras"""
        dx = ninja_x - self.x  # Selisih koordinat x
        dy = ninja_y - self.y  # Selisih koordinat y
        
        # Rumus jarak Euclidean: d = √[(Δx)² + (Δy)²]
        distance = math.sqrt(dx * dx + dy * dy)
        return distance
        
    def move_towards_ninja(self, ninja_x, ninja_y):
        """Gerakkan zombie menuju ninja"""
        distance = self.calculate_distance_to_ninja(ninja_x, ninja_y)
        
        if distance > 0:  # Hindari pembagian dengan nol
            # Normalisasi vektor arah
            dx = (ninja_x - self.x) / distance
            dy = (ninja_y - self.y) / distance
            
            # Gerakkan zombie dengan kecepatan konstan
            self.x += dx * self.zombie_speed
            self.y += dy * self.zombie_speed

# Contoh perhitungan jarak sederhana
ninja_x, ninja_y = 100, 200
zombie_x, zombie_y = 150, 250

# Menghitung jarak
dx = zombie_x - ninja_x  # Selisih x = 150 - 100 = 50
dy = zombie_y - ninja_y  # Selisih y = 250 - 200 = 50

# Jarak menggunakan Pythagoras: d = √[(Δx)² + (Δy)²]
distance = math.sqrt(dx*dx + dy*dy)
distance = math.sqrt(50*50 + 50*50) # = √5000 ≈ 70.7
```

### 🧮 Latihan Perhitungan:
**Soal:** Ninja di posisi P₁ = (60, 80) dan zombie di posisi P₂ = (90, 120). Berapa jarak mereka?

**Jawab:**
```
Diketahui:
P₁ = (x₁, y₁) = (60, 80)
P₂ = (x₂, y₂) = (90, 120)

Penyelesaian:
Δx = x₂ - x₁ = 90 - 60 = 30
Δy = y₂ - y₁ = 120 - 80 = 40

d = ||P₂ - P₁|| = √[(Δx)² + (Δy)²]
d = √[(30)² + (40)²] = √[900 + 1600] = √2500 = 50

∴ Jarak antara ninja dan zombie adalah 50 pixel
```

## 🎯 5. Trigonometri untuk Arah Proyektil

### 🔍 Konsep Sudut dan Arah:
Trigonometri membantu kita menghitung arah tembakan boss dan kunai ninja!

### 📐 Rumus Trigonometri:
```
θ = arctan(Δy/Δx) = arctan₂(Δy, Δx)

Komponen kecepatan:
vₓ = |v| · cos(θ)
vᵧ = |v| · sin(θ)

di mana:
• θ ∈ [-π, π] = sudut dalam radian
• |v| ∈ ℝ⁺ = magnitude kecepatan
• Δx = x₂ - x₁ = komponen horizontal
• Δy = y₂ - y₁ = komponen vertikal
• arctan₂ = fungsi arctangen dua argumen
```

### 🎮 Contoh Proyektil Boss:
```python
# Dari file boss_projectile.py - Sistem proyektil dengan trigonometri
import math

class BossProjectile:
    def __init__(self, screen, start_x, start_y, target_x, target_y, speed=8):
        """Inisialisasi projectile boss dengan perhitungan trigonometri"""
        self.x = start_x
        self.y = start_y
        self.speed = speed
        
        # Hitung jarak ke target menggunakan teorema Pythagoras
        distance = math.sqrt((target_x - start_x)**2 + (target_y - start_y)**2)
        
        if distance > 0:
            # Normalisasi vektor arah menggunakan trigonometri
            self.velocity_x = (target_x - start_x) / distance * speed
            self.velocity_y = (target_y - start_y) / distance * speed
        else:
            self.velocity_x = speed
            self.velocity_y = 0
            
    def update(self, ninja_x=None, ninja_y=None):
        """Update posisi projectile dengan homing menggunakan trigonometri"""
        if ninja_x is not None and ninja_y is not None:
            # Recalculate velocity menuju target baru
            distance = math.sqrt((ninja_x - self.x)**2 + (ninja_y - self.y)**2)
            if distance > 0:
                # Gunakan trigonometri untuk menghitung komponen kecepatan
                self.velocity_x = (ninja_x - self.x) / distance * self.speed
                self.velocity_y = (ninja_y - self.y) / distance * self.speed
        
        # Gerakkan projectile: posisi_baru = posisi_lama + kecepatan
        self.x += self.velocity_x  # x(t+1) = x(t) + vₓ
        self.y += self.velocity_y  # y(t+1) = y(t) + vᵧ

# Contoh perhitungan trigonometri sederhana
boss_x, boss_y = 400, 100
ninja_x, ninja_y = 200, 300

# Menghitung arah menggunakan trigonometri
dx = ninja_x - boss_x  # Δx = -200
dy = ninja_y - boss_y  # Δy = 200

# Sudut dalam radian: θ = arctan₂(Δy, Δx)
angle = math.atan2(dy, dx)

# Komponen kecepatan menggunakan trigonometri
speed = 10
projectile_vx = speed * math.cos(angle)  # vₓ = |v| · cos(θ)
projectile_vy = speed * math.sin(angle)  # vᵧ = |v| · sin(θ)
```

### 🧮 Latihan Perhitungan:
**Soal:** Boss di P₁ = (300, 100) menembak ninja di P₂ = (200, 200) dengan |v| = 8. Berapa komponen kecepatan vₓ dan vᵧ?

**Jawab:**
```
Diketahui:
P₁ = (300, 100), P₂ = (200, 200), |v| = 8

Penyelesaian:
Δx = x₂ - x₁ = 200 - 300 = -100
Δy = y₂ - y₁ = 200 - 100 = 100

d = √[(Δx)² + (Δy)²] = √[(-100)² + (100)²] = √20000 ≈ 141.42

Unit vector: û = (Δx/d, Δy/d) = (-100/141.42, 100/141.42)

vₓ = |v| · cos(θ) = 8 × (-100/141.42) ≈ -5.66
vᵧ = |v| · sin(θ) = 8 × (100/141.42) ≈ 5.66

∴ Komponen kecepatan: vₓ ≈ -5.66, vᵧ ≈ 5.66
```

## 🎲 6. Probabilitas dan Kejadian Acak

### 🔍 Konsep Probabilitas:
Probabilitas adalah peluang suatu kejadian terjadi, dinyatakan dalam persen atau desimal.

### 📐 Rumus Probabilitas:
```
P(A) = |A|/|Ω|

di mana:
• P(A) ∈ [0, 1] = probabilitas kejadian A
• |A| = kardinalitas himpunan kejadian yang diinginkan
• |Ω| = kardinalitas ruang sampel (total kemungkinan)
• 0 ≤ P(A) ≤ 1

Konversi:
P(A) = 0.3 = 30% = 3/10
```

### 🎮 Contoh dalam Game:
```python
# Dari file gameplay.py - Sistem probabilitas spawn zombie
import random

class GamePlay:
    def __init__(self):
        # Pengaturan probabilitas spawn
        self.zombie_spawn_chance = 0.02  # 2% peluang spawn per frame
        self.lightning_chance = 0.001    # 0.1% peluang petir per frame
        
    def update_zombie_spawning(self):
        """Update sistem spawn zombie berdasarkan probabilitas"""
        # Generate angka random antara 0.0 - 1.0
        random_value = random.random()
        
        # Jika angka random < peluang spawn, maka spawn zombie
        if random_value < self.zombie_spawn_chance:
            self.spawn_new_zombie()
            
    def update_weather_effects(self):
        """Update efek cuaca berdasarkan probabilitas"""
        # Peluang petir menyambar
        if random.random() < self.lightning_chance:
            self.create_lightning_effect()
            
        # Peluang hujan mulai/berhenti
        rain_change_chance = 0.005  # 0.5% peluang perubahan hujan
        if random.random() < rain_change_chance:
            self.toggle_rain()

# Contoh implementasi probabilitas sederhana
import random

# Peluang zombie spawn: P(spawn) = 2%
zombie_spawn_chance = 0.02  

# Generate angka random [0.0, 1.0)
random_number = random.random()

# Bandingkan dengan probabilitas
if random_number < zombie_spawn_chance:
    print("Zombie spawn!")  # Kejadian terjadi
else:
    print("Tidak ada zombie")  # Kejadian tidak terjadi

# Peluang petir: P(lightning) = 0.1%
lightning_chance = 0.001
if random.random() < lightning_chance:
    print("Petir menyambar!")  # Kejadian langka terjadi
```

### 🧮 Latihan Perhitungan:
**Soal:** Jika peluang zombie spawn adalah P(spawn) = 3% setiap frame, dan game berjalan f = 60 frame per detik, berapa ekspektasi zombie yang spawn dalam 1 detik?

**Jawab:**
```
Diketahui:
P(spawn) = 0.03 per frame
f = 60 frame/detik

Penyelesaian:
E[X] = P(spawn) × f
E[X] = 0.03 × 60 = 1.8 zombie/detik

∴ Ekspektasi zombie spawn per detik adalah 1.8 zombie
```

## ⚡ 7. Fisika Tumbukan

### 🔍 Konsep Tumbukan:
Ketika dua objek bertabrakan, kita perlu menghitung apa yang terjadi selanjutnya.

### 📐 Rumus Deteksi Tumbukan (AABB - Axis-Aligned Bounding Box):
```
Dua rectangle R₁ dan R₂ bertabrakan jika dan hanya jika:

(x₁ < x₂ + w₂) ∧ (x₁ + w₁ > x₂) ∧ (y₁ < y₂ + h₂) ∧ (y₁ + h₁ > y₂)

di mana:
• R₁ = {(x₁, y₁), w₁, h₁} = rectangle pertama
• R₂ = {(x₂, y₂), w₂, h₂} = rectangle kedua
• (xᵢ, yᵢ) = koordinat sudut kiri atas rectangle i
• wᵢ, hᵢ = lebar dan tinggi rectangle i
• ∧ = operator logika AND
```

### 🎮 Contoh Deteksi Tumbukan:
```python
# Dari file gameplay.py - Sistem collision detection yang sebenarnya
import pygame

class GamePlay:
    def check_zombie_collision(self, zombie, ninja):
        """Cek jika zombie menabrak ninja menggunakan pygame rect collision"""
        zombie_sprite = zombie.get_current_sprite()
        ninja_sprite = ninja.get_current_sprite()

        if ninja_sprite and zombie_sprite:
            # Buat rectangle dari sprite untuk collision detection
            zombie_rect = zombie_sprite.get_rect(topleft=(zombie.get_x(), zombie.get_y()))
            ninja_rect = ninja_sprite.get_rect(topleft=(ninja.get_x(), ninja.get_y()))

            # Perluas area serangan zombie untuk deteksi yang lebih konsisten
            attack_buffer = 20  # Buffer tambahan untuk jangkauan serangan
            zombie_attack_rect = zombie_rect.inflate(attack_buffer, attack_buffer)

            # Gunakan pygame built-in collision detection
            if zombie_attack_rect.colliderect(ninja_rect):
                return True  # Collision detected!
            return False
            
    def hit_zombie_kunais(self, zombies, ninja):
        """Deteksi tabrakan kunai dengan zombie"""
        for zombie in zombies:
            for kunai in ninja.kunais:
                # Buat rectangle untuk kunai dan zombie
                kunai_rect = kunai.get_current_sprite().get_rect(
                    topleft=(kunai.get_x(), kunai.get_y())
                )
                zombie_rect = zombie.get_current_sprite().get_rect(
                    topleft=(zombie.get_x(), zombie.get_y())
                )

                # Cek collision menggunakan pygame
                if kunai_rect.colliderect(zombie_rect):
                    if zombie.get_alive():
                        zombie.damage('Kunai')  # Berikan damage
                        ninja.kunais.remove(kunai)  # Hapus kunai

# Contoh implementasi collision detection manual
def check_collision(rect1, rect2):
    """Implementasi manual AABB collision detection"""
    return (rect1["x"] < rect2["x"] + rect2["width"] and
            rect1["x"] + rect1["width"] > rect2["x"] and
            rect1["y"] < rect2["y"] + rect2["height"] and
            rect1["y"] + rect1["height"] > rect2["y"])

# Contoh penggunaan
ninja_rect = {"x": 100, "y": 200, "width": 32, "height": 48}
zombie_rect = {"x": 120, "y": 210, "width": 32, "height": 48}

if check_collision(ninja_rect, zombie_rect):
    print("COLLISION! Ninja terkena zombie!")
```

### 🧮 Latihan Perhitungan:
**Soal:** Ninja R₁ = {(50, 100), 30, 40} dan Zombie R₂ = {(70, 110), 30, 40}. Apakah mereka bertabrakan?

**Jawab:**
```
Diketahui:
R₁ = {(x₁, y₁), w₁, h₁} = {(50, 100), 30, 40}
R₂ = {(x₂, y₂), w₂, h₂} = {(70, 110), 30, 40}

Batas rectangle:
R₁: [50, 80] × [100, 140]
R₂: [70, 100] × [110, 150]

Kondisi collision:
(x₁ < x₂ + w₂) ∧ (x₁ + w₁ > x₂) ∧ (y₁ < y₂ + h₂) ∧ (y₁ + h₁ > y₂)

Evaluasi:
(50 < 70+30) ∧ (50+30 > 70) ∧ (100 < 110+40) ∧ (100+40 > 110)
(50 < 100) ∧ (80 > 70) ∧ (100 < 150) ∧ (140 > 110)
⊤ ∧ ⊤ ∧ ⊤ ∧ ⊤ = ⊤

∴ COLLISION DETECTED! 💥
```

## 🌊 8. Gelombang dan Efek Visual

### 🔍 Konsep Gelombang:
Efek distorsi layar menggunakan fungsi sinus untuk membuat gerakan bergelombang.

### 📐 Rumus Gelombang Sinusoidal:
```
f(x) = A · sin(ωx + φ) + D

di mana:
• A ∈ ℝ⁺ = amplitudo (tinggi gelombang)
• ω ∈ ℝ⁺ = frekuensi angular (ω = 2πf)
• φ ∈ [0, 2π) = fase awal (phase shift)
• D ∈ ℝ = offset vertikal (DC component)
• f ∈ ℝ⁺ = frekuensi dalam Hz
• T = 2π/ω = periode gelombang
```

### 🎮 Contoh Efek Distorsi:
```python
# Dari file screen_distortion.py - Sistem gelombang yang sebenarnya
import pygame
import math
import random

class ScreenDistortion:
    """Kelas untuk efek distorsi layar menggunakan gelombang sinusoidal"""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.active = False
        self.duration = 0
        self.intensity = 0
        self.shake_offset_x = 0
        self.shake_offset_y = 0
        self.distortion_type = "shake"  # "shake", "wave", "zoom"
        
    def trigger_wave(self, intensity=5, duration=45):
        """Memicu efek gelombang distorsi menggunakan fungsi sinus dan cosinus"""
        self.active = True
        self.duration = 0
        self.max_duration = duration
        self.intensity = intensity
        self.distortion_type = "wave"
        
    def update(self):
        """Update efek distorsi dengan perhitungan gelombang"""
        if not self.active:
            return
            
        self.duration += 1
        
        # Hitung intensitas yang menurun seiring waktu
        progress = self.duration / self.max_duration
        current_intensity = self.intensity * (1 - progress)
        
        if self.distortion_type == "shake":
            # Efek guncangan random
            self.shake_offset_x = random.randint(-int(current_intensity), int(current_intensity))
            self.shake_offset_y = random.randint(-int(current_intensity), int(current_intensity))
            
        elif self.distortion_type == "wave":
            # Efek gelombang sinusoidal - IMPLEMENTASI RUMUS GELOMBANG!
            wave_freq = 0.3  # Frekuensi gelombang
            
            # y(t) = A × sin(ωt) untuk sumbu X
            self.shake_offset_x = int(math.sin(self.duration * wave_freq) * current_intensity)
            
            # y(t) = A × cos(ωt × 1.5) × 0.5 untuk sumbu Y (frekuensi berbeda)
            self.shake_offset_y = int(math.cos(self.duration * wave_freq * 1.5) * current_intensity * 0.5)
            
        # Matikan efek setelah durasi habis
        if self.duration >= self.max_duration:
            self.active = False
            self.shake_offset_x = 0
            self.shake_offset_y = 0

# Contoh penggunaan efek gelombang sederhana
def screen_shake_wave(time, intensity):
    """Fungsi sederhana untuk efek guncangan gelombang"""
    # Rumus gelombang: y = A × sin(ωt + φ)
    offset_x = math.sin(time * 10) * intensity      # Gelombang horizontal
    offset_y = math.cos(time * 8) * intensity * 0.7 # Gelombang vertikal (amplitudo lebih kecil)
    return offset_x, offset_y

# Contoh implementasi gelombang untuk efek air
def water_wave_effect(x, time, amplitude=5, frequency=0.1):
    """Efek gelombang air menggunakan fungsi sinus"""
    # y = A × sin(2π × f × x + ωt)
    wave_y = amplitude * math.sin(2 * math.pi * frequency * x + time)
    return wave_y
```

### 🧮 Latihan Perhitungan:
**Soal:** Dengan rumus f(x) = 5 · sin(2x), berapa nilai f(π/4)?

**Jawab:**
```
Diketahui:
f(x) = 5 · sin(2x)
x = π/4

Penyelesaian:
f(π/4) = 5 · sin(2 · π/4)
f(π/4) = 5 · sin(π/2)
f(π/4) = 5 · 1 = 5

∴ f(π/4) = 5
```

## 🎯 9. Optimasi dan Efisiensi

### 🔍 Konsep Big O Notation:
Untuk mengukur seberapa efisien algoritma kita.

### 📐 Kompleksitas Waktu:
```
Time Complexity: T(n) = O(f(n))
Space Complexity: S(n) = O(g(n))

O(1) - Konstan: Akses array
O(n) - Linear: Loop sederhana  
O(n²) - Kuadrat: Loop bersarang
O(log n) - Logaritmik: Binary search

Memory Usage: M = Σᵢ₌₁ⁿ (objectᵢ × sizeᵢ)
FPS = 1/Δt, dimana Δt = waktu per frame
```

### 🧮 Latihan Perhitungan:
**Soal:** Jika ada n = 100 zombie dan setiap zombie membutuhkan m = 50 byte memori, berapa total memori yang digunakan?

**Jawab:**
```
Diketahui:
n = 100 zombie
m = 50 byte/zombie

Penyelesaian:
M_total = n × m
M_total = 100 × 50 = 5000 byte
M_total = 5000 ÷ 1024 ≈ 4.88 KB

∴ Total memori yang digunakan ≈ 4.88 KB
```

### 🎮 Contoh Optimasi:
```python
# Dari file gameplay.py - Optimasi algoritma yang sebenarnya
class GamePlay:
    def generate_dynamic_zombie_positions(self, num_zombies=140, min_distance=80, max_distance=200):
        """Generate posisi zombie dengan kompleksitas O(n)
        
        Analisis Kompleksitas:
        - Time Complexity: O(n) dimana n = num_zombies
        - Space Complexity: O(n) untuk menyimpan positions
        """
        import random
        from constants import MAX_WIDTH

        positions = []  # O(1) space initialization
        current_x = 1000  # Mulai dari posisi 1000
        max_x = self.screen.get_width() * self.object.max_scene
        zombie_width = MAX_WIDTH

        # Set seed untuk konsistensi - O(1)
        random.seed(42)

        # Loop utama - O(n) time complexity
        while current_x < max_x and len(positions) < num_zombies:
            # Cek posisi aman - O(1) per iterasi
            if self.object._is_safe_position(current_x, zombie_width):
                positions.append(current_x)  # O(1) append
                # Tambah jarak acak - O(1)
                current_x += random.randint(min_distance, max_distance)
            else:
                current_x += 50  # O(1) increment

        return positions  # Total: O(n) time, O(n) space

    # Contoh optimasi collision detection
    def optimized_collision_check(self, zombies, ninja):
        """Collision detection yang dioptimasi
        
        Kompleksitas: O(n) dimana n = jumlah zombie
        Lebih efisien daripada O(n²) naive approach
        """
        ninja_rect = ninja.get_current_sprite().get_rect(
            topleft=(ninja.get_x(), ninja.get_y())
        )
        
        # Loop melalui zombie sekali saja - O(n)
        for zombie in zombies:  # n iterasi
            zombie_rect = zombie.get_current_sprite().get_rect(
                topleft=(zombie.get_x(), zombie.get_y())
            )
            
            # Collision check - O(1) per zombie
            if ninja_rect.colliderect(zombie_rect):
                # Handle collision - O(1)
                self.handle_collision(ninja, zombie)
                
        # Total complexity: O(n) - linear time!

# Perbandingan algoritma tidak efisien vs efisien
def inefficient_collision_check(zombies):
    """Algoritma tidak efisien - O(n²)"""
    collisions = []
    # Nested loop - n × n = n² iterasi
    for i, zombie1 in enumerate(zombies):      # n iterasi
        for j, zombie2 in enumerate(zombies):  # n iterasi untuk setiap i
            if i != j:  # Hindari self-collision
                if check_collision(zombie1, zombie2):  # O(1)
                    collisions.append((i, j))
    return collisions  # Total: O(n²) - quadratic time!

def efficient_collision_check(zombies):
    """Algoritma efisien - O(n²/2) ≈ O(n²) tapi 2x lebih cepat"""
    collisions = []
    # Hanya cek pasangan unik - mengurangi iterasi hingga 50%
    for i in range(len(zombies)):              # n iterasi
        for j in range(i+1, len(zombies)):     # (n-i-1) iterasi
            if check_collision(zombies[i], zombies[j]):  # O(1)
                collisions.append((i, j))
    return collisions  # Total: O(n²/2) - 50% lebih efisien!

# Analisis Memory Usage
def calculate_memory_usage(num_zombies, num_effects):
    """Hitung penggunaan memori game
    
    Formula: M = Σᵢ₌₁ⁿ (objectᵢ × sizeᵢ)
    """
    zombie_size = 50    # byte per zombie
    effect_size = 20    # byte per effect
    ninja_size = 100    # byte untuk ninja
    
    # M_total = M_zombies + M_effects + M_ninja
    total_memory = (num_zombies * zombie_size + 
                   num_effects * effect_size + 
                   ninja_size)
    
    return total_memory  # bytes

# Contoh penggunaan
zombies_count = 140
effects_count = 50
memory_used = calculate_memory_usage(zombies_count, effects_count)
print(f"Total memory: {memory_used} bytes = {memory_used/1024:.2f} KB")
# Output: Total memory: 8100 bytes = 7.91 KB
```

## 🏆 10. Statistik Game

### 🔍 Konsep Statistik:
Menghitung rata-rata, maksimum, minimum dari data game.

### 📐 Rumus Statistik:
```
Mean (μ): μ = (1/n) × Σᵢ₌₁ⁿ xᵢ
Variance: σ² = (1/n) × Σᵢ₌₁ⁿ (xᵢ - μ)²
Standard Deviation: σ = √σ²
Maximum: max(X) = max{x₁, x₂, ..., xₙ}
Minimum: min(X) = min{x₁, x₂, ..., xₙ}
```

### 🧮 Latihan Perhitungan:
**Soal:** Pemain bermain n = 5 kali dengan skor X = {100, 150, 200, 120, 180}. Berapa rata-rata skornya?

**Jawab:**
```
Diketahui:
X = {x₁, x₂, x₃, x₄, x₅} = {100, 150, 200, 120, 180}
n = 5

Penyelesaian:
μ = (1/n) × Σᵢ₌₁ⁿ xᵢ
μ = (1/5) × (100 + 150 + 200 + 120 + 180)
μ = (1/5) × 750 = 150

∴ Rata-rata skor adalah μ = 150
```

### 🎮 Contoh Statistik Score:
```python
# Dari file gameplay.py - Sistem scoring yang sebenarnya
class GamePlay:
    def __init__(self):
        self.score = 0  # Skor pemain (bertambah 5 setiap membunuh zombie)
        self.boss_trigger_score = 300  # Score untuk memicu boss fight
        
    def add_score(self, points=5):
        """Tambah skor pemain dengan statistik"""
        self.score += points
        
    def get_game_statistics(self):
        """Hitung statistik game menggunakan rumus matematika"""
        # Data kesehatan karakter
        ninja_health = 100  # Kesehatan ninja maksimal
        zombie_health = 100  # Kesehatan zombie
        boss_health = 500   # Kesehatan boss maksimal
        
        # Hitung rata-rata kesehatan semua karakter
        health_data = [ninja_health, zombie_health, boss_health]
        n = len(health_data)
        
        # μ = (1/n) × Σᵢ₌₁ⁿ xᵢ
        average_health = sum(health_data) / n  # μ = 233.33
        
        # max(X) dan min(X)
        max_health = max(health_data)  # max = 500 (boss)
        min_health = min(health_data)  # min = 100 (ninja/zombie)
        
        # Variance: σ² = (1/n) × Σᵢ₌₁ⁿ (xᵢ - μ)²
        variance = sum((x - average_health)**2 for x in health_data) / n
        std_deviation = variance**0.5  # σ ≈ 188.56
        
        return {
            'average_health': average_health,
            'max_health': max_health,
            'min_health': min_health,
            'std_deviation': std_deviation,
            'current_score': self.score
        }

# Contoh implementasi statistik skor pemain
class ScoreTracker:
    def __init__(self):
        self.scores_history = []  # Riwayat skor pemain
        
    def add_game_score(self, final_score):
        """Tambah skor akhir game ke riwayat"""
        self.scores_history.append(final_score)
        
    def calculate_player_statistics(self):
        """Hitung statistik performa pemain"""
        if not self.scores_history:
            return None
            
        scores = self.scores_history
        n = len(scores)
        
        # Rata-rata skor: μ = (1/n) × Σᵢ₌₁ⁿ xᵢ
        average_score = sum(scores) / n
        
        # Skor tertinggi dan terendah
        high_score = max(scores)  # max(X)
        low_score = min(scores)   # min(X)
        
        # Standar deviasi: σ = √[(1/n) × Σᵢ₌₁ⁿ (xᵢ - μ)²]
        variance = sum((score - average_score)**2 for score in scores) / n
        std_dev = variance**0.5
        
        return {
            'games_played': n,
            'average_score': round(average_score, 2),
            'high_score': high_score,
            'low_score': low_score,
            'std_deviation': round(std_dev, 2)
        }

# Contoh penggunaan
tracker = ScoreTracker()
tracker.scores_history = [1200, 1500, 900, 1800, 1100]  # Data skor
stats = tracker.calculate_player_statistics()
print(f"Rata-rata: {stats['average_score']}")  # μ = 1300
print(f"Tertinggi: {stats['high_score']}")      # max = 1800
print(f"Terendah: {stats['low_score']}")        # min = 900
print(f"Std Dev: {stats['std_deviation']}")     # σ ≈ 307.79
```

## 🎓 Kesimpulan: Matematika itu Keren!

Wah, ternyata banyak sekali matematika yang tersembunyi dalam game Shinombie! Dari koordinat Kartesius sampai analisis kompleksitas algoritma, semuanya bekerja sama untuk menciptakan pengalaman gaming yang seru.

### 🌟 Yang Sudah Kita Pelajari:
1. **Koordinat Kartesius** - P(x,y) ∈ ℝ²
2. **Kinematika** - v⃗ = dr⃗/dt, a⃗ = dv⃗/dt
3. **Gravitasi** - F⃗ = mg⃗, y(t) = y₀ + v₀t + ½gt²
4. **Geometri Euclidean** - d = √[(Δx)² + (Δy)²]
5. **Trigonometri** - θ = arctan₂(Δy, Δx)
6. **Teori Probabilitas** - P(A) ∈ [0,1], E[X], σ²
7. **Geometri Komputasi** - AABB collision detection
8. **Analisis Fourier** - f(t) = A·sin(ωt + φ)
9. **Kompleksitas Algoritma** - O(n), Θ(n), Ω(n)
10. **Statistik Deskriptif** - μ, σ, max, min

### 🚀 Tips untuk Belajar Lebih Lanjut:
1. **Praktik** - Coba ubah parameter dalam persamaan dan observasi hasilnya
2. **Eksperimen** - Implementasikan fungsi matematika baru
3. **Visualisasi** - Plot grafik untuk memahami behavior fungsi
4. **Rigor** - Pelajari notasi matematika formal

Matematika bukan hanya simbol-simbol abstrak, tapi foundation yang kokoh untuk computational thinking! ∀ concept ∈ Mathematics → ∃ application ∈ GameDevelopment 🎮✨

---

*"Mathematica est lingua qua Deus universum scripsit"* - Galileo Galilei  
*"Matematika adalah bahasa yang digunakan Tuhan untuk menulis alam semesta"* 🌟

### 📚 Notasi Matematika yang Digunakan:
- ∀ (untuk semua), ∃ (ada), ∈ (elemen dari), ∉ (bukan elemen dari)
- ∑ (sigma - penjumlahan), ∏ (pi - perkalian), ∫ (integral)
- √ (akar kuadrat), ∞ (tak hingga), ∅ (himpunan kosong)
- ≈ (hampir sama dengan), ≡ (identik dengan), ≠ (tidak sama dengan)
- ∴ (oleh karena itu), ∵ (karena), ⟹ (implikasi)
- ⊤ (benar), ⊥ (salah), ∧ (dan), ∨ (atau), ¬ (negasi)
- θ (theta), π (pi ≈ 3.14159), e (≈ 2.71828), φ (phi ≈ 1.618)
- Δ (delta - perubahan), ∂ (partial derivative), ∇ (nabla)