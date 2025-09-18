# FILE KARAKTER NINJA
# File ini berisi semua yang berhubungan dengan karakter ninja kita!
# Ninja bisa berlari, melompat, menyerang, dan melempar kunai

# Import (mengambil) library dan file yang kita butuhkan
import os, re, random, math, pygame  # Library untuk membuat game
from helper import resize_with_aspect_ratio  # Fungsi untuk mengubah ukuran gambar
from constants import MAX_WIDTH, MAX_HEIGHT  # Ukuran layar game
from kunai import Kunai  # File untuk senjata kunai ninja

class Ninja:
    """Kelas Ninja - Karakter utama dalam permainan!

    Kelas ini seperti 'cetakan' untuk membuat karakter ninja.
    Ninja punya banyak kemampuan seperti berlari, melompat, dan menyerang!
    """
    def __init__(self, sprite_folder, screen, ninja_ground, ninja_speed):
        """Fungsi untuk membuat ninja baru (seperti melahirkan ninja!)

        Parameter:
        - sprite_folder: Folder tempat gambar-gambar ninja disimpan
        - screen: Layar tempat ninja akan muncul
        - ninja_ground: Ketinggian tanah tempat ninja berdiri
        - ninja_speed: Seberapa cepat ninja bisa bergerak
        """

        # Dictionary (kamus) untuk menyimpan semua gerakan ninja
        # Seperti buku panduan gerakan ninja!
        self.actions = {
            'Attack': [],      # Gerakan menyerang
            'Climb': [],       # Gerakan memanjat
            'Dead': [],        # Gerakan ketika ninja kalah
            'Glide': [],       # Gerakan melayang di udara
            'Idle': [],        # Gerakan diam/menunggu
            'Jump': [],        # Gerakan melompat
            'Jump_Attack': [], # Gerakan menyerang sambil melompat
            'Jump_Throw': [],  # Gerakan melempar kunai sambil melompat
            'Run': [],         # Gerakan berlari
            'Slide': [],       # Gerakan meluncur
            'Throw': [],       # Gerakan melempar kunai
        }
        # Pengaturan kecepatan dan layar
        self.ninja_speed = ninja_speed  # Seberapa cepat ninja bergerak
        self.screen = screen            # Layar tempat ninja muncul

        # Tentukan jenis kelamin ninja berdasarkan sprite_folder
        self.gender = 'female' if 'female' in sprite_folder else 'male'

        # Pengaturan animasi ninja
        self.current_action = 'Idle'    # Gerakan yang sedang dilakukan (mulai dengan diam)
        self.current_frame = 0          # Frame animasi yang sedang ditampilkan
        self.ninja_ground = ninja_ground # Ketinggian tanah
        self.load_sprites(sprite_folder) # Memuat semua gambar ninja

        # Posisi ninja di layar (koordinat x, y)
        self.x = 0                      # Posisi horizontal (kiri-kanan)
        self.y = self.ninja_ground      # Posisi vertikal (atas-bawah), mulai di tanah

        # Pengaturan untuk melompat dan gravitasi
        self.vel_y = 0                  # Kecepatan vertikal (naik/turun)
        self.on_ground = True           # Apakah ninja sedang berdiri di tanah?
        self.jump_power = -20           # Seberapa kuat ninja melompat (angka minus = ke atas)
        self.gravity = 1                # Gaya gravitasi yang menarik ninja ke bawah

        # Arah hadap ninja (kiri atau kanan)
        self.facing_left = False        # False = menghadap kanan, True = menghadap kiri
        
        # Sistem prioritas tombol untuk menangani A dan D ditekan bersamaan
        self.last_direction_key = None  # Tombol arah terakhir yang ditekan ('a' atau 'd')

        # Pengaturan senjata Kunai (senjata lempar ninja)
        self.kunai_image = pygame.image.load(os.path.join(sprite_folder, 'Kunai.png')).convert_alpha()
        self.kunai_image = resize_with_aspect_ratio(self.kunai_image, 40, 40)  # Ubah ukuran kunai
        # self.kunai_image = pygame.transform.rotate(self.kunai_image, 270)  # Putar kunai (tidak dipakai)
        self.kunai_width, _ = self.kunai_image.get_size()  # Dapatkan lebar kunai
        self.kunai_flip = False         # Apakah kunai perlu dibalik?
        self.kunais = []                # Daftar semua kunai yang sedang terbang

        # Pengaturan untuk sistem pertarungan
        self.is_attacked = False        # Apakah ninja sedang diserang?
        self.attack_time = 0            # Waktu kapan ninja terakhir diserang
        self.attack_duration = 0.05     # Berapa lama efek serangan berlangsung (dalam detik)

        # Pengaturan kesehatan ninja
        self.health = 100               # Nyawa ninja (100 = sehat penuh, 0 = mati)
        self.alive = True               # Apakah ninja masih hidup?
        self.is_falling_to_cliff = False # Apakah ninja sedang jatuh ke jurang?


        # Pengaturan tampilan teks
        self.font = pygame.font.Font(None, 28)  # Font untuk menulis teks di layar
        self.name = "Shinoboy"                  # Nama ninja kita

        # Efek overlay merah (tidak dipakai saat ini)
        # self.red_overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        # self.red_overlay.fill((255, 0, 0))  # Warna merah
        # self.red_overlay.set_alpha(128)  # Set transparansi (0-255, 255 = tidak transparan, 0 = transparan)

    def get_x(self):
        """Mendapatkan posisi horizontal ninja (kiri-kanan)"""
        return self.x

    def get_y(self):
        """Mendapatkan posisi vertikal ninja (atas-bawah)"""
        return self.y

    def add_y(self):
        """Membuat ninja jatuh ke bawah (untuk jatuh ke jurang)"""
        self.is_falling_to_cliff = True  # Tandai ninja sedang jatuh ke jurang
        self.on_ground = False  # Ninja tidak lagi di tanah
        self.y += 10  # Gerakkan ninja 10 pixel ke bawah

    def get_alive(self):
        """Mengecek apakah ninja masih hidup"""
        return self.alive

    def set_alive(self, alive):
        """Mengatur status hidup/mati ninja"""
        self.alive = alive

    def set_name(self, name):
        """Mengubah nama ninja"""
        self.name = name

    def load_sprites(self, sprite_folder):
        """Memuat semua gambar ninja dari folder

        Fungsi ini seperti membuka album foto ninja!
        Setiap foto (sprite) akan dikelompokkan berdasarkan gerakan ninja.
        """
        # Baca semua file gambar di folder ninja
        for filename in sorted(os.listdir(sprite_folder)):
            if filename.endswith('.png'):  # Hanya ambil file gambar PNG
                path = os.path.join(sprite_folder, filename)  # Buat alamat lengkap file
                sprite = pygame.image.load(path).convert_alpha()  # Muat gambar

                # Cari tahu gambar ini untuk gerakan apa
                # Seperti mengelompokkan foto berdasarkan aktivitas
                for action in self.actions:
                    # Cocokkan nama file dengan nama gerakan
                    if re.match(rf"^{action}(__\d{{3}}\.png)$", filename) or re.match(rf"^{action}(_\d{{3}}\.png)$", filename):
                        # Beberapa gerakan perlu ukuran khusus
                        if action in ['Jump_Throw', 'Slide']:
                            sprite_resized = resize_with_aspect_ratio(sprite, MAX_WIDTH - 20, MAX_HEIGHT - 20)
                            self.actions[action].append(sprite_resized)
                        else:
                            sprite_resized = resize_with_aspect_ratio(sprite, MAX_WIDTH, MAX_HEIGHT)
                            self.actions[action].append(sprite_resized)

    def get_current_sprite(self):
        """Mengambil gambar ninja yang sedang aktif

        Fungsi ini seperti memilih kostum ninja yang tepat!
        Tergantung gerakan apa yang sedang dilakukan ninja.
        """
        # Ambil gambar sesuai gerakan dan frame saat ini
        sprite = self.actions[self.current_action][self.current_frame]

        # Perbesar gambar untuk gerakan serangan agar terlihat lebih keren!
        if self.current_action in ['Attack', 'Jump_Attack', 'Jump_Throw']:
            if self.gender == 'female':
                # Ninja perempuan diperbesar 10% lebih besar (1.2 + 0.1 = 1.3)
                sprite = pygame.transform.smoothscale(sprite, (sprite.get_width() * 1.1, sprite.get_height() * 1.1))
            else:
                # Ninja laki-laki tetap 20%
                sprite = pygame.transform.smoothscale(sprite, (sprite.get_width() * 1.2, sprite.get_height() * 1.2))

        # Balik gambar jika ninja menghadap kiri
        if self.facing_left:
            return pygame.transform.flip(sprite, True, False)  # Flip sprite jika bergerak ke kiri
        return sprite

    def _handle_movement_keys(self):
        keys = pygame.key.get_pressed()
        
        # Jika kedua tombol ditekan, gunakan prioritas tombol terakhir
        if keys[pygame.K_a] and keys[pygame.K_d]:
            if self.last_direction_key == 'a':
                self.facing_left = True
            elif self.last_direction_key == 'd':
                self.facing_left = False
        elif keys[pygame.K_a] and not keys[pygame.K_d]:
            self.facing_left = True
        elif keys[pygame.K_d] and not keys[pygame.K_a]:
            self.facing_left = False

    def _update_action_frame(self):
        if self.current_action == 'Jump' and self.current_frame == len(self.actions['Jump']) - 1:
            if self.on_ground:
                self.current_frame = len(self.actions['Jump']) - 1  # Pertahankan frame terakhir
                # Jika tombol run masih ditekan, lanjutkan ke Run setelah mendarat
                if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_d]:
                   self.set_action('Run')
                else:
                    self.set_action('Idle')  # Ganti aksi ke Idle setelah mendarat

        elif self.current_action == 'Run':
            if self.current_frame < len(self.actions['Run']) - 1:
                self.current_frame += 1  # Lanjutkan animasi 'Run'
            else:
                self.current_frame = 0  # Reset frame 'Run' jika sudah mencapai akhir animasi
        else:
            self._update_non_run_actions()

    def _update_non_run_actions(self):
        # Jika aksi selain 'Run', lanjutkan animasi satu kali
        if self.current_frame < len(self.actions[self.current_action]) - 1:
            self.current_frame += 1
        else:
            self._handle_end_of_action()

    def _handle_end_of_action(self):
        # Jika aksi adalah Jump_Attack atau Jump_Throw, tetap di frame terakhir
        if self.current_action in ['Jump_Attack', 'Jump_Throw']:
            if self.on_ground:
                # Jika tombol run ditekan, kembali ke Run
                if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_d]:
                    self.set_action('Run')
                else:
                    self.set_action('Idle')  # Kembali ke Idle jika tidak ada tombol yang ditekan
        elif self.current_action == 'Slide':
            # Jika tombol run ditekan, kembali ke Run
            if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_d]:
                self.set_action('Run')
                self.y -= 30
            else:
                self.set_action('Idle')
                self.y -= 30
        elif self.current_action == 'Glide':
            if self.on_ground:
                # Jika tombol run ditekan, kembali ke Run
                if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_d]:
                    self.set_action('Run')
                else:
                    self.set_action('Idle')  # Kembali ke Idle jika tidak ada tombol yang ditekan
        elif self.current_action == 'Attack':
            # Setelah animasi Attack selesai, cek apakah masih ada input gerakan
            if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_d]:
                self.set_action('Run')  # Kembali ke Run jika tombol gerakan masih ditekan
            else:
                self.set_action('Idle')  # Kembali ke Idle jika tidak ada input
        elif self.current_action == 'Throw':
            # Setelah animasi Throw selesai, cek apakah masih ada input gerakan
            if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_d]:
                self.set_action('Run')  # Kembali ke Run jika tombol gerakan masih ditekan
            else:
                self.set_action('Idle')  # Kembali ke Idle jika tidak ada input
        else:
            self.set_action('Idle')  # Kembali ke Idle jika selesai animasi lainnya
            self.current_frame = 0  # Reset frame ke awal untuk aksi berikutnya

    def update_frame(self):
        """Perbarui frame animasi."""
        if self.alive:
            self._handle_movement_keys()
            self._update_action_frame()
        else:
            if self.current_action != 'Dead':
                self.set_action('Dead')

            if self.current_action == 'Dead':
                if self.current_frame < len(self.actions['Dead']) - 1:
                    self.current_frame += 1  # Lanjutkan animasi 'Run'

    def _handle_keydown_event(self, event):
        if event.key == pygame.K_a:
            self.last_direction_key = 'a'  # Catat tombol A sebagai tombol terakhir
            self.facing_left = True
            if self.current_action == 'Glide':
                self.set_action('Glide')
            else:
                self.set_action('Run')  # Set aksi Run
        elif event.key == pygame.K_d:
            self.last_direction_key = 'd'  # Catat tombol D sebagai tombol terakhir
            self.facing_left = False
            if self.current_action == 'Glide':
                self.set_action('Glide')
            else:
                self.set_action('Run')  # Set aksi Run
        elif event.key == pygame.K_w:
            if self.on_ground:  # Jika karakter ada di tanah
                self.vel_y = self.jump_power  # Memberikan gaya lompat
                self.on_ground = False  # Karakter tidak lagi di tanah
                self.set_action('Jump')  # Set aksi ke Jump saat karakter melompat
        elif event.key == pygame.K_j:
            # Glide
            if self.current_action == 'Jump':
                self.set_action('Glide')
        elif event.key == pygame.K_s:
            if self.current_action == 'Run':
                self.y += 30
                self.set_action('Slide')  # Slide saat Run + S
        elif event.key == pygame.K_k:
            # Aksi serangan berdasarkan kondisi ninja
            if self.current_action == 'Jump':
                self.set_action('Jump_Attack')
            elif self.current_action == 'Idle':
                self.set_action('Attack')  # Aksi Attack saat diam
            elif self.current_action == 'Run':
                self.set_action('Attack')  # Aksi Attack saat berlari
        elif event.key == pygame.K_l:
            # Aksi Jump_Throw hanya bisa dilakukan saat karakter sedang melompat
            if self.current_action == 'Jump':
                self.set_action('Jump_Throw')
                self.throw_kunai() # Lempar kunai
            elif self.current_action == 'Idle':
                self.set_action('Throw')  # Aksi Throw
                self.throw_kunai() # Lempar kunai
            elif self.current_action == 'Run':
                self.set_action('Jump_Throw')  # Aksi Jump_Throw
                self.throw_kunai() # Lempar kunai

    def _handle_keyup_event(self, event):
        if event.key == pygame.K_a or event.key == pygame.K_d:
            if not pygame.key.get_pressed()[pygame.K_a] and not pygame.key.get_pressed()[pygame.K_d]:
                if self.current_action != 'Glide':
                    self.set_action('Idle')

        if event.key == pygame.K_j and self.current_action == 'Glide':
            if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_d]:
                self.set_action('Run')
            else:
                self.set_action('Idle')

    def event_handler(self, event):
        # Ganti aksi dengan tombol
        if event.type == pygame.KEYDOWN:
            self._handle_keydown_event(event)
        elif event.type == pygame.KEYUP:
            self._handle_keyup_event(event)

    def set_action(self, action):
        """Set aksi ninja dan reset frame."""
        if action in self.actions:
            self.current_action = action
            self.current_frame = 0  # Reset frame ketika aksi berubah

    def draw_health_bar(self):
        """Gambar health bar ninja dengan border."""
        # Ukuran dan posisi health bar
        bar_width = 200
        bar_height = 20
        bar_x = 10  # Posisi X
        bar_y = 10  # Posisi Y
        border_thickness = 3  # Ketebalan border
        radius = 10  # Radius sudut

        # Gambar border health bar (coklat)
        pygame.draw.rect(self.screen, (139, 69, 19), (bar_x - border_thickness, bar_y - border_thickness, bar_width + 2 * border_thickness, bar_height + 2 * border_thickness), border_radius=radius)  # Border coklat

        # Gambar background health bar
        pygame.draw.rect(self.screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height), border_radius=radius)  # Background merah

        # Hitung lebar health bar berdasarkan kesehatan
        health_ratio = self.health / 100
        current_health_width = bar_width * health_ratio

        # Gambar health bar yang terisi (hijau)
        pygame.draw.rect(self.screen, (102,146,61), (bar_x, bar_y, current_health_width, bar_height), border_radius=radius)  # Background hijau

        text_surface = self.font.render(self.name, True, (255, 255, 255))  # Teks putih
        text_rect = text_surface.get_rect(center=(10 + 100, 20))  # Pusatkan teks di atas health bar
        self.screen.blit(text_surface, text_rect)  # Gambar teks di layar

    def damage(self):
        """Metode untuk menandai ninja diserang."""
        self.health -= 10  # Kurangi nyawa ninja

        if self.health == 0:
            self.set_action('Dead')
            self.alive = False

    def apply_gravity(self):
        """Menambahkan gravitasi pada karakter."""
        if not self.on_ground:
            self.vel_y += self.gravity  # Menambahkan kecepatan vertikal karena gravitasi

            if self.vel_y > 0:
                if self.current_action == 'Glide':
                    self.y += 1
                else:
                    self.y += self.vel_y
            else:
                self.y += self.vel_y

            # Jika karakter mencapai tanah dan tidak sedang jatuh ke jurang
            if self.y >= self.ninja_ground and not self.is_falling_to_cliff:
                self.y = self.ninja_ground  # Set posisi y agar tetap di tanah
                self.vel_y = 0  # Reset kecepatan vertikal
                self.on_ground = True  # Karakter kembali ke tanah

    def draw(self, screen):
        """Gambar sprite ninja pada posisi tertentu."""
        # Gunakan ukuran sprite asli untuk perhitungan posisi
        original_sprite = self.actions[self.current_action][self.current_frame]
        if self.facing_left:
            original_sprite = pygame.transform.flip(original_sprite, True, False)

        screen_size_x, _ = original_sprite.get_size()
        self.x = self.screen.get_width() / 2 - (screen_size_x / 2)

        # Gambar sprite yang sudah di-scale (jika perlu) pada posisi yang benar
        current_sprite = self.get_current_sprite()
        screen.blit(current_sprite, (self.x, self.y))
        # # Gambar sparks
        # for spark in self.sparks:
        #     spark.draw(screen)
        self.draw_kunai()
        self.apply_gravity()

    def reset(self):
        self.alive = True
        self.health = 100
        self.x = 0  # Reset posisi X ninja ke posisi awal
        self.y = self.ninja_ground
        self.vel_y = 0
        self.on_ground = True
        self.is_falling_to_cliff = False  # Reset flag jatuh ke jurang
        self.set_action('Jump')

    def draw_kunai(self):
        """Gambar kunai."""
        for kunai in self.kunais:
            if kunai.active:
                kunai.draw(self.screen)

    def throw_kunai(self):
        """Melempar kunai."""
        kunai_speed = 10 if not self.facing_left else -10  # Tentukan arah kunai
        if self.facing_left:
            if not self.kunai_flip:
                self.kunai_image = pygame.transform.flip(self.kunai_image, True, False)
                self.kunai_flip = True
        else:
            if self.kunai_flip:
                self.kunai_flip = False
                self.kunai_image = pygame.transform.flip(self.kunai_image, True, False)
            else:
                self.kunai_image = pygame.transform.flip(self.kunai_image, False, False)
        kunai = Kunai(self.screen, self.kunai_image, self.x + (self.kunai_width // 2), self.y + 40, kunai_speed)  # Buat kunai baru
        self.kunais.append(kunai)  # Tambahkan kunai ke daftar

    def update_kunais(self):
        """Update semua kunai yang dilempar."""
        for kunai in self.kunais:
            kunai.update()  # Update posisi kunai
        # Hapus kunai yang tidak aktif
        self.kunais = [kunai for kunai in self.kunais if kunai.active]
