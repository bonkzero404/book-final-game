# -*- coding: utf-8 -*-
# File utama untuk menjalankan permainan Shinobi vs Zombie
# File ini mengatur semua yang terjadi dalam game: ninja, zombie, objek, dan layar

import random, pygame, math  # Library untuk membuat game
from ninja import Ninja  # Karakter ninja (pemain)
from object import Object  # Objek-objek dalam game (tanah, latar belakang)
from zombie import Zombie  # Karakter zombie (musuh)
from boss import Boss  # Karakter boss (musuh utama)
from spark import Spark  # Efek percikan darah
from explosion import Explosion  # Efek ledakan
from rain_effect import RainEffect  # Efek hujan
from lightning_effect import LightningEffect  # Efek petir
from moving_shadow_effect import MovingShadowEffect  # Efek shadow bergerak
from ash_effect import AshEffect  # Efek partikel abu gelap

pygame.init()  # Mulai pygame

# Import semua pengaturan game
from constants import CHARACTER_FOLDER, ENEMIES_FOLDER, OBJECTS_FOLDER, MAX_SCENE, BOSS_SCENE, NINJA_SPEED, ZOMBIE_SPEED, FPS, NINJA_GROND, FONT_GAME, BACKGROUND_START_GAME

class GamePlay:
    """Kelas GamePlay - Otak dari seluruh permainan

    Kelas ini mengatur semua yang terjadi dalam game:
    - Ninja bergerak dan bertarung
    - Zombie menyerang
    - Layar game dan menu
    - Skor dan game over
    """
    def __init__(self):
        """Mempersiapkan semua yang dibutuhkan untuk game

        Fungsi ini seperti menyiapkan panggung sebelum pertunjukan dimulai!
        """
        # Buat layar game dengan ukuran 1024x600 pixel
        self.screen = pygame.display.set_mode((1024, 600))
        self.clock = pygame.time.Clock()  # Pengatur kecepatan game
        self.ninja_ground = NINJA_GROND  # Tinggi tanah tempat ninja berdiri

        # Ninja akan dibuat nanti saat pemain memilih karakter
        self.ninja = None
        # Objek akan dimuat saat loading
        self.object = None

        # Asset akan dimuat saat loading
        self.male_character_image = None
        self.female_character_image = None
        self.assets_loaded = False


        # Preload semua zombie - tidak ada lazy loading lagi
        # Zombie bisa laki-laki atau perempuan (dipilih secara acak)
        self.zombies_sprite = ['/male', '/female']
        self.zombies = []  # Daftar semua zombie yang akan dimuat saat loading
        # Posisi zombie akan di-generate secara dinamis untuk menghindari jurang
        self.zombie_positions = []  # Akan diisi oleh generate_dynamic_zombie_positions()

        # Variabel untuk mengontrol game
        self.now = 0  # Waktu saat ini dalam game
        self.last_update = 0  # Waktu update terakhir untuk FPS control
        self.running = True  # Apakah game masih berjalan

        # Sistem skor
        self.score = 0  # Skor pemain

        # Boss fight variables
        self.boss = None  # Boss instance
        self.boss_mode = False  # Apakah sedang dalam mode boss
        self.boss_alert_shown = False  # Apakah alert boss sudah ditampilkan
        self.boss_defeated = False  # Apakah boss sudah dikalahkan
        self.boss_trigger_score = 300  # Score untuk memicu boss fight (setelah mengalahkan ~60 zombie)

        self.sparks = []  # Daftar efek percikan darah
        self.explosions = []  # Daftar efek ledakan

        self.zombie_is_hit = False  # Apakah ada zombie yang terkena serangan
        self.boss_is_hit = False  # Apakah boss sedang menyerang ninja

        # Efek layar merah saat ninja terkena serangan
        self.red_overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        self.red_overlay.fill((255, 0, 0))  # Warna merah
        self.red_overlay.set_alpha(128)  # Set transparansi (setengah transparan)

        # Pengaturan serangan zombie
        self.zombie_attack_time = 0  # Kapan zombie mulai menyerang
        self.zombie_attack_duration = 300  # Berapa lama serangan berlangsung (0.3 detik)

        # Berbagai ukuran font untuk teks di layar
        self.font = pygame.font.Font(FONT_GAME, 74)  # Font besar untuk judul
        self.font_small = pygame.font.Font(FONT_GAME, 28)  # Font kecil untuk instruksi
        self.title_character = pygame.font.Font(FONT_GAME, 40)  # Font untuk judul karakter
        self.font_character = pygame.font.Font(FONT_GAME, 20)  # Font untuk nama karakter

        self.blink_start_time = 0
        self.blink_duration = 500  # Durasi dalam milidetik
        self.show_instruction = True  # Status visibilitas teks

        # Background akan dimuat saat loading
        self.background_start_game = None
        self.background_resized = None
        self.background_character = None

        # Efek cuaca untuk mode boss
        self.rain_effect = None  # Akan diinisialisasi saat mode boss
        self.lightning_effect = None  # Akan diinisialisasi saat mode boss
        self.weather_active = False  # Status efek cuaca
        self.background_character_resized = None

        # Efek shadow bergerak untuk atmosfer horor
        self.shadow_effect = MovingShadowEffect(self.screen.get_width(), self.screen.get_height())
        self.shadow_effect.set_intensity(0.3)  # Intensitas awal rendah

        # Efek partikel abu gelap untuk atmosfer suram
        self.ash_effect = AshEffect(self.screen.get_width(), self.screen.get_height())

        # Sistem Score
        self.score = 0  # Skor pemain (bertambah 5 setiap membunuh zombie)

    def generate_dynamic_zombie_positions(self, num_zombies=70, min_distance=80, max_distance=200):
        """Generate posisi zombie secara dinamis yang aman dari jurang

        Parameter:
        - num_zombies: Jumlah zombie yang ingin dibuat
        - min_distance: Jarak minimum antar zombie
        - max_distance: Jarak maksimum antar zombie

        Return:
        - List posisi X yang aman untuk zombie
        """
        import random
        from constants import MAX_WIDTH

        # Pastikan object sudah dimuat
        if self.object is None:
            return []

        positions = []
        current_x = 1000  # Mulai dari posisi 1000 (setelah area awal)
        # Dapatkan max_x dari sistem game (lebar layar * jumlah scene)
        max_x = self.screen.get_width() * self.object.max_scene
        # Dapatkan lebar zombie dari konstanta yang digunakan sistem
        zombie_width = MAX_WIDTH

        # Set seed untuk konsistensi (opsional)
        random.seed(42)

        # Hitung estimasi zombie yang bisa dibuat berdasarkan area
        available_area = max_x - current_x
        estimated_max_zombies = int(available_area / min_distance)

        # Sesuaikan target zombie jika melebihi kapasitas area
        if num_zombies > estimated_max_zombies:
            print(f"⚠️  Target zombie ({num_zombies}) melebihi kapasitas area ({estimated_max_zombies})")
            print(f"🔧 Menyesuaikan target zombie menjadi {estimated_max_zombies}")
            num_zombies = estimated_max_zombies

        while current_x < max_x and len(positions) < num_zombies:
            # Cek apakah posisi saat ini aman
            if self.object._is_safe_position(current_x, zombie_width):
                positions.append(current_x)
                # Tambah jarak acak untuk posisi zombie berikutnya
                current_x += random.randint(min_distance, max_distance)
            else:
                # Jika tidak aman, lompat ke posisi berikutnya
                current_x += 50  # Lompat 50 pixel dan coba lagi

        return positions

    def show_loading_screen(self):
        """🔄 Tampilkan loading screen dan muat semua asset game."""
        # Setup loading screen
        loading_font = pygame.font.Font(FONT_GAME, 48)
        progress_font = pygame.font.Font(FONT_GAME, 24)

        # Estimasi jumlah zombie untuk perhitungan progress yang akurat
        estimated_zombies = 140  # Estimasi berdasarkan parameter default generate_dynamic_zombie_positions
        zombie_progress_calls = len([i for i in range(estimated_zombies) if i % 10 == 0 or i == estimated_zombies - 1])
        total_items = 7 + zombie_progress_calls + 1  # 7 basic + zombie calls + 1 finalizing
        loaded_items = 0

        def update_progress(message):
            nonlocal loaded_items, total_items
            loaded_items += 1
            progress = (loaded_items / total_items) * 100

            # Clear screen
            self.screen.fill((0, 0, 0))

            # Loading title
            title_text = loading_font.render("MEMUAT SHINOMBIE", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(self.screen.get_width()//2, 200))
            self.screen.blit(title_text, title_rect)

            # Progress message
            message_text = progress_font.render(message, True, (255, 255, 255))
            message_rect = message_text.get_rect(center=(self.screen.get_width()//2, 280))
            self.screen.blit(message_text, message_rect)

            # Progress bar
            bar_width = 400
            bar_height = 20
            bar_x = (self.screen.get_width() - bar_width) // 2
            bar_y = 320

            # Background bar
            pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
            # Progress bar
            progress_width = int((progress / 100) * bar_width)
            pygame.draw.rect(self.screen, (0, 255, 0), (bar_x, bar_y, progress_width, bar_height))
            # Border
            pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)

            # Progress percentage
            percent_text = progress_font.render(f"{progress:.1f}%", True, (255, 255, 255))
            percent_rect = percent_text.get_rect(center=(self.screen.get_width()//2, 360))
            self.screen.blit(percent_text, percent_rect)

            pygame.display.flip()
            self.clock.tick(60)  # Smooth loading animation

        # Load basic assets
        update_progress("Loading fonts and UI...")

        update_progress("Loading background images...")
        self.background_start_game = pygame.image.load(BACKGROUND_START_GAME).convert()
        self.background_resized = pygame.transform.scale(self.background_start_game, (self.screen.get_width(), self.screen.get_height()))

        update_progress("Loading character selection images...")
        self.background_character = pygame.image.load("assets/tiles/Background.png").convert()
        self.background_character_resized = pygame.transform.scale(self.background_character, (self.screen.get_width(), self.screen.get_height()))

        update_progress("Loading ninja character images...")
        self.male_character_image = pygame.image.load("assets/ninja/male/Attack__009.png").convert_alpha()
        self.female_character_image = pygame.image.load("assets/ninja/female/Attack__009.png").convert_alpha()

        update_progress("Loading game objects and tiles...")
        self.object = Object(OBJECTS_FOLDER, self.screen, MAX_SCENE, NINJA_SPEED)

        update_progress("Generating dynamic zombie positions...")
        # Generate posisi zombie secara dinamis setelah object dimuat
        self.zombie_positions = self.generate_dynamic_zombie_positions()

        # Update total_items dengan jumlah zombie yang sebenarnya untuk akurasi progress
        actual_zombie_calls = len([i for i in range(len(self.zombie_positions)) if i % 10 == 0 or i == len(self.zombie_positions) - 1])
        total_items = 7 + actual_zombie_calls + 1  # Update dengan jumlah sebenarnya

        update_progress("Menginisialisasi sistem game...")

        # Preload semua zombie dengan posisi dinamis
        update_progress(f"Memuat zombie... (0/{len(self.zombie_positions)})")
        for i, x_offset in enumerate(self.zombie_positions):
            zombie_type = random.choice(self.zombies_sprite)
            zombie = Zombie(ENEMIES_FOLDER + zombie_type, self.screen, NINJA_GROND, ZOMBIE_SPEED, x_offset, self.add_score)
            self.zombies.append(zombie)

            # Update progress setiap 10 zombie untuk performa
            if i % 10 == 0 or i == len(self.zombie_positions) - 1:
                update_progress(f"Memuat zombie... ({i+1}/{len(self.zombie_positions)})")

        update_progress("Menyelesaikan pengaturan game...")

        # Final setup
        self.assets_loaded = True

        # Show completion message
        self.screen.fill((0, 0, 0))
        complete_text = loading_font.render("LOADING SELESAI!", True, (0, 255, 0))
        complete_rect = complete_text.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2))
        self.screen.blit(complete_text, complete_rect)

        ready_text = progress_font.render("Tekan ENTER untuk melanjutkan...", True, (255, 255, 255))
        ready_rect = ready_text.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 + 60))
        self.screen.blit(ready_text, ready_rect)

        pygame.display.flip()

        # Wait for user input
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False
            self.clock.tick(60)

    def load_sprites(self, character_type):
        if character_type == 'male':
            self.ninja = Ninja(CHARACTER_FOLDER + '/' + character_type, self.screen, NINJA_GROND, NINJA_SPEED)  # Membuat instance Ninja
        else:
            self.ninja = Ninja(CHARACTER_FOLDER + '/' + character_type, self.screen, NINJA_GROND, NINJA_SPEED)  # Membuat instance Ninja

    def show_reset_loading_screen(self):
        """🔄 Tampilkan loading screen khusus untuk reset game."""
        # Setup loading screen
        loading_font = pygame.font.Font(FONT_GAME, 48)
        progress_font = pygame.font.Font(FONT_GAME, 24)

        # Tahapan reset yang akan ditampilkan
        reset_stages = [
            "Menghentikan semua proses...",
            "Mereset posisi ninja...",
            "Membersihkan zombie...",
            "Mereset objek lingkungan...",
            "Mereset skor dan status...",
            "Mereset efek visual...",
            "Regenerasi posisi zombie..."
        ]

        # Proses tahapan awal
        for stage_index, stage_text in enumerate(reset_stages):
            # Hitung progress untuk tahapan awal (70% dari total)
            progress = (stage_index + 1) / len(reset_stages) * 0.7

            # Clear screen
            self.screen.fill((0, 0, 0))

            # Tampilkan judul loading
            title_text = loading_font.render("MERESET GAME...", True, (255, 255, 0))
            title_rect = title_text.get_rect(center=(self.screen.get_width()//2, 200))
            self.screen.blit(title_text, title_rect)

            # Tampilkan tahapan saat ini
            stage_surface = progress_font.render(stage_text, True, (255, 255, 255))
            stage_rect = stage_surface.get_rect(center=(self.screen.get_width()//2, 300))
            self.screen.blit(stage_surface, stage_rect)

            # Progress bar
            bar_width = 400
            bar_height = 30
            bar_x = (self.screen.get_width() - bar_width) // 2
            bar_y = 350

            # Background bar
            pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))

            # Progress bar dengan gradient
            if progress > 0:
                filled_width = int(bar_width * progress)
                # Gradient dari merah ke hijau
                red_component = int(255 * (1 - progress))
                green_component = int(255 * progress)
                color = (red_component, green_component, 0)
                pygame.draw.rect(self.screen, color, (bar_x, bar_y, filled_width, bar_height))

            # Border bar
            pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)

            # Persentase
            percentage = int(progress * 100)
            percent_text = progress_font.render(f"{percentage}%", True, (255, 255, 255))
            percent_rect = percent_text.get_rect(center=(self.screen.get_width()//2, bar_y + bar_height + 30))
            self.screen.blit(percent_text, percent_rect)

            pygame.display.flip()

            # Delay untuk setiap tahapan
            pygame.time.wait(200)

            # Handle events untuk mencegah freeze
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

        # Proses pembuatan zombie dengan progress yang terlihat
        import random

        # Regenerate zombie positions
        self.zombie_positions = self.generate_dynamic_zombie_positions()
        self.zombies = []  # Clear zombie list

        # Buat ulang semua zombie dengan progress bar
        total_zombies = len(self.zombie_positions)
        for i, x_offset in enumerate(self.zombie_positions):
            # Hitung progress untuk pembuatan zombie (30% sisanya)
            zombie_progress = 0.7 + (i + 1) / total_zombies * 0.3

            # Clear screen
            self.screen.fill((0, 0, 0))

            # Tampilkan judul loading
            title_text = loading_font.render("MERESET GAME...", True, (255, 255, 0))
            title_rect = title_text.get_rect(center=(self.screen.get_width()//2, 200))
            self.screen.blit(title_text, title_rect)

            # Tampilkan tahapan pembuatan zombie
            stage_surface = progress_font.render(f"Memuat ulang zombie... ({i+1}/{total_zombies})", True, (255, 255, 255))
            stage_rect = stage_surface.get_rect(center=(self.screen.get_width()//2, 300))
            self.screen.blit(stage_surface, stage_rect)

            # Progress bar
            bar_width = 400
            bar_height = 30
            bar_x = (self.screen.get_width() - bar_width) // 2
            bar_y = 350

            # Background bar
            pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))

            # Progress bar dengan gradient
            filled_width = int(bar_width * zombie_progress)
            red_component = int(255 * (1 - zombie_progress))
            green_component = int(255 * zombie_progress)
            color = (red_component, green_component, 0)
            pygame.draw.rect(self.screen, color, (bar_x, bar_y, filled_width, bar_height))

            # Border bar
            pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)

            # Persentase
            percentage = int(zombie_progress * 100)
            percent_text = progress_font.render(f"{percentage}%", True, (255, 255, 255))
            percent_rect = percent_text.get_rect(center=(self.screen.get_width()//2, bar_y + bar_height + 30))
            self.screen.blit(percent_text, percent_rect)

            # Update display setiap 10 zombie untuk performa
            if i % 10 == 0 or i == total_zombies - 1:
                pygame.display.flip()

            # Buat zombie
            zombie_type = random.choice(self.zombies_sprite)
            zombie = Zombie(ENEMIES_FOLDER + zombie_type, self.screen, NINJA_GROND, ZOMBIE_SPEED, x_offset, self.add_score)
            self.zombies.append(zombie)

            # Handle events untuk mencegah freeze
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

        # Tampilkan pesan selesai
        self.screen.fill((0, 0, 0))
        complete_text = loading_font.render("RESET SELESAI!", True, (0, 255, 0))
        complete_rect = complete_text.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2))
        self.screen.blit(complete_text, complete_rect)

        ready_text = progress_font.render("Game akan dimulai...", True, (255, 255, 255))
        ready_rect = ready_text.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 + 60))
        self.screen.blit(ready_text, ready_rect)

        pygame.display.flip()
        pygame.time.wait(1000)  # Tampilkan pesan selesai selama 1 detik

    def get_visible_zombies(self):
        """Dapatkan zombie yang terlihat di layar untuk rendering."""
        if not self.ninja:
            return []

        visible_zombies = []
        ninja_x = self.ninja.get_x()
        screen_width = self.screen.get_width()

        for zombie in self.zombies:
            zombie_x = zombie.get_x()
            # Hanya render zombie yang terlihat di layar dengan buffer
            if zombie_x > ninja_x - screen_width and zombie_x < ninja_x + screen_width:
                visible_zombies.append(zombie)

        return visible_zombies

    def downfall_action(self):
        ninja_size_x, _ = self.ninja.get_current_sprite().get_size()

        for idx, x in enumerate(self.object.get_downfall_positions()):
            block_width = x + self.object.get_road_width()

            if idx + 1 < len(self.object.get_downfall_positions()):
                if x + self.object.get_road_width() == self.object.get_downfall_positions()[idx + 1]:
                    block_width = x + (self.object.get_road_width() * 2)

            # Ninja downfall
            if self.object.get_x() + self.ninja.get_x() >= x  and self.object.get_x() + self.ninja.get_x() <= (block_width - ninja_size_x) and self.ninja.get_y() >= self.ninja_ground:
                self.object.set_downfall()
                self.ninja.add_y()

                if self.ninja.get_y() >= self.screen.get_height():
                    # self.reset()
                    self.ninja.set_alive(False)
                    self.ninja.health = 0
                    break

            # Zombie downfall
            for i, zombie in enumerate(self.zombies):
                zombie_size_x, _ = zombie.get_current_sprite().get_size()
                if zombie.get_relative_x() >= x and zombie.get_relative_x() <= block_width:
                    if not zombie.is_downfall:
                        zombie.set_action('Idle')
                        zombie.set_downfall()

    def remove_dead_zombies(self):
        """Menghapus zombie yang sudah mati dari daftar."""
        self.zombies = [zombie for zombie in self.zombies if zombie.get_alive() or not zombie.is_ready_to_remove()]

    def add_score(self, points=5):
        """🏆 Menambah poin score

        Parameter:
        - points: Jumlah poin yang ditambahkan (default 5 untuk zombie)
        """
        self.score += points

    def get_score(self):
        """📊 Mengambil score saat ini"""
        return self.score

    def initialize_boss(self):
        """👹 Inisialisasi boss fight"""
        if self.boss is None:
            # Buat object baru dengan mode boss (tanpa jurang)
            self.object = Object(OBJECTS_FOLDER, self.screen, MAX_SCENE, NINJA_SPEED, boss_mode=True)

            # Buat boss di posisi yang tepat
            boss_init_pos = self.screen.get_width() + 200  # Boss muncul dari kanan
            boss_ground = NINJA_GROND - 30  # Boss lebih tinggi dari ninja (50 pixel ke atas)
            self.boss = Boss('assets/boss', self.screen, boss_ground, ZOMBIE_SPEED * 0.8, boss_init_pos)

            # Set mode boss
            self.boss_mode = True

            # Inisialisasi efek cuaca untuk mode boss
            self.rain_effect = RainEffect(self.screen.get_width(), self.screen.get_height(), intensity=150)
            self.lightning_effect = LightningEffect(self.screen.get_width(), self.screen.get_height(), self.create_ground_explosion)
            self.weather_active = True

            # Hapus semua zombie yang tersisa
            self.zombies = []

    def create_ground_explosion(self, x, y):
        """💥 Buat efek ledakan tanah saat petir menyambar - berhamburan seperti spark"""
        # Buat banyak partikel tanah yang berhamburan dalam jumlah sangat besar
        particle_count = random.randint(50, 80)  # Jumlah partikel yang sangat banyak

        for _ in range(particle_count):
            # Posisi acak di sekitar titik sambaran dengan area yang lebih luas
            spark_x = x + random.randint(-60, 60)
            spark_y = y + random.randint(-25, 10)

            # Variasi warna tanah - coklat gelap, coklat muda, dan abu-abu
            colors = [
                (101, 67, 33),   # Coklat gelap
                (139, 69, 19),   # Coklat sedang
                (160, 82, 45),   # Coklat muda
                (105, 105, 105), # Abu-abu gelap
                (128, 128, 128), # Abu-abu terang
                (87, 59, 12),    # Coklat sangat gelap
                (205, 133, 63),  # Coklat terang
                (139, 90, 43)    # Coklat kekuningan
            ]
            color = random.choice(colors)

            # Buat spark dengan parameter yang sesuai dengan konstruktor Spark
            angle = random.uniform(0, 2 * math.pi)  # Arah acak
            speed = random.uniform(3, 10)  # Kecepatan yang lebih bervariasi
            spark = Spark([spark_x, spark_y], angle, speed, color)
            self.sparks.append(spark)

    def show_boss_alert(self):
        """🚨 Tampilkan alert sebelum boss fight"""
        self.screen.fill((0, 0, 0))  # Background hitam

        # Alert text - bagi menjadi 2 baris agar tidak terpotong
        alert_text1 = self.font_small.render("SEBENTAR LAGI AKAN MELAWAN", True, (255, 0, 0))
        alert_rect1 = alert_text1.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 20))
        self.screen.blit(alert_text1, alert_rect1)

        alert_text2 = self.font_small.render("BOSS ZOMBIE!", True, (255, 0, 0))
        alert_rect2 = alert_text2.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 10))
        self.screen.blit(alert_text2, alert_rect2)

        # Instruction
        instruction_text = self.font_small.render("Tekan ENTER untuk melanjutkan...", True, (255, 255, 255))
        instruction_rect = instruction_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 60))
        self.screen.blit(instruction_text, instruction_rect)

        pygame.display.flip()

        # Wait for user input
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False
            self.clock.tick(60)

    def show_victory_screen(self):
        """🏆 Tampilkan screen kemenangan setelah boss dikalahkan"""
        self.screen.fill((0, 0, 0))  # Background hitam

        # Game complete text
        complete_text = self.font.render("GAME TAMAT", True, (255, 255, 0))
        complete_rect = complete_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 30))
        self.screen.blit(complete_text, complete_rect)

        # Final score
        score_text = self.font_small.render(f"Score Akhir: {self.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 80))
        self.screen.blit(score_text, score_rect)

        # Exit instruction
        exit_text = self.font_small.render("Tekan ESC untuk keluar...", True, (255, 255, 255))
        exit_rect = exit_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 120))
        self.screen.blit(exit_text, exit_rect)

        pygame.display.flip()

        # Wait for user input
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        waiting = False
                        self.running = False
            self.clock.tick(60)

    def reset(self):
        # Reset karakter dan objek
        self.ninja.reset()
        self.object.reset()

        # Reset score dan status game
        self.score = 0

        # Reset boss mode dan status
        self.boss_mode = False
        self.boss_defeated = False
        self.boss_alert_shown = False
        self.boss = None

        # Reset efek cuaca
        self.weather_active = False
        self.rain_effect = None
        self.lightning_effect = None

        # Reset efek visual
        self.sparks = []
        self.explosions = []

        # Reset status serangan
        self.zombie_is_hit = False
        self.boss_is_hit = False
        self.zombie_attack_time = 0

        # Reset timer dan state variables
        self.now = 0
        self.last_update = 0
        self.blink_start_time = pygame.time.get_ticks()
        self.show_instruction = True

        # Catatan: Zombie positions dan zombies sudah di-handle di show_reset_loading_screen()
        # Tidak perlu membuat zombie di sini lagi untuk menghindari jeda

        pygame.display.update()
        self.update_frame()

    def hit_ninja(self, zombie, ninja):
        """Cek jika zombie menabrak ninja."""
        zombie_sprite = zombie.get_current_sprite()
        ninja_sprite = ninja.get_current_sprite()

        if ninja_sprite and zombie_sprite:
            # Sesuaikan posisi collision box dengan posisi visual sprite yang di-center
            zombie_rect = zombie_sprite.get_rect(topleft=(zombie.get_x() - zombie_sprite.get_width() // 2, zombie.get_y()))
            ninja_rect = ninja_sprite.get_rect(topleft=(ninja.get_x(), ninja.get_y()))

            # Perluas area serangan zombie untuk deteksi yang lebih konsisten
            attack_buffer = 20  # Buffer tambahan untuk jangkauan serangan
            zombie_attack_rect = zombie_rect.inflate(attack_buffer, attack_buffer)

            if zombie_attack_rect.colliderect(ninja_rect):

                if not self.zombie_is_hit and zombie.alive:
                    zombie.set_action('Attack')
                    self.zombie_is_hit = True

                if zombie.current_action == 'Attack':
                    # Damage terjadi di tengah animasi untuk timing yang lebih konsisten
                    attack_frames = len(zombie.actions['Attack'])
                    damage_frame = attack_frames // 2  # Frame tengah animasi

                    if zombie.current_frame == damage_frame and ninja.get_alive():
                        self.zombie_attack_time = pygame.time.get_ticks()
                        ninja.damage()
                        self.zombie_is_hit = False

            else:
                if self.zombie_is_hit and zombie.alive:
                    zombie.set_action('Walk')

                self.zombie_is_hit = False

    def hit_zombie(self, zombies, ninja):
        """Deteksi tabrakan dengan semua zombie."""
        for zombie in zombies:
            ninja_rect = ninja.get_current_sprite().get_rect(topleft=(ninja.get_x(), ninja.get_y()))
            zombie_sprite = zombie.get_current_sprite()
            zombie_rect = zombie_sprite.get_rect(topleft=(zombie.get_x() - zombie_sprite.get_width() // 2, zombie.get_y()))

            if ninja_rect.colliderect(zombie_rect):
                if ninja.current_action in ['Jump_Attack'] and zombie.get_alive():
                    self.spark_zombie_blood(zombie)
                    # zombie.set_dead()
                    zombie.damage('Double')
                if ninja.current_action in ['Attack'] and zombie.get_alive():
                    self.spark_zombie_blood(zombie)
                    # zombie.set_dead()
                    zombie.damage()

        self.remove_dead_zombies()

    def hit_zombie_kunais(self, zombies, ninja):
        """Deteksi tabrakan kunai dengan zombie."""
        for zombie in zombies:
            for kunai in ninja.kunais:
                kunai_rect = kunai.get_current_sprite().get_rect(topleft=(kunai.get_x(), kunai.get_y()))
                zombie_sprite = zombie.get_current_sprite()
                zombie_rect = zombie_sprite.get_rect(topleft=(zombie.get_x() - zombie_sprite.get_width() // 2, zombie.get_y()))

                if kunai_rect.colliderect(zombie_rect):
                    if zombie.get_alive():
                        self.spark_zombie_blood(zombie)
                        # zombie.set_dead()
                        zombie.damage('Kunai')

                        if kunai in ninja.kunais:
                            ninja.kunais.remove(kunai)

        self.remove_dead_zombies

    def spark_zombie_blood(self, zombie):
        """Buat sparks darah saat ninja menyerang zombie."""
        direction = 1 if zombie.facing_left else -1  # Arah berdasarkan orientasi zombie

        # Warna darah dengan variasi untuk efek realistis
        blood_colors = [
            (220, 20, 20),   # Merah darah terang
            (180, 0, 0),     # Merah darah gelap
            (255, 0, 0),     # Merah murni
            (139, 0, 0),     # Merah tua
            (205, 92, 92),   # Merah muda darah
            (128, 0, 0),     # Maroon
            (255, 69, 0)     # Merah oranye
        ]

        # Tambah jumlah partikel untuk efek yang lebih dramatis
        for _ in range(random.randint(15, 25)):
            # Sudut yang lebih lebar untuk efek percikan yang lebih natural
            angle = random.uniform(-math.pi / 3, math.pi / 3)
            speed = random.uniform(3, 8)  # Kecepatan yang lebih bervariasi
            scale = random.uniform(0.8, 3.0)  # Ukuran partikel yang lebih bervariasi
            color = random.choice(blood_colors)  # Pilih warna darah

            # Posisi spawn yang lebih tersebar untuk efek percikan natural
            spawn_x = zombie.get_x() + random.randint(35, 55)
            spawn_y = zombie.get_y() + random.randint(50, 70)

            spark = Spark([spawn_x, spawn_y], angle, speed, color, scale=scale, direction=direction)
            self.sparks.append(spark)

    def spark_boss_blood(self, boss):
        """Buat sparks darah saat ninja menyerang boss."""
        direction = 1 if boss.facing_left else -1  # Arah berdasarkan orientasi boss

        # Warna darah dengan variasi untuk efek realistis
        blood_colors = [
            (220, 20, 20),   # Merah darah terang
            (180, 0, 0),     # Merah darah gelap
            (255, 0, 0),     # Merah murni
            (139, 0, 0),     # Merah tua
            (205, 92, 92),   # Merah muda darah
            (128, 0, 0),     # Maroon
            (255, 69, 0)     # Merah oranye
        ]

        # Lebih banyak partikel untuk boss karena lebih besar
        for _ in range(random.randint(20, 30)):
            # Sudut yang lebih lebar untuk efek percikan yang lebih natural
            angle = random.uniform(-math.pi / 3, math.pi / 3)
            speed = random.uniform(4, 10)  # Kecepatan lebih tinggi untuk boss
            scale = random.uniform(1.0, 4.0)  # Ukuran partikel lebih besar untuk boss
            color = random.choice(blood_colors)  # Pilih warna darah

            # Posisi spawn yang lebih tersebar untuk efek percikan natural
            boss_sprite = boss.get_current_sprite()
            spawn_x = boss.get_x() + random.randint(40, boss_sprite.get_width() - 40)
            spawn_y = boss.get_y() + random.randint(60, boss_sprite.get_height() - 20)

            spark = Spark([spawn_x, spawn_y], angle, speed, color, scale=scale, direction=direction)
            self.sparks.append(spark)

    def get_distance(self, point1, point2):
        """Menghitung jarak antara dua titik (x, y)."""
        x1, y1 = point1
        x2, y2 = point2
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def find_nearest_zombie(self, ninja, zombies):
        """Temukan zombie terdekat dengan ninja."""
        nearest_zombie_index = -1
        min_distance = float('inf')

        for index, zombie in enumerate(zombies):
            distance = self.get_distance((ninja.get_x(), ninja.get_y()), (zombie.get_x(), zombie.get_y()))
            if distance < min_distance:
                min_distance = distance
                nearest_zombie_index = index

        return nearest_zombie_index

    def reset_attacking_zombies_out_of_range(self):
        """Reset zombie yang sedang menyerang tapi tidak lagi dalam jangkauan ninja."""
        for zombie in self.zombies:
            if zombie.current_action == 'Attack' and zombie.alive:
                zombie_sprite = zombie.get_current_sprite()
                ninja_sprite = self.ninja.get_current_sprite()

                if ninja_sprite and zombie_sprite:
                    # Sesuaikan posisi collision box dengan posisi visual sprite yang di-center
                    zombie_rect = zombie_sprite.get_rect(topleft=(zombie.get_x() - zombie_sprite.get_width() // 2, zombie.get_y()))
                    ninja_rect = ninja_sprite.get_rect(topleft=(self.ninja.get_x(), self.ninja.get_y()))

                    # Perluas area serangan zombie untuk deteksi yang lebih konsisten
                    attack_buffer = 20  # Buffer tambahan untuk jangkauan serangan
                    zombie_attack_rect = zombie_rect.inflate(attack_buffer, attack_buffer)

                    # Jika zombie tidak lagi dalam jangkauan ninja, reset ke Walk
                    if not zombie_attack_rect.colliderect(ninja_rect):
                        zombie.set_action('Walk')

    def hit_boss(self, boss, ninja):
        """👹 Cek collision antara ninja dan boss"""
        if not boss or not boss.get_alive():
            return

        ninja_sprite = ninja.get_current_sprite()
        boss_sprite = boss.get_current_sprite()

        if ninja_sprite and boss_sprite:
            ninja_rect = ninja_sprite.get_rect(topleft=(ninja.get_x(), ninja.get_y()))
            boss_rect = boss_sprite.get_rect(topleft=(boss.get_x(), boss.get_y()))

            # Cek collision untuk serangan ninja
            if ninja.current_action in ['Attack', 'Jump_Attack'] and ninja_rect.colliderect(boss_rect):
                if not hasattr(self, 'boss_hit_cooldown'):
                    self.boss_hit_cooldown = 0

                if self.boss_hit_cooldown <= 0:
                    boss.damage(25)  # Boss menerima damage lebih besar
                    self.boss_hit_cooldown = 30  # Cooldown 0.5 detik

                    # Buat spark blood effect menggunakan fungsi yang sama dengan zombie
                    self.spark_boss_blood(boss)

            # Update cooldown
            if hasattr(self, 'boss_hit_cooldown') and self.boss_hit_cooldown > 0:
                self.boss_hit_cooldown -= 1

    def hit_boss_kunais(self, boss, ninja):
        """🗡️ Cek collision antara kunai ninja dan boss"""
        if not boss or not boss.get_alive():
            return

        boss_sprite = boss.get_current_sprite()
        if not boss_sprite:
            return

        boss_rect = boss_sprite.get_rect(topleft=(boss.get_x(), boss.get_y()))

        for kunai in ninja.kunais[:]:
            kunai_rect = kunai.get_current_sprite().get_rect(topleft=(kunai.get_x(), kunai.get_y()))

            if kunai_rect.colliderect(boss_rect):
                boss.damage(15)  # Kunai damage ke boss
                ninja.kunais.remove(kunai)

                # Buat spark blood effect menggunakan fungsi yang sama dengan zombie
                self.spark_boss_blood(boss)

    def hit_ninja_boss(self, boss, ninja):
        """👹 Cek collision antara boss dan ninja"""
        if not boss or not boss.get_alive():
            return

        boss_sprite = boss.get_current_sprite()
        ninja_sprite = ninja.get_current_sprite()

        if ninja_sprite and boss_sprite:
            boss_rect = boss_sprite.get_rect(topleft=(boss.get_x(), boss.get_y()))
            ninja_rect = ninja_sprite.get_rect(topleft=(ninja.get_x(), ninja.get_y()))

            # Buffer untuk serangan boss
            attack_buffer = 30
            boss_attack_rect = boss_rect.inflate(attack_buffer, attack_buffer)

            # Boss sekarang menyerang secara independen melalui AI
            # Collision detection hanya menangani damage ketika boss sedang menyerang (kecuali Throwing)
            if boss_attack_rect.colliderect(ninja_rect) and boss.current_action in ['Slashing', 'Kicking', 'Run Slashing']:
                # Damage terjadi di tengah animasi untuk timing yang lebih konsisten
                attack_frames = len(boss.actions[boss.current_action])
                damage_frame = attack_frames // 2  # Frame tengah animasi

                if boss.current_frame == damage_frame and ninja.get_alive() and not self.boss_is_hit:
                    self.zombie_attack_time = pygame.time.get_ticks()  # Set waktu serangan untuk red overlay
                    ninja.damage()
                    self.boss_is_hit = True

                    # Buat spark effect pada ninja
                    spark_x = ninja.get_x() + ninja_sprite.get_width() // 2
                    spark_y = ninja.get_y() + ninja_sprite.get_height() // 2
                    for _ in range(6):
                        angle = random.uniform(0, 2 * math.pi)  # Arah acak
                        speed = random.uniform(2, 5)  # Kecepatan acak
                        spark = Spark([spark_x, spark_y], angle, speed, (255, 0, 0))
                        self.sparks.append(spark)
            else:
                # Reset flag ketika tidak ada collision atau boss tidak sedang menyerang
                if boss.current_action not in ['Slashing', 'Throwing', 'Run Slashing']:
                    self.boss_is_hit = False

    def hit_ninja_boss_projectiles(self, boss, ninja):
        """🔮 Cek collision antara projectile boss dan ninja"""
        if not boss or not boss.get_alive() or not ninja.get_alive():
            return

        ninja_sprite = ninja.get_current_sprite()
        if not ninja_sprite:
            return

        ninja_rect = ninja_sprite.get_rect(topleft=(ninja.get_x(), ninja.get_y()))

        # Cek collision dengan semua projectile boss
        for projectile in boss.get_projectiles()[:]:
            if projectile.is_active():
                projectile_rect = projectile.get_rect()

                if ninja_rect.colliderect(projectile_rect):
                    # Ninja terkena projectile
                    self.zombie_attack_time = pygame.time.get_ticks()  # Set waktu serangan untuk red overlay
                    ninja.damage()

                    # Posisi ledakan di tengah ninja
                    explosion_x = ninja.get_x() + ninja_sprite.get_width() // 2
                    explosion_y = ninja.get_y() + ninja_sprite.get_height() // 2

                    # Buat efek ledakan
                    explosion = Explosion(explosion_x, explosion_y, 60)
                    self.explosions.append(explosion)

                    # Buat spark effect tambahan
                    self.sparks.append(Spark([explosion_x, explosion_y], 0, 5, (255, 0, 0)))

                    # Hapus projectile
                    boss.remove_projectile(projectile)

                    # Hanya satu projectile yang bisa hit per frame
                    break

    def update_frame(self):
        self.ninja.update_frame()
        self.ninja.update_kunais()

        # Update zombie atau boss berdasarkan mode
        if self.boss_mode and self.boss:
            # Update boss
            self.boss.update_frame(self.object.get_road_x(), self.ninja.get_x(), self.ninja.get_y())

            # Combat dengan boss
            self.hit_boss(self.boss, self.ninja)
            self.hit_boss_kunais(self.boss, self.ninja)
            self.hit_ninja_boss(self.boss, self.ninja)
            self.hit_ninja_boss_projectiles(self.boss, self.ninja)

            # Cek apakah boss mati
            if not self.boss.get_alive() and not self.boss_defeated:
                self.boss_defeated = True
                self.add_score(100)  # Bonus score untuk mengalahkan boss
                # Nonaktifkan efek cuaca saat boss dikalahkan
                self.weather_active = False
        else:
            # Update zombie normal
            for zombie in self.zombies:
                zombie.update_frame(self.object.get_road_x(), abs(self.object.get_road_x() - self.ninja.get_x()), self.zombies,
                                  self.object.get_downfall_positions(), self.object.get_road_width())

            self.hit_zombie(self.zombies, self.ninja)
            self.hit_zombie_kunais(self.zombies, self.ninja)

            nearest_zombie_index = self.find_nearest_zombie(self.ninja, self.zombies)
            if nearest_zombie_index != -1:
                self.hit_ninja(self.zombies[nearest_zombie_index], self.ninja)

            # Reset zombie yang sedang menyerang tapi tidak lagi dalam jangkauan
            self.reset_attacking_zombies_out_of_range()

        for spark in self.sparks:
            spark.velocity_adjust(1, 0.2, 8, 1)
            spark.move(5)

        # Update explosions
        for explosion in self.explosions[:]:
            explosion.update()
            if not explosion.is_alive():
                self.explosions.remove(explosion)

        # Update efek cuaca saat mode boss
        if self.boss_mode and self.weather_active:
            if self.rain_effect:
                self.rain_effect.update()
            if self.lightning_effect:
                self.lightning_effect.update()

        # Update efek shadow bergerak
        if self.shadow_effect:
            # Atur intensitas berdasarkan jumlah zombie
            zombie_count = len([z for z in self.zombies if z.get_alive()])
            self.shadow_effect.create_horror_atmosphere(zombie_count)
            self.shadow_effect.update()

        # Update efek partikel abu gelap
        if self.ash_effect:
            dt = self.clock.get_time() / 1000.0  # Delta time dalam detik
            self.ash_effect.update(dt)

        self.object.update_frame(self.ninja)
        self.event_handler()

        self.last_update = self.now
        pygame.display.update()  # Update layar
        self.clock.tick(FPS)  # Batasi FPS game loop

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                self.ninja.event_handler(event)

    def show_start_screen(self):
        """Menampilkan halaman start game."""
        # Load background untuk start screen jika belum dimuat
        if self.background_start_game is None:
            self.background_start_game = pygame.image.load(BACKGROUND_START_GAME).convert()
            self.background_resized = pygame.transform.scale(self.background_start_game, (self.screen.get_width(), self.screen.get_height()))

        instruction_surface = ''
        instruction_rect = ''

        # Tampilkan teks "Start Game"
        title_surface = self.font.render("SHINOMBIE", True, (255, 255, 255))  # Teks putih
        title_rect = title_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 50))

        # Tampilkan instruksi
        if self.show_instruction:
            instruction_surface = self.font_small.render("Tekan Enter Untuk Mulai", True, (255, 255, 255))
            instruction_rect = instruction_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 20))

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Jika Enter ditekan
                        waiting = False

            # Logika untuk membuat teks berkedip
            current_time = pygame.time.get_ticks()
            if current_time - self.blink_start_time > self.blink_duration:
                self.show_instruction = not self.show_instruction  # Toggle visibilitas
                self.blink_start_time = current_time  # Reset timer

            self.screen.blit(self.background_resized, (0, 0))
            self.screen.blit(title_surface, title_rect)  # Gambar judul
            if self.show_instruction:
                self.screen.blit(instruction_surface, instruction_rect)  # Gambar instruksi

            pygame.display.flip()  # Update layar
            self.clock.tick(FPS)  # Batasi FPS

    def show_character_selection_screen(self):
        """Menampilkan layar pemilihan karakter."""
        # instruction_surface = ''
        # instruction_rect = ''

        female = pygame.transform.flip(self.female_character_image, True, False)

        # Tampilkan teks instruksi
        title_character = self.title_character.render("PILIH KARAKTER", True, (255, 255, 255))
        title_rect = title_character.get_rect(center=(self.screen.get_width() // 2, 50))

        # if self.show_instruction:
        instruction_surface = self.font_character.render("Tekan 1 Untuk Shinoboy, Tekan 2 Untuk Shinogirl", True, (255, 255, 255))
        instruction_rect = instruction_surface.get_rect(center=(self.screen.get_width() // 2, 100))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:  # Tekan 1 untuk memilih karakter pria
                        self.load_sprites("male")
                        self.ninja.set_name("Shinoboy")
                        running = False
                    elif event.key == pygame.K_2:  # Tekan 2 untuk memilih karakter wanita
                        self.load_sprites("female")
                        self.ninja.set_name("Shinogirl")
                        running = False

            current_time = pygame.time.get_ticks()
            if current_time - self.blink_start_time > self.blink_duration:
                self.show_instruction = not self.show_instruction  # Toggle visibilitas
                self.blink_start_time = current_time  # Reset timer

            # Gambar latar belakang
            self.screen.blit(self.background_character_resized, (0, 0))

            self.screen.blit(self.male_character_image, (10, 200))  # Posisi karakter pria
            self.screen.blit(female, (500, 130))  # Posisi karakter wanita

            self.screen.blit(title_character, title_rect)

            if self.show_instruction:
                self.screen.blit(instruction_surface, instruction_rect)  # Gambar instruksi

            pygame.display.flip()  # Update layar
            self.clock.tick(FPS)  # Batasi FPS

    def show_game_over_screen(self):
        """Menampilkan halaman game over dengan pilihan restart atau keluar."""
        self.screen.fill((0, 0, 0))  # Latar belakang hitam

        # Tampilkan teks "Game Over"
        game_over_surface = self.font.render("Game Over", True, (255, 0, 0))  # Teks merah
        game_over_rect = game_over_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 80))
        self.screen.blit(game_over_surface, game_over_rect)

        # Tampilkan skor akhir
        score_surface = self.font_small.render(f"Skor Akhir: {self.score}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 30))
        self.screen.blit(score_surface, score_rect)

        # Tampilkan pilihan menu
        restart_surface = self.font_small.render("Tekan R untuk Restart Game", True, (0, 255, 0))  # Hijau
        restart_rect = restart_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 20))
        self.screen.blit(restart_surface, restart_rect)

        quit_surface = self.font_small.render("Tekan Q untuk Keluar Game", True, (255, 255, 0))  # Kuning
        quit_rect = quit_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 60))
        self.screen.blit(quit_surface, quit_rect)

        pygame.display.flip()  # Update layar

        # Tunggu sampai pemain memilih opsi
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Jika R ditekan untuk restart
                        waiting = False
                        self.show_reset_loading_screen()  # Tampilkan loading screen reset
                        self.reset()  # Reset permainan untuk memulai ulang
                        self.show_character_selection_screen()  # Kembali ke pemilihan karakter
                    elif event.key == pygame.K_q:  # Jika Q ditekan untuk keluar
                        waiting = False
                        self.running = False

    def run(self):
        """🎮 Game loop utama"""
        self.show_start_screen()
        self.show_loading_screen()
        self.show_character_selection_screen()

        # SHORTCUT: Langsung ke boss mode untuk testing
        # Uncomment baris di bawah untuk langsung test boss
        # self.initialize_boss()

        while self.running:
            self.now = pygame.time.get_ticks()
            if self.now - self.last_update > 1000 / FPS:
                self.screen.fill((0, 0, 0))

                # Cek trigger boss fight berdasarkan scene terakhir
                current_scene = self.object.get_scene()
                if current_scene >= MAX_SCENE and not self.boss_mode and not self.boss_alert_shown:
                    self.show_boss_alert()
                    self.boss_alert_shown = True
                    self.initialize_boss()

                # Gambar objek latar belakang
                self.object.draw(self.screen)

                # Gambar ninja
                self.ninja.draw(self.screen)

                # Gambar health bar ninja
                self.ninja.draw_health_bar()

                # Tampilkan skor di pojok kanan atas
                score_text = self.font_small.render(f"Score: {self.score}", True, (255, 255, 255))
                score_rect = score_text.get_rect(topright=(self.screen.get_width() - 20, 20))
                self.screen.blit(score_text, score_rect)

                # Gambar sparks
                for spark in self.sparks[:]:
                    spark.draw(self.screen)
                    if not spark.alive:
                        self.sparks.remove(spark)

                # Gambar explosions
                for explosion in self.explosions:
                    explosion.draw(self.screen)

                # Gambar boss atau zombie berdasarkan mode
                if self.boss_mode and self.boss:
                    self.boss.draw()
                    self.boss.draw_health_bar()

                    # Cek apakah boss sudah dikalahkan
                    if self.boss_defeated:
                        self.show_victory_screen()
                        break
                else:
                    # Gambar semua zombie
                    for zombie in self.zombies:
                        zombie.draw()

                # Update dan gambar efek cuaca saat mode boss
                if self.boss_mode and self.weather_active:
                    # Update efek hujan
                    if self.rain_effect:
                        self.rain_effect.update()
                        self.rain_effect.draw(self.screen)

                    # Update efek petir
                    if self.lightning_effect:
                        self.lightning_effect.update()
                        self.lightning_effect.draw(self.screen)

                # Gambar efek shadow bergerak
                if self.shadow_effect:
                    self.shadow_effect.draw(self.screen)

                # Gambar efek partikel abu gelap
                if self.ash_effect:
                    self.ash_effect.draw(self.screen)

                # Tampilkan red overlay jika ninja baru terkena serangan
                current_time = pygame.time.get_ticks()
                if (self.zombie_attack_time > 0 and
                    current_time - self.zombie_attack_time < self.zombie_attack_duration):
                    self.screen.blit(self.red_overlay, (0, 0))

                # Update frame
                self.update_frame()

                # Cek downfall (ninja atau zombie jatuh ke jurang)
                self.downfall_action()

                # Cek apakah ninja mati
                if not self.ninja.get_alive():
                    self.show_game_over_screen()
                    # Jika self.running masih True setelah game over screen, lanjutkan game
                    if not self.running:
                        break

        pygame.quit()
