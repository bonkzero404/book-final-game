# File untuk karakter zombie (musuh ninja)
# File ini mengatur bagaimana zombie bergerak, menyerang, dan berinteraksi

import os, re, math, random, pygame  # Library untuk membuat game
from helper import resize_with_aspect_ratio  # Fungsi untuk mengubah ukuran gambar
from constants import MAX_WIDTH, MAX_HEIGHT  # Ukuran layar game

class Zombie:
    """Kelas Zombie - Cetakan untuk membuat karakter zombie

    Zombie adalah musuh ninja yang akan berjalan dan menyerang.
    Mereka bisa bergerak, diserang, dan mati.
    """
    def __init__(self, sprite_folder, screen, zombie_ground, zombie_speed, init_pos, on_death_callback=None):
        """Membuat zombie baru

        Parameter:
        - sprite_folder: Folder tempat gambar zombie
        - screen: Layar game
        - zombie_ground: Tinggi tanah tempat zombie berjalan
        - zombie_speed: Seberapa cepat zombie bergerak
        - init_pos: Posisi awal zombie
        - on_death_callback: Fungsi yang dipanggil saat zombie mati
        """
        # Kamus untuk menyimpan semua gerakan zombie
        self.actions = {
            'Attack': [],    # Gambar saat zombie menyerang
            'Dead': [],      # Gambar saat zombie mati
            'Idle': [],      # Gambar saat zombie diam
            'Walk': [],      # Gambar saat zombie berjalan
        }
        self.zombie_speed = zombie_speed  # Seberapa cepat zombie bergerak
        self.screen = screen  # Layar tempat zombie muncul
        self.current_action = 'Walk'  # Gerakan yang sedang dilakukan (mulai dengan Walk)
        self.current_frame = 0  # Frame animasi yang sedang ditampilkan
        self.zombie_ground = zombie_ground  # Tinggi tanah tempat zombie berdiri
        self.load_sprites(sprite_folder)  # Muat semua gambar zombie

        # Posisi zombie di layar (x = kiri-kanan, y = atas-bawah)
        self.init_pos = init_pos  # Posisi awal zombie
        self.relative_x = self.init_pos  # Posisi relatif zombie
        self.x = self.init_pos + self.relative_x  # Posisi X zombie di layar
        self.y = self.zombie_ground  # Posisi Y zombie (tinggi tanah)

        # Arah gerakan zombie
        self.facing_left = True  # Zombie menghadap kiri (True) atau kanan (False)
        self.is_init = False  # Apakah zombie baru dibuat
        self.health = 100  # Nyawa zombie (100 = sehat penuh)

        # Pengaturan animasi zombie
        self.frame_update_time = 0.1  # Seberapa cepat animasi berubah (0.1 detik)
        self.last_frame_update = pygame.time.get_ticks()  # Kapan terakhir animasi berubah

        # Status zombie saat bertarung
        self.is_hit = False  # Apakah zombie sedang terkena serangan
        self.is_hit_ninja = False  # Apakah zombie mengenai ninja
        self.is_downfall = False  # Apakah zombie jatuh ke jurang
        self.min_distance = 30  # Jarak minimum antar zombie (agar tidak bertabrakan)
        self.alive = True  # Apakah zombie masih hidup

        # Pengaturan kematian zombie
        self.death_time = None  # Kapan zombie mati
        self.death_duration = 5000  # Berapa lama zombie mati sebelum hilang (5 detik)
        self.tries_avoid_downfall = 0  # Berapa kali zombie mencoba menghindari jurang
        self.long_idle = 0  # Berapa lama zombie diam
        self.on_death_callback = on_death_callback  # Callback saat zombie mati
        self.death_callback_called = False  # Apakah callback sudah dipanggil

        # Pengaturan gerakan zombie yang lebih pintar
        self.direction_change_cooldown = 0  # Waktu tunggu sebelum bisa berubah arah
        self.max_direction_change_cooldown = 30  # Maksimal waktu tunggu (30 frame)
        self.stuck_counter = 0  # Penghitung untuk deteksi zombie yang macet
        self.last_position = self.relative_x  # Posisi terakhir (untuk cek apakah zombie macet)

        # Variabel untuk perilaku di ujung jurang
        self.at_edge = False  # Apakah zombie berada di ujung jurang
        self.ninja_passed = False  # Apakah ninja sudah melewati zombie
        self.last_ninja_x = None  # Posisi ninja terakhir untuk deteksi melewati

        # Status aktivasi zombie yang persisten
        self.is_activated = False  # Apakah zombie sudah pernah diaktivasi (tetap True setelah aktivasi pertama)
        self.chase_distance = 300  # Jarak untuk aktivasi awal zombie

    def get_relative_x(self):
        """Mengambil posisi relatif zombie"""
        return self.relative_x

    def get_x(self):
        """Mengambil posisi X zombie (kiri-kanan)"""
        return self.x

    def get_y(self):
        """Mengambil posisi Y zombie (atas-bawah)"""
        return self.y

    def set_downfall(self):
        """Membuat zombie jatuh ke jurang"""
        self.is_downfall = True

    def get_alive(self):
        """Cek apakah zombie masih hidup"""
        return self.alive

    def set_alive(self, alive):
        """Mengatur status hidup/mati zombie"""
        self.alive = alive

    def extract_number(self, file_name):
        """Mengambil nomor urut dari nama file gambar

        Contoh: 'Walk (1).png' akan menghasilkan angka 1
        Ini untuk mengurutkan gambar animasi dengan benar.
        """
        match = re.search(r'\((\d+)\)', file_name)  # Cari angka di dalam tanda kurung
        return int(match.group(1)) if match else 0  # Return angka atau 0 jika tidak ditemukan

    def load_sprites(self, sprite_folder):
        """Memuat semua gambar zombie dari folder

        Fungsi ini seperti membuka album foto zombie!
        Setiap foto akan dikelompokkan berdasarkan gerakan zombie.
        """
        # Baca semua file di folder zombie
        files = os.listdir(sprite_folder)
        # Ambil hanya file gambar yang sesuai pola nama
        filtered_files = [file for file in files if re.search(r'(Idle|Walk|Attack|Dead) \(\d+\)\.png', file)]
        # Urutkan file berdasarkan nomor
        sorted_files = sorted(filtered_files, key=self.extract_number)

        # Muat setiap gambar
        for filename in sorted_files:
            if filename.endswith('.png'):  # Hanya file PNG
                path = os.path.join(sprite_folder, filename)  # Buat alamat lengkap file
                sprite = pygame.image.load(path).convert_alpha()  # Muat gambar

                # Kelompokkan gambar berdasarkan gerakan
                for action in self.actions:
                    # Cocokkan nama file dengan nama gerakan
                    if re.match(rf"^{action}\s\(\d+\)\.png$", filename):
                        # Gambar zombie mati dibuat lebih besar
                        if action == 'Dead':
                            sprite_resized = resize_with_aspect_ratio(sprite, MAX_WIDTH + 20, MAX_HEIGHT + 20)
                            self.actions[action].append(sprite_resized)
                        else:
                            sprite_resized = resize_with_aspect_ratio(sprite, MAX_WIDTH, MAX_HEIGHT)
                            self.actions[action].append(sprite_resized)



    def get_current_sprite(self):
        """Mengambil sprite untuk aksi saat ini."""
        action_to_use = self.current_action

        if action_to_use in self.actions and self.actions[action_to_use]:
            # Pastikan frame tidak melebihi jumlah sprite yang tersedia
            frame_index = min(self.current_frame, len(self.actions[action_to_use]) - 1)
            sprite = self.actions[action_to_use][frame_index]
        else:
            # Jika tidak ada sprite, kembalikan sprite default atau kosong
            return None  # Atau Anda bisa mengembalikan sprite default

        if self.facing_left:
            return pygame.transform.flip(sprite, True, False)

        return sprite


    def set_action(self, action):
        """Set aksi zombie dan reset frame."""
        if action in self.actions:
            self.current_action = action
            self.current_frame = 0

    def damage(self, damage_type='Normal'):
        """Metode untuk menandai zombie diserang."""
        self.health -= 5  # Kurangi nyawa ninja

        if damage_type == 'Double':
            self.health -= 5

        if damage_type == 'Kunai':
            self.health -= 5

        if self.health <= 0:
            self.set_action('Dead')
            # self.alive = False
            self.set_dead()

    def set_dead(self):
        """Cek jika zombie mati."""
        # Jika zombie hidup, set aksi Dead
        if self.alive:
            self.y += 10
            self.set_action('Dead')
            self.alive = False
            self.death_time = pygame.time.get_ticks()

            # Panggil callback untuk menambah score (hanya sekali)
            if self.on_death_callback and not self.death_callback_called:
                self.on_death_callback()
                self.death_callback_called = True
        else:
            self.y -= 10

    def is_ready_to_remove(self):
        """Cek apakah zombie sudah siap untuk dihapus."""
        if self.death_time is not None:
            current_time = pygame.time.get_ticks()
            if current_time - self.death_time >= self.death_duration:
                return True
        return False

    def update_frame(self, road_x, ninja_x, zombies, road_x_downfall=None, block_width=None):
        """Perbarui frame animasi dan posisi zombie."""
        # Hapus sparks setelah aksi attack selesai
        current_time = pygame.time.get_ticks()  # Ambil waktu saat ini
        if current_time - self.last_frame_update > self.frame_update_time * 1000:
            if self.alive:
                # Perbarui frame animasi
                action_for_animation = self.current_action

                if action_for_animation in self.actions and len(self.actions[action_for_animation]) > 0:
                    if self.current_frame < len(self.actions[action_for_animation]) - 1:
                        self.current_frame += 1
                    else:
                        self.current_frame = 0  # Reset frame jika sudah mencapai akhir animasi

                        # Jika zombie selesai menyerang di ujung jurang, kembali ke Walk
                        if self.current_action == 'Attack' and self.at_edge:
                            self.set_action('Walk')

                # self.avoid_collision(zombies)

                # Sistem chase: zombie yang sudah diaktivasi tetap mengejar ninja
                distance_to_ninja = abs(self.relative_x - ninja_x)

                # Aktivasi zombie jika ninja mendekat untuk pertama kali
                if distance_to_ninja <= self.chase_distance and not self.is_activated:
                    self.is_activated = True
                    self.is_chasing = True
                    if self.current_action == 'Idle':
                        self.set_action('Walk')  # Mulai mengejar

                # Zombie yang sudah diaktivasi tetap mengejar ninja
                if self.is_activated:
                    self.is_chasing = True
                    if self.current_action == 'Idle':
                        self.set_action('Walk')  # Tetap aktif mengejar
                else:
                    self.is_chasing = False
                    if self.current_action == 'Walk' and not self.at_edge:
                        self.set_action('Idle')  # Tetap idle jika belum diaktivasi

                # Update posisi zombie relatif terhadap jalan
                if self.current_action == 'Walk' and not self.is_downfall and self.is_chasing:
                    # Update cooldown dan deteksi stuck
                    if self.direction_change_cooldown > 0:
                        self.direction_change_cooldown -= 1

                    # Deteksi apakah zombie stuck (tidak bergerak)
                    if abs(self.relative_x - self.last_position) < 1:
                        self.stuck_counter += 1
                    else:
                        self.stuck_counter = 0
                        self.last_position = self.relative_x

                    # Deteksi ninja melewati zombie
                    if self.last_ninja_x is not None:
                        # Jika ninja bergerak dari satu sisi zombie ke sisi lain
                        if ((self.last_ninja_x < self.relative_x and ninja_x > self.relative_x) or
                            (self.last_ninja_x > self.relative_x and ninja_x < self.relative_x)):
                            self.ninja_passed = True
                            self.at_edge = False  # Reset status di ujung jurang
                    self.last_ninja_x = ninja_x

                    # Pergerakan zombie berdasarkan posisi ninja dengan pengecekan keamanan
                    if self.relative_x < ninja_x:
                        # Cek apakah posisi berikutnya aman sebelum bergerak ke kanan
                        next_position = self.relative_x + self.zombie_speed
                        if road_x_downfall and block_width and self.is_position_safe(next_position, road_x_downfall, block_width):
                            self.facing_left = False
                            self.relative_x += self.zombie_speed
                            self.at_edge = False  # Tidak di ujung jurang
                        elif road_x_downfall and block_width:
                            # Zombie berada di ujung jurang
                            self.at_edge = True
                            self.facing_left = False  # Tetap menghadap ninja

                            # Jika ninja belum melewati zombie, serang
                            if not self.ninja_passed:
                                self.set_action('Attack')
                            else:
                                # Jika ninja sudah melewati, baru boleh balik arah
                                if (self.direction_change_cooldown <= 0 or self.stuck_counter > 60):
                                    opposite_position = self.relative_x - self.zombie_speed
                                    if self.is_position_safe(opposite_position, road_x_downfall, block_width):
                                        self.facing_left = True
                                        self.relative_x -= self.zombie_speed
                                        self.direction_change_cooldown = self.max_direction_change_cooldown
                                        self.stuck_counter = 0
                                        self.ninja_passed = False  # Reset status
                                        self.at_edge = False
                                    else:
                                        self.set_action('Idle')
                        else:
                            # Jika tidak ada data jurang, bergerak normal
                            self.facing_left = False
                            self.relative_x += self.zombie_speed
                            self.at_edge = False
                    elif self.relative_x > ninja_x:
                        # Cek apakah posisi berikutnya aman sebelum bergerak ke kiri
                        next_position = self.relative_x - self.zombie_speed
                        if road_x_downfall and block_width and self.is_position_safe(next_position, road_x_downfall, block_width):
                            self.facing_left = True
                            self.relative_x -= self.zombie_speed
                            self.at_edge = False  # Tidak di ujung jurang
                        elif road_x_downfall and block_width:
                            # Zombie berada di ujung jurang
                            self.at_edge = True
                            self.facing_left = True  # Tetap menghadap ninja

                            # Jika ninja belum melewati zombie, serang
                            if not self.ninja_passed:
                                self.set_action('Attack')
                            else:
                                # Jika ninja sudah melewati, baru boleh balik arah
                                if (self.direction_change_cooldown <= 0 or self.stuck_counter > 60):
                                    opposite_position = self.relative_x + self.zombie_speed
                                    if self.is_position_safe(opposite_position, road_x_downfall, block_width):
                                        self.facing_left = False
                                        self.relative_x += self.zombie_speed
                                        self.direction_change_cooldown = self.max_direction_change_cooldown
                                        self.stuck_counter = 0
                                        self.ninja_passed = False  # Reset status
                                        self.at_edge = False
                                    else:
                                        self.set_action('Idle')
                        else:
                            # Jika tidak ada data jurang, bergerak normal
                            self.facing_left = True
                            self.relative_x -= self.zombie_speed
                            self.at_edge = False

                # Zombie jatuh ke jurang dengan gravitasi
                elif self.current_action == 'Walk' and self.is_downfall:
                    # Zombie berhenti bergerak horizontal tetapi jatuh ke bawah
                    if self.relative_x < ninja_x:
                        self.facing_left = False
                    elif self.relative_x > ninja_x:
                        self.facing_left = True

                    # Terapkan gravitasi - zombie jatuh ke bawah
                    if self.y < self.screen.get_height():  # Hanya jatuh jika belum keluar layar
                        self.y += 3  # Kecepatan jatuh zombie (dikurangi untuk performa)
                    else:
                        # Tandai sebagai mati hanya sekali
                        if self.current_action != 'Dead':
                            self.set_dead()

                elif self.current_action == 'Idle' and self.is_downfall:
                    # Zombie tetap idle ketika berada di jurang tetapi tetap jatuh
                    if self.relative_x < ninja_x:
                        self.facing_left = False
                    elif self.relative_x > ninja_x:
                        self.facing_left = True

                    # Terapkan gravitasi - zombie jatuh ke bawah
                    if self.y < self.screen.get_height():  # Hanya jatuh jika belum keluar layar
                        self.y += 3  # Kecepatan jatuh zombie (dikurangi untuk performa)
                    else:
                        # Tandai sebagai mati hanya sekali
                        if self.current_action != 'Dead':
                            self.set_dead()

                self.last_frame_update = current_time
            else:
                if self.current_action != 'Dead':
                    self.set_action('Dead')

                if self.current_action == 'Dead':

                    if self.current_frame < len(self.actions['Dead']) - 1:
                        self.current_frame += 1  # Lanjutkan animasi 'Run'

        # Posisi absolut zombie berdasarkan jalan
        self.x = road_x + self.relative_x

    def avoid_collision(self, zombies):
        """Mencegah zombie saling bertabrakan atau terlalu dekat."""
        for zombie in zombies:
            if zombie != self and not zombie.is_downfall:
                distance = self.get_distance((self.relative_x, self.y), (zombie.relative_x, zombie.y))
                if distance < self.min_distance:
                    # Menggeser posisi zombie ini sedikit untuk menghindari tabrakan
                    dx = self.relative_x - zombie.relative_x
                    dy = self.y - zombie.y
                    magnitude = math.sqrt(dx**2 + dy**2)

                    # Menghindari pembagian dengan nol
                    if magnitude > 0:
                        dx /= magnitude
                        dy /= magnitude

                        # Geser zombie ini sedikit menjauh
                        self.relative_x += dx * (self.min_distance - distance) * 0.5
                        self.y += dy * (self.min_distance - distance) * 0.5

    def get_distance(self, point1, point2):
        """Menghitung jarak antara dua titik (x, y)."""
        x1, y1 = point1
        x2, y2 = point2
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def is_position_safe(self, position, downfall_list, block_width):
        """Mengecek apakah posisi aman (tidak di jurang)."""
        for x in downfall_list:
            if position >= x and position <= x + block_width:
                return False
        return True

    def draw(self):
        """Gambar sprite zombie pada posisi tertentu."""
        sprite = self.get_current_sprite()
        if sprite:  # Pastikan sprite tidak None
            #center
            self.screen.blit(sprite, (self.x - sprite.get_width() // 2, self.y))
            # self.screen.blit(sprite, (self.x, self.y))

    def reset(self):
        """Reset posisi zombie ke posisi awal."""
        self.relative_x = self.init_pos
        self.x = self.init_pos + self.relative_x
        self.y = self.zombie_ground
        self.is_downfall = False
        self.is_hit = False
        self.alive = True
        self.health = 100

        # Reset variabel chase dan AI
        self.is_activated = False
        self.is_chasing = False
        self.direction_change_cooldown = 0
        self.stuck_counter = 0
        self.last_position = self.relative_x
        self.at_edge = False
        self.ninja_passed = False
        self.last_ninja_x = None

        # Reset ke Walk normal
        self.set_action('Walk')
