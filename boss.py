# File untuk karakter boss (musuh utama ninja)
# File ini mengatur bagaimana boss bergerak, menyerang, dan berinteraksi

import os, re, math, random, pygame  # Library untuk membuat game
from helper import resize_with_aspect_ratio  # Fungsi untuk mengubah ukuran gambar
from constants import MAX_WIDTH, MAX_HEIGHT  # Ukuran layar game
from boss_projectile import BossProjectile  # Import class projectile boss

class Boss:
    """Kelas Boss - Cetakan untuk membuat karakter boss

    Boss adalah musuh utama ninja yang akan bertarung di scene akhir.
    Boss memiliki health bar, berbagai serangan.
    """
    def __init__(self, sprite_folder, screen, boss_ground, boss_speed, init_pos):
        """Membuat boss baru

        Parameter:
        - sprite_folder: Folder tempat gambar boss
        - screen: Layar game
        - boss_ground: Tinggi tanah tempat boss berdiri
        - boss_speed: Seberapa cepat boss bergerak
        - init_pos: Posisi awal boss
        """
        # Kamus untuk menyimpan semua gerakan boss
        self.actions = {
            'Idle': [],              # Gambar saat boss diam
            'Idle Blinking': [],     # Gambar saat boss berkedip
            'Walking': [],           # Gambar saat boss berjalan
            'Running': [],           # Gambar saat boss berlari
            'Slashing': [],          # Gambar saat boss menyerang dengan pedang
            'Kicking': [],           # Gambar saat boss menendang
            'Throwing': [],          # Gambar saat boss melempar
            'Run Slashing': [],      # Gambar saat boss berlari sambil menyerang
            'Run Throwing': [],      # Gambar saat boss berlari sambil melempar
            'Slashing in The Air': [], # Gambar saat boss menyerang di udara
            'Throwing in The Air': [], # Gambar saat boss melempar di udara
            'Jump Start': [],        # Gambar saat boss mulai melompat
            'Jump Loop': [],         # Gambar saat boss di udara
            'Sliding': [],           # Gambar saat boss meluncur
            'Falling Down': [],      # Gambar saat boss jatuh
            'Hurt': [],              # Gambar saat boss terkena serangan
            'Dying': [],             # Gambar saat boss mati
        }

        self.boss_speed = boss_speed  # Seberapa cepat boss bergerak
        self.screen = screen  # Layar tempat boss muncul
        self.current_action = 'Idle'  # Gerakan yang sedang dilakukan (mulai dengan Idle)
        self.current_frame = 0  # Frame animasi yang sedang ditampilkan
        self.boss_ground = boss_ground  # Tinggi tanah tempat boss berdiri
        self.load_sprites(sprite_folder)  # Muat semua gambar boss

        # Posisi boss di layar (x = kiri-kanan, y = atas-bawah)
        self.init_pos = init_pos  # Posisi awal boss
        self.relative_x = self.init_pos  # Posisi relatif boss
        self.x = self.init_pos + self.relative_x  # Posisi X boss di layar
        self.y = self.boss_ground  # Posisi Y boss (tinggi tanah)

        # Arah gerakan boss
        self.facing_left = True  # Boss menghadap kiri (True) atau kanan (False)
        self.max_health = 500  # Nyawa maksimal boss (500 = sangat kuat)
        self.health = self.max_health  # Nyawa boss saat ini

        # Pengaturan animasi boss
        self.frame_update_time = 0.05  # Seberapa cepat animasi berubah (0.05 detik untuk gerakan lebih smooth)
        self.last_frame_update = pygame.time.get_ticks()  # Kapan terakhir animasi berubah

        # Status boss saat bertarung
        self.is_hit = False  # Apakah boss sedang terkena serangan
        self.alive = True  # Apakah boss masih hidup
        self.is_jumping = False  # Apakah boss sedang melompat
        self.jump_velocity = 0  # Kecepatan lompat boss
        self.gravity = 0.8  # Gravitasi untuk lompat boss

        # Pengaturan kematian boss
        self.death_time = None  # Kapan boss mati
        self.death_duration = 3000  # Berapa lama boss mati sebelum hilang (3 detik)

        # Boss
        self.attack_cooldown = 0  # Waktu tunggu sebelum bisa menyerang lagi
        self.max_attack_cooldown = 15  # Maksimal waktu tunggu (15 frame = 0.25 detik) - lebih agresif
        self.attack_range = 220  # Jarak serangan boss - diperluas agar bisa menyerang sambil mengejar
        self.detection_range = 400  # Jarak deteksi ninja - diperluas
        self.close_range = 80  # Jarak dekat untuk serangan intense
        self.last_attack_time = 0  # Kapan terakhir boss menyerang

        # Pola serangan boss
        self.attack_patterns = ['Slashing', 'Kicking', 'Throwing', 'Run Slashing']
        self.current_pattern_index = 0

        # Health bar boss
        self.health_bar_width = 400
        self.health_bar_height = 20
        self.health_bar_x = (screen.get_width() - self.health_bar_width) // 2
        self.health_bar_y = 50

        # Projectile system
        self.projectiles = []  # Daftar projectile yang aktif
        self.throwing_frame_trigger = 3  # Frame ke-3 dari animasi throwing untuk spawn projectile

    def load_sprites(self, sprite_folder):
        """Memuat semua gambar sprite boss dari folder"""
        for action_name in self.actions.keys():
            action_folder = os.path.join(sprite_folder, action_name)
            if os.path.exists(action_folder):
                # Ambil semua file PNG dalam folder action
                sprite_files = [f for f in os.listdir(action_folder) if f.endswith('.png')]
                sprite_files.sort()  # Urutkan file berdasarkan nama

                for sprite_file in sprite_files:
                    sprite_path = os.path.join(action_folder, sprite_file)
                    try:
                        sprite = pygame.image.load(sprite_path).convert_alpha()
                        # Resize sprite boss agar lebih besar dari zombie biasa
                        sprite_resized = resize_with_aspect_ratio(sprite, MAX_WIDTH * 1.5, MAX_HEIGHT * 1.5)
                        self.actions[action_name].append(sprite_resized)
                    except pygame.error as e:
                        print(f"Error loading sprite {sprite_path}: {e}")

    def get_current_sprite(self):
        """Mengambil sprite yang sedang ditampilkan"""
        if self.current_action in self.actions and self.actions[self.current_action]:
            return self.actions[self.current_action][self.current_frame]
        return None

    def get_relative_x(self):
        """Mengambil posisi relatif boss"""
        return self.relative_x

    def get_x(self):
        """Mengambil posisi X boss (kiri-kanan)"""
        return self.x

    def get_y(self):
        """Mengambil posisi Y boss (atas-bawah)"""
        return self.y

    def get_alive(self):
        """Cek apakah boss masih hidup"""
        return self.alive

    def set_alive(self, alive):
        """Mengatur status hidup/mati boss"""
        self.alive = alive

    def set_action(self, action):
        """Set aksi boss dan reset frame"""
        if action in self.actions and action != self.current_action:
            self.current_action = action
            self.current_frame = 0

    def damage(self, damage_amount=20):
        """Boss menerima damage"""
        if not self.alive:
            return

        self.health -= damage_amount
        self.is_hit = True

        # Set action ke Hurt jika tidak sedang mati
        if self.health > 0:
            self.set_action('Hurt')
        else:
            self.set_action('Dying')
            self.set_dead()

    def set_dead(self):
        """Boss mati"""
        if self.alive:
            self.set_action('Dying')
            self.alive = False
            self.death_time = pygame.time.get_ticks()

    def is_ready_to_remove(self):
        """Cek apakah boss sudah siap untuk dihapus"""
        if self.death_time is not None:
            current_time = pygame.time.get_ticks()
            if current_time - self.death_time >= self.death_duration:
                return True
        return False

    def get_distance_to_ninja(self, ninja_x, ninja_y):
        """Hitung jarak ke ninja"""
        dx = self.x - ninja_x
        dy = self.y - ninja_y
        return math.sqrt(dx*dx + dy*dy)

    def choose_attack_pattern(self, distance_to_ninja):
        """Pilih pola serangan berdasarkan jarak ke ninja"""
        if distance_to_ninja <= 80:  # Jarak dekat
            return random.choice(['Slashing', 'Kicking'])
        elif distance_to_ninja <= 150:  # Jarak sedang
            return random.choice(['Run Slashing', 'Throwing'])
        else:  # Jarak jauh
            return 'Running'  # Mendekat ke ninja

    def is_animation_complete(self):
        """Cek apakah animasi saat ini sudah selesai satu cycle"""
        if self.current_action in self.actions and self.actions[self.current_action]:
            return self.current_frame >= len(self.actions[self.current_action]) - 1
        return True

    def update_frame(self, road_x, ninja_x, ninja_y):
        """Update frame animasi dan boss"""
        current_time = pygame.time.get_ticks()

        # Update posisi absolut boss
        self.x = road_x + self.relative_x

        # Jika boss mati, hanya update animasi dying
        if not self.alive:
            if current_time - self.last_frame_update >= self.frame_update_time * 1000:
                if self.current_action == 'Dying':
                    if self.current_frame < len(self.actions['Dying']) - 1:
                        self.current_frame += 1
                self.last_frame_update = current_time
            return

        # Update semua projectile (tanpa homing)
        self.update_projectiles()

        # Hitung jarak ke ninja
        distance_to_ninja = self.get_distance_to_ninja(ninja_x, ninja_y)

        # Tentukan arah menghadap berdasarkan posisi ninja
        # Kurangi frekuensi perubahan arah saat ninja sangat dekat untuk menghindari kebingungan
        if distance_to_ninja > self.close_range or abs(ninja_x - self.x) > 50:
            if ninja_x < self.x and ninja_x < self.x - 20:  # Tambah threshold untuk mengurangi flicker
                self.facing_left = True
            elif ninja_x > self.x and ninja_x > self.x + 20:  # Tambah threshold untuk mengurangi flicker
                self.facing_left = False

        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Cek apakah sedang dalam animasi movement yang belum selesai
        is_movement_animation = self.current_action in ['Running']
        animation_not_complete = not self.is_animation_complete()

        # Cek apakah sedang dalam animasi throwing yang belum selesai
        is_throwing_animation = self.current_action in ['Throwing', 'Run Throwing']
        throwing_not_complete = is_throwing_animation and self.current_frame < self.throwing_frame_trigger

        # pilih action berdasarkan situasi
        if self.is_hit:
            # Jika sedang terkena serangan, tetap di action Hurt sampai selesai
            if self.current_action == 'Hurt':
                if self.current_frame >= len(self.actions['Hurt']) - 1:
                    self.is_hit = False
                    self.set_action('Idle')
        elif throwing_not_complete:
            # Jika sedang throwing dan belum mencapai frame trigger, jangan ganti action
            # Tetap di throwing action sampai projectile di-spawn
            pass
        elif distance_to_ninja <= self.detection_range:
            # Ninja terdeteksi, bergerak mendekat dan menyerang secara agresif

            # Jika sedang dalam animasi movement dan belum selesai, tunggu sampai selesai
            if is_movement_animation and animation_not_complete:
                # Tetap bergerak sesuai action saat ini
                if self.current_action == 'Running':
                    if ninja_x < self.x:
                        self.relative_x -= self.boss_speed * 2.0
                    else:
                        self.relative_x += self.boss_speed * 2.0
            else:
                # Animasi selesai atau bukan movement animation, bisa ganti action
                if distance_to_ninja > self.attack_range:
                    # Terlalu jauh, mendekat ke ninja dengan kemungkinan serangan sambil berlari
                    if distance_to_ninja > 250:
                        # Boss bisa menyerang sambil berlari dari jarak jauh - gunakan projectile
                        if self.attack_cooldown <= 0 and random.randint(1, 4) == 1:  # 25% chance
                            self.set_action('Run Throwing')  # Gunakan projectile saat berlari
                            self.attack_cooldown = self.max_attack_cooldown
                        else:
                            self.set_action('Running')
                        # Bergerak menuju ninja dengan cepat
                        if ninja_x < self.x:
                            self.relative_x -= self.boss_speed * 1.0
                        else:
                            self.relative_x += self.boss_speed * 1.0
                    else:
                        # Jarak menengah - pilih serangan berdasarkan jarak
                        if self.attack_cooldown <= 0 and random.randint(1, 3) == 1:  # 33% chance
                            if distance_to_ninja > 200:
                                self.set_action('Run Throwing')  # Projectile untuk jarak menengah-jauh
                            else:
                                self.set_action('Run Slashing')  # Pedang untuk jarak menengah-dekat
                            self.attack_cooldown = self.max_attack_cooldown
                        else:
                            self.set_action('Running')
                        # Bergerak menuju ninja
                        if ninja_x < self.x:
                            self.relative_x -= self.boss_speed * 0.8
                        else:
                            self.relative_x += self.boss_speed * 0.8
                else:
                    # Dalam jangkauan serangan - boss menyerang berdasarkan jarak!
                    if self.attack_cooldown <= 0 and self.current_action not in self.attack_patterns:
                        # Strategi berdasarkan jarak:
                        # - Jarak jauh (>200): Gunakan projectile (Throwing)
                        # - Jarak dekat (<=200): Gunakan serangan pedang (Slashing, Kicking)
                        if distance_to_ninja > 200:
                            # Jarak jauh - gunakan projectile
                            attack_actions = ['Throwing', 'Run Throwing']
                            chosen_attack = random.choice(attack_actions)
                        else:
                            # Jarak dekat - gunakan serangan pedang
                            attack_actions = ['Slashing', 'Run Slashing', 'Kicking']
                            chosen_attack = random.choice(attack_actions)

                        self.set_action(chosen_attack)
                        self.attack_cooldown = self.max_attack_cooldown
                    elif self.current_action not in self.attack_patterns:
                        # Tetap mengejar sambil menunggu cooldown
                        if distance_to_ninja > self.close_range:
                            self.set_action('Running')
                            if ninja_x < self.x:
                                self.relative_x -= self.boss_speed * 0.5
                            else:
                                self.relative_x += self.boss_speed * 0.5
                        else:
                            self.set_action('Idle')
        else:
            # Ninja tidak terdeteksi, idle atau patrol
            # Hanya ganti action jika animasi movement sudah selesai
            if not (is_movement_animation and animation_not_complete):
                if random.randint(1, 120) == 1:  # Sesekali bergerak random
                    if random.choice([True, False]):
                        self.set_action('Running')
                        self.relative_x += random.choice([-1, 1]) * self.boss_speed * 0.3
                    else:
                        self.set_action('Idle Blinking')
                elif self.current_action not in ['Idle', 'Idle Blinking']:
                    self.set_action('Idle')
            else:
                # Tetap bergerak sesuai action saat ini
                if self.current_action == 'Running':
                    self.relative_x += random.choice([-1, 1]) * self.boss_speed * 0.3

        # Boss bergerak sambil melakukan 'Run Slashing'
        if self.current_action == 'Run Slashing' and distance_to_ninja <= self.detection_range:
            # Tetap mengejar ninja sambil menyerang
            if ninja_x < self.x:
                self.relative_x -= self.boss_speed * 0.6
            else:
                self.relative_x += self.boss_speed * 0.6

        # Update animasi frame
        if current_time - self.last_frame_update >= self.frame_update_time * 1000:
            if self.current_action in self.actions and self.actions[self.current_action]:
                self.current_frame += 1



                # Cek apakah boss sedang throwing dan di frame yang tepat untuk spawn projectile
                if (self.current_action in ['Throwing', 'Run Throwing'] and
                    self.current_frame == self.throwing_frame_trigger):
                    self.spawn_projectile(ninja_x, ninja_y)

                if self.current_frame >= len(self.actions[self.current_action]):
                    # Reset frame, kecuali untuk action yang tidak loop
                    if self.current_action in ['Hurt', 'Dying']:
                        self.current_frame = len(self.actions[self.current_action]) - 1
                        if self.current_action == 'Hurt':
                            self.is_hit = False
                            self.set_action('Idle')
                    else:
                        self.current_frame = 0
                        # Setelah selesai menyerang, kembali ke Idle (seperti zombie kembali ke Walk)
                        if self.current_action in self.attack_patterns:
                            self.set_action('Idle')  # Kembali ke Idle setelah serangan selesai

            self.last_frame_update = current_time

    def draw(self):
        """Gambar boss di layar"""
        sprite = self.get_current_sprite()
        if sprite:
            # Flip sprite jika menghadap kiri
            if self.facing_left:
                sprite = pygame.transform.flip(sprite, True, False)

            self.screen.blit(sprite, (self.x, self.y))

            # Gambar projectiles
            self.draw_projectiles()

    def draw_health_bar(self):
        """Gambar health bar boss di atas layar"""
        if not self.alive:
            return

        # Background health bar (merah gelap)
        pygame.draw.rect(self.screen, (100, 0, 0),
                        (self.health_bar_x, self.health_bar_y, self.health_bar_width, self.health_bar_height))

        # Health bar (merah terang)
        health_percentage = self.health / self.max_health
        current_width = int(self.health_bar_width * health_percentage)

        # Warna berubah berdasarkan health
        if health_percentage > 0.6:
            color = (255, 0, 0)  # Merah
        elif health_percentage > 0.3:
            color = (255, 165, 0)  # Orange
        else:
            color = (255, 255, 0)  # Kuning (critical)

        pygame.draw.rect(self.screen, color,
                        (self.health_bar_x, self.health_bar_y, current_width, self.health_bar_height))

        # Border health bar
        pygame.draw.rect(self.screen, (255, 255, 255),
                        (self.health_bar_x, self.health_bar_y, self.health_bar_width, self.health_bar_height), 2)

        # Text label
        font = pygame.font.Font(None, 24)
        boss_text = font.render("BOSS ZOMBIE", True, (255, 255, 255))
        text_rect = boss_text.get_rect(center=(self.health_bar_x + self.health_bar_width // 2, self.health_bar_y - 15))
        self.screen.blit(boss_text, text_rect)

        # Health numbers
        health_text = font.render(f"{self.health}/{self.max_health}", True, (255, 255, 255))
        health_rect = health_text.get_rect(center=(self.health_bar_x + self.health_bar_width // 2, self.health_bar_y + self.health_bar_height // 2))
        self.screen.blit(health_text, health_rect)

    def spawn_projectile(self, ninja_x, ninja_y):
        """Spawn projectile saat boss throwing"""
        # Hitung posisi spawn projectile (dari tangan boss)
        start_x = self.x + 50 if not self.facing_left else self.x - 50
        start_y = self.y + 30

        # Spawn projectile menuju ninja (tanpa homing)
        projectile = BossProjectile(
            screen=self.screen,
            start_x=start_x,
            start_y=start_y,
            target_x=ninja_x,
            target_y=ninja_y,
            speed=8,
            homing=False
        )
        self.projectiles.append(projectile)

    def update_projectiles(self, ninja_x=None, ninja_y=None):
        """Update semua projectile boss"""
        # Update posisi projectile dengan posisi ninja untuk homing
        for projectile in self.projectiles[:]:
            projectile.update(ninja_x, ninja_y)
            # Hapus projectile yang tidak aktif
            if not projectile.is_active():
                self.projectiles.remove(projectile)

    def draw_projectiles(self):
        """Gambar semua projectile boss"""
        for projectile in self.projectiles:
            projectile.draw()

    def get_projectiles(self):
        """Ambil daftar projectile untuk collision detection"""
        return self.projectiles

    def remove_projectile(self, projectile):
        """Hapus projectile tertentu (saat hit ninja)"""
        if projectile in self.projectiles:
            self.projectiles.remove(projectile)

    def reset(self):
        """Reset boss ke kondisi awal"""
        self.relative_x = self.init_pos
        self.x = self.init_pos + self.relative_x
        self.y = self.boss_ground
        self.health = self.max_health
        self.alive = True
        self.is_hit = False
        self.attack_cooldown = 0
        self.death_time = None
        self.projectiles = []  # Reset projectiles
        self.set_action('Idle')
