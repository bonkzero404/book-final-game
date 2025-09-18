# File untuk objek latar belakang dan jalan
# File ini mengatur pemandangan game seperti latar belakang dan jalan yang bergerak

import pygame  # Library untuk membuat game
from constants import BOSS_SCENE  # Import konstanta boss scene
from leaf_effect import LeafEffect  # Import efek daun beterbangan

class Object:
    """Kelas Object - Cetakan untuk membuat latar belakang game

    Kelas ini mengatur semua pemandangan dalam game seperti:
    - Latar belakang yang bergerak
    - Jalan tempat ninja berlari
    - Jurang-jurang berbahaya
    """

    def __init__(self, image_path, screen, max_scene, ninja_speed, boss_mode=False):
        """Membuat objek latar belakang baru

        Parameter:
        - image_path: Folder tempat gambar disimpan
        - screen: Layar game
        - max_scene: Berapa banyak pemandangan yang ada
        - ninja_speed: Seberapa cepat ninja bergerak
        - boss_mode: Mode boss tanpa jurang (default: False)
        """
        self.screen = screen          # Layar game
        # Gunakan BOSS_SCENE jika dalam mode boss, otherwise gunakan max_scene normal
        self.max_scene = BOSS_SCENE if boss_mode else max_scene    # Jumlah pemandangan maksimal
        self.ninja_speed = ninja_speed # Kecepatan ninja
        self.boss_mode = boss_mode    # Mode boss tanpa jurang

        # Muat dan siapkan gambar latar belakang
        background_path = image_path + '/Background.png'  # Lokasi file gambar latar
        self.background_image = pygame.image.load(background_path).convert()  # Muat gambar
        # Ubah ukuran latar belakang agar pas dengan layar
        self.background_resized = pygame.transform.scale(
            self.background_image,
            (screen.get_width(), screen.get_height())
        )

        # Muat dan siapkan gambar jalan
        road_path = image_path + '/Tile_11.png'  # Lokasi file gambar jalan
        self.road_image = pygame.image.load(road_path).convert_alpha()  # Muat gambar jalan
        self.road_width = self.road_image.get_width()  # Ukur lebar satu ubin jalan

        # Variabel posisi dan status
        self.x = 0                           # Posisi objek secara umum
        self.road_x = 0                      # Posisi jalan (untuk efek bergerak)
        self.scene = 0                       # Pemandangan saat ini (mulai dari 0)
        self.background_x1 = 0               # Posisi latar belakang pertama
        self.background_x2 = screen.get_width()  # Posisi latar belakang kedua

        # Muat objek alam untuk latar belakang natural
        self.nature_objects = {}  # Kamus objek alam berdasarkan jenis

        # Definisi objek alam yang akan digunakan
        nature_items = {
            'bunga': 1,      # Object_1.png - Bunga cantik
            'batu': 2,       # Object_2.png - Batu alam
            'plang': 5,      # Object_5.png - Plang petunjuk
            'rumput': 6,     # Object_6.png - Rumput hijau
            'tumbuhan': 12,  # Object_12.png - Tumbuhan datar
            'pohon': 16,     # Object_16.png - Pohon besar
            'pohon_medium': 21  # Object_21.png - Pohon sedang
        }

        # Muat setiap jenis objek alam
        for obj_name, obj_number in nature_items.items():
            obj_path = image_path + f'/Object_{obj_number}.png'  # Lokasi file objek
            try:
                obj_image = pygame.image.load(obj_path).convert_alpha()  # Muat gambar objek
                self.nature_objects[obj_name] = obj_image  # Simpan dengan nama yang mudah diingat
            except pygame.error:
                print(f"Tidak dapat memuat {obj_path}")  # Peringatan jika file tidak ada

        # Pengaturan jurang berbahaya
        self.is_downfall = False             # Apakah sedang ada jurang?
        # Jika mode boss, tidak ada jurang sama sekali
        if self.boss_mode:
            self.downfall_positions = []     # Tidak ada jurang di mode boss
        else:
            self.downfall_positions = [6, 9, 11, 14, 15, 18, 22, 25, 28, 31, 35, 38, 42, 45, 48, 52, 55, 58, 62, 65, 68, 72, 75, 78, 82, 85]  # Daftar posisi di mana jurang muncul (diperbanyak untuk tantangan lebih sulit)
        self.x_downfall = []                 # Daftar posisi jurang yang aktif

        # Buat lingkungan alam yang natural
        self.nature_positions = []  # Posisi objek alam

        # Buat pola alam yang realistis
        import random
        random.seed(42)  # Gunakan seed tetap agar pola konsisten

        # Tempatkan objek alam dengan pola natural (hanya di area tiles yang aman)
        for section in range(0, 80):  # Buat 80 bagian lingkungan untuk scene yang sangat panjang
            section_x = section * 300  # Setiap bagian selebar 300 pixel

            # Pohon besar (jarang, di belakang jalan)
            if random.random() < 0.3:  # 30% kemungkinan ada pohon besar
                for attempt in range(10):  # Coba maksimal 10 kali untuk posisi aman
                    obj_x = section_x + random.randint(0, 200)
                    obj_width = self.nature_objects['pohon'].get_width() if 'pohon' in self.nature_objects else 100
                    if self._is_safe_position(obj_x, obj_width):
                        # Hitung posisi Y agar bagian bawah objek berada di Y=360 dengan offset tambahan
                        obj_height = self.nature_objects['pohon'].get_height() if 'pohon' in self.nature_objects else 100
                        offset_tambahan = 100  # Offset untuk menurunkan objek lebih jauh
                        self.nature_positions.append({
                            'type': 'pohon',
                            'x': obj_x,
                            'y': 360 - obj_height + offset_tambahan  # Bagian bawah objek di Y=360 + offset
                        })
                        break

            # Pohon medium (lebih sering, di samping jalan)
            if random.random() < 0.5:  # 50% kemungkinan ada pohon medium
                for attempt in range(10):  # Coba maksimal 10 kali untuk posisi aman
                    obj_x = section_x + random.randint(50, 250)
                    obj_width = self.nature_objects['pohon_medium'].get_width() if 'pohon_medium' in self.nature_objects else 80
                    if self._is_safe_position(obj_x, obj_width):
                        # Hitung posisi Y agar bagian bawah objek berada di Y=360 dengan offset tambahan
                        obj_height = self.nature_objects['pohon_medium'].get_height() if 'pohon_medium' in self.nature_objects else 80
                        offset_tambahan = 100  # Offset untuk menurunkan objek lebih jauh
                        self.nature_positions.append({
                            'type': 'pohon_medium',
                            'x': obj_x,
                            'y': 360 - obj_height + offset_tambahan  # Bagian bawah objek di Y=360 + offset
                        })
                        break

            # Tumbuhan datar (sering, di tepi jalan)
            for _ in range(random.randint(1, 3)):  # 1-3 tumbuhan per bagian
                for attempt in range(10):  # Coba maksimal 10 kali untuk posisi aman
                    obj_x = section_x + random.randint(0, 280)
                    obj_width = self.nature_objects['tumbuhan'].get_width() if 'tumbuhan' in self.nature_objects else 60
                    if self._is_safe_position(obj_x, obj_width):
                        # Hitung posisi Y agar bagian bawah objek berada di Y=360 dengan offset tambahan
                        obj_height = self.nature_objects['tumbuhan'].get_height() if 'tumbuhan' in self.nature_objects else 60
                        offset_tambahan = 100  # Offset untuk menurunkan objek lebih jauh
                        self.nature_positions.append({
                            'type': 'tumbuhan',
                            'x': obj_x,
                            'y': 360 - obj_height + offset_tambahan  # Bagian bawah objek di Y=360 + offset
                        })
                        break

            # Rumput (banyak, di area jalan)
            for _ in range(random.randint(2, 5)):  # 2-5 rumput per bagian
                for attempt in range(10):  # Coba maksimal 10 kali untuk posisi aman
                    obj_x = section_x + random.randint(0, 300)
                    obj_width = self.nature_objects['rumput'].get_width() if 'rumput' in self.nature_objects else 40
                    if self._is_safe_position(obj_x, obj_width):
                        # Hitung posisi Y agar bagian bawah objek berada di Y=360 dengan offset tambahan
                        obj_height = self.nature_objects['rumput'].get_height() if 'rumput' in self.nature_objects else 40
                        offset_tambahan = 100  # Offset untuk menurunkan objek lebih jauh
                        self.nature_positions.append({
                            'type': 'rumput',
                            'x': obj_x,
                            'y': 360 - obj_height + offset_tambahan  # Bagian bawah objek di Y=360 + offset
                        })
                        break

            # Bunga (cantik, di area jalan yang aman)
            if random.random() < 0.7:  # 70% kemungkinan ada bunga
                for _ in range(random.randint(1, 2)):  # 1-2 bunga per bagian
                    for attempt in range(10):  # Coba maksimal 10 kali untuk posisi aman
                        obj_x = section_x + random.randint(20, 280)
                        obj_width = self.nature_objects['bunga'].get_width() if 'bunga' in self.nature_objects else 30
                        if self._is_safe_position(obj_x, obj_width):
                            # Hitung posisi Y agar bagian bawah objek berada di Y=360 dengan offset tambahan
                            obj_height = self.nature_objects['bunga'].get_height() if 'bunga' in self.nature_objects else 30
                            offset_tambahan = 100  # Offset untuk menurunkan objek lebih jauh
                            self.nature_positions.append({
                                'type': 'bunga',
                                'x': obj_x,
                                'y': 360 - obj_height + offset_tambahan  # Bagian bawah objek di Y=360 + offset
                            })
                            break

            # Batu (jarang, di area jalan yang aman)
            if random.random() < 0.4:  # 40% kemungkinan ada batu
                for attempt in range(10):  # Coba maksimal 10 kali untuk posisi aman
                    obj_x = section_x + random.randint(0, 300)
                    obj_width = self.nature_objects['batu'].get_width() if 'batu' in self.nature_objects else 50
                    if self._is_safe_position(obj_x, obj_width):
                        # Hitung posisi Y agar bagian bawah objek berada di Y=360 dengan offset tambahan
                        obj_height = self.nature_objects['batu'].get_height() if 'batu' in self.nature_objects else 50
                        offset_tambahan = 100  # Offset untuk menurunkan objek lebih jauh
                        self.nature_positions.append({
                            'type': 'batu',
                            'x': obj_x,
                            'y': 360 - obj_height + offset_tambahan  # Bagian bawah objek di Y=360 + offset
                        })
                        break

            # Plang (sangat jarang, strategis di area jalan)
            if random.random() < 0.1:  # 10% kemungkinan ada plang
                for attempt in range(10):  # Coba maksimal 10 kali untuk posisi aman
                    obj_x = section_x + random.randint(50, 250)
                    obj_width = self.nature_objects['plang'].get_width() if 'plang' in self.nature_objects else 70
                    if self._is_safe_position(obj_x, obj_width):
                        # Hitung posisi Y agar bagian bawah objek berada di Y=360 dengan offset tambahan
                        obj_height = self.nature_objects['plang'].get_height() if 'plang' in self.nature_objects else 70
                        offset_tambahan = 100  # Offset untuk menurunkan objek lebih jauh
                        self.nature_positions.append({
                            'type': 'plang',
                            'x': obj_x,
                            'y': 360 - obj_height + offset_tambahan  # Bagian bawah objek di Y=360 + offset
                        })
                        break

        # Debug: Informasi objek alam (dinonaktifkan untuk performa)
        # print(f"Total objek alam dibuat: {len(self.nature_positions)}")
        # print(f"Objek alam yang berhasil dimuat: {list(self.nature_objects.keys())}")
        # for i, obj in enumerate(self.nature_positions[:5]):
        #     print(f"   {i+1}. {obj['type']} di posisi ({obj['x']}, {obj['y']})")
        # if len(self.nature_positions) > 5:
        #     print(f"   ... dan {len(self.nature_positions) - 5} objek lainnya")
        
        # Inisialisasi efek daun beterbangan
        self.leaf_effect = LeafEffect(screen.get_width(), screen.get_height())

    def _is_safe_position(self, x_position, obj_width=0):
        """Mengecek apakah posisi X aman (tidak di area jurang)

        Parameter:
        - x_position: Posisi X yang akan dicek
        - obj_width: Lebar objek untuk memastikan seluruh objek aman

        Return:
        - True jika posisi aman (ada tiles jalan)
        - False jika posisi berbahaya (area jurang)
        """
        # Hitung indeks tile berdasarkan posisi X relatif terhadap jalan
        # Posisi objek harus dihitung relatif terhadap posisi jalan awal
        relative_x = x_position
        tile_index_start = int(relative_x // self.road_width)
        tile_index_end = int((relative_x + obj_width) // self.road_width)

        # Cek apakah ada tile jurang di area yang akan ditempati objek
        for tile_idx in range(tile_index_start, tile_index_end + 1):
            if tile_idx in self.downfall_positions:
                return False  # Posisi berbahaya (objek akan melewati jurang)

        # Cek juga tile di sekitarnya untuk memastikan objek tidak terlalu dekat dengan jurang
        # Cek tile sebelah kiri dan kanan dari area objek
        left_tile = tile_index_start - 1
        right_tile = tile_index_end + 1

        # Tambahkan margin keamanan berdasarkan lebar objek
        safety_margin = max(self.road_width * 0.2, obj_width * 0.5)  # Minimal 20% lebar tile atau 50% lebar objek

        if left_tile in self.downfall_positions or right_tile in self.downfall_positions:
            # Jika ada jurang di sebelah, beri jarak aman yang lebih besar
            tile_start = tile_index_start * self.road_width
            tile_end = (tile_index_end + 1) * self.road_width

            # Pastikan objek tidak terlalu dekat dengan tepi tile yang berbatasan dengan jurang
            if (left_tile in self.downfall_positions and (relative_x - tile_start) < safety_margin) or \
               (right_tile in self.downfall_positions and (tile_end - (relative_x + obj_width)) < safety_margin):
                return False  # Terlalu dekat dengan jurang

        return True  # Posisi aman (ada tiles jalan)

    # Getter methods
    def get_x(self):
        """Mengembalikan posisi x saat ini."""
        return self.x

    def get_road_x(self):
        """Mengembalikan posisi x jalan saat ini."""
        return self.road_x

    def get_scene(self):
        """Mengembalikan scene saat ini."""
        return self.scene

    def get_road_width(self):
        """Mengembalikan lebar tile jalan."""
        return self.road_width

    def get_downfall_positions(self):
        """Mengembalikan daftar posisi jurang."""
        return self.x_downfall

    # Setter methods
    def set_downfall(self, is_downfall=True):
        """Mengatur status downfall."""
        self.is_downfall = is_downfall

    def draw_road(self, screen):
        """Gambar jalan yang diulang dengan posisi dinamis, melewati area jurang."""
        road_y = 350  # Posisi Y tetap untuk jalan
        index = 0

        # Hitung range untuk menggambar jalan
        start_x = self.road_x
        end_x = self.road_x + self.screen.get_width() * (self.max_scene + 1)

        for x in range(start_x, end_x, self.road_width):
            # Jika mode boss, gambar semua jalan tanpa jurang
            if self.boss_mode:
                # Gambar tile jalan di semua posisi
                screen.blit(self.road_image, (x, road_y))
            else:
                # Cek apakah posisi ini adalah jurang (mode normal)
                if index in self.downfall_positions:
                    # Simpan posisi jurang jika belum ada
                    if len(self.x_downfall) < len(self.downfall_positions) and x not in self.x_downfall:
                        self.x_downfall.append(x)
                    # Skip menggambar jalan di posisi jurang
                else:
                    # Gambar tile jalan
                    screen.blit(self.road_image, (x, road_y))

            index += 1


    def draw_background(self, screen):
        """Gambar latar belakang di layar."""
        screen.blit(self.background_resized, (self.background_x1, 0))
        screen.blit(self.background_resized, (self.background_x2, 0))

    def _update_road_position(self, ninja=None):
        """Update posisi jalan berdasarkan input keyboard dan prioritas tombol ninja."""
        if self.is_downfall:
            return

        keys = pygame.key.get_pressed()
        max_x = self.screen.get_width() * self.max_scene

        # Gunakan sistem prioritas tombol yang sama dengan ninja
        if ninja and hasattr(ninja, 'last_direction_key'):
            # Jika kedua tombol ditekan, gunakan prioritas tombol terakhir
            if keys[pygame.K_a] and keys[pygame.K_d]:
                if ninja.last_direction_key == 'a':
                    # Bergerak ke kiri (prioritas tombol A)
                    self.x -= self.ninja_speed
                    self.road_x += self.ninja_speed
                    # Batasi agar tidak melewati batas kiri
                    if self.x <= 0:
                        self.x = 0
                        self.road_x = 0
                elif ninja.last_direction_key == 'd':
                    # Bergerak ke kanan (prioritas tombol D)
                    if self.x < max_x:
                        self.x += self.ninja_speed
                        self.road_x -= self.ninja_speed
            elif keys[pygame.K_a]:  # Hanya tombol A ditekan
                self.x -= self.ninja_speed
                self.road_x += self.ninja_speed
                # Batasi agar tidak melewati batas kiri
                if self.x <= 0:
                    self.x = 0
                    self.road_x = 0
            elif keys[pygame.K_d]:  # Hanya tombol D ditekan
                if self.x < max_x:
                    self.x += self.ninja_speed
                    self.road_x -= self.ninja_speed
        else:
            # Fallback ke logika lama jika ninja tidak tersedia
            if keys[pygame.K_a]:  # Bergerak ke kiri
                self.x -= self.ninja_speed
                self.road_x += self.ninja_speed
                # Batasi agar tidak melewati batas kiri
                if self.x <= 0:
                    self.x = 0
                    self.road_x = 0
            elif keys[pygame.K_d]:  # Bergerak ke kanan
                if self.x < max_x:
                    self.x += self.ninja_speed
                    self.road_x -= self.ninja_speed

    def _set_scene(self):
        """Update scene berdasarkan posisi x."""
        screen_width = self.screen.get_width()

        if self.x % screen_width == 0:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_a]:  # Bergerak ke kiri
                self.scene = max(0, self.scene - 1)
            else:  # Bergerak ke kanan
                if self.x <= (screen_width * self.max_scene):
                    self.scene += 1

    def _move_background(self):
        """Gerakkan background dengan efek parallax."""
        if self.is_downfall or self.x <= 0 or self.x >= (self.screen.get_width() * self.max_scene):
            return

        keys = pygame.key.get_pressed()
        bg_speed = 2  # Kecepatan background (lebih lambat dari jalan)
        screen_width = self.screen.get_width()

        # Geser background berdasarkan arah gerakan
        if keys[pygame.K_a]:  # Bergerak ke kiri
            self.background_x1 += bg_speed
            self.background_x2 += bg_speed
        else:  # Bergerak ke kanan
            self.background_x1 -= bg_speed
            self.background_x2 -= bg_speed

        # Reset posisi background untuk efek infinite scrolling
        if self.background_x1 <= -screen_width:
            self.background_x1 = self.background_x2 + screen_width
        elif self.background_x1 >= screen_width:
            self.background_x1 = self.background_x2 - screen_width

        if self.background_x2 <= -screen_width:
            self.background_x2 = self.background_x1 + screen_width
        elif self.background_x2 >= screen_width:
            self.background_x2 = self.background_x1 - screen_width

    def update_frame(self, ninja=None):
        """Update semua elemen objek setiap frame."""
        keys = pygame.key.get_pressed()

        # Update posisi hanya jika ada input gerakan
        if keys[pygame.K_a] or keys[pygame.K_d]:
            self._update_road_position(ninja)
            self._set_scene()
            self._move_background()

    def draw(self, screen):
        """
        Menggambar semua elemen latar belakang dan jalan
        Ini adalah method utama untuk menampilkan semua objek di layar
        """
        # Gambar latar belakang yang bergerak
        self.draw_background(screen)

        # Gambar objek alam natural di latar belakang
        self.draw_nature_objects(screen)

        # Gambar jalan dengan variasi tiles
        self.draw_road(screen)

    def draw_nature_objects(self, screen):
        """
        Menggambar objek alam di latar belakang
        Menciptakan lingkungan yang natural dan indah
        """
        # Gambar setiap objek alam berdasarkan layer (belakang ke depan)
        objects_drawn = 0  # Hitung berapa objek yang digambar

        # Layer 1: Pohon besar (paling belakang)
        for obj_data in self.nature_positions:
            if obj_data['type'] == 'pohon':
                obj_x = obj_data['x'] - self.x
                obj_y = obj_data['y']

                # Hanya gambar objek yang terlihat di layar
                if -300 <= obj_x <= self.screen.get_width() + 300:
                    if 'pohon' in self.nature_objects:
                        screen.blit(self.nature_objects['pohon'], (obj_x, obj_y))
                        objects_drawn += 1

        # Layer 2: Pohon medium
        for obj_data in self.nature_positions:
            if obj_data['type'] == 'pohon_medium':
                obj_x = obj_data['x'] - self.x
                obj_y = obj_data['y']

                if -250 <= obj_x <= self.screen.get_width() + 250:
                    if 'pohon_medium' in self.nature_objects:
                        screen.blit(self.nature_objects['pohon_medium'], (obj_x, obj_y))
                        objects_drawn += 1

        # Layer 3: Plang dan batu
        for obj_data in self.nature_positions:
            if obj_data['type'] in ['plang', 'batu']:
                obj_x = obj_data['x'] - self.x
                obj_y = obj_data['y']

                if -200 <= obj_x <= self.screen.get_width() + 200:
                    obj_type = obj_data['type']
                    if obj_type in self.nature_objects:
                        screen.blit(self.nature_objects[obj_type], (obj_x, obj_y))
                        objects_drawn += 1

        # Layer 4: Tumbuhan, rumput, dan bunga (paling depan)
        for obj_data in self.nature_positions:
            if obj_data['type'] in ['tumbuhan', 'rumput', 'bunga']:
                obj_x = obj_data['x'] - self.x
                obj_y = obj_data['y']

                if -150 <= obj_x <= self.screen.get_width() + 150:
                    obj_type = obj_data['type']
                    if obj_type in self.nature_objects:
                        screen.blit(self.nature_objects[obj_type], (obj_x, obj_y))
                        objects_drawn += 1

        # Debug: Informasi rendering (dinonaktifkan untuk performa)
        # if hasattr(self, 'debug_counter'):
        #     self.debug_counter += 1
        # else:
        #     self.debug_counter = 0
        # if self.debug_counter % 60 == 0:  # Setiap 1 detik (60 FPS)
        #     print(f"Objek alam digambar: {objects_drawn}, Posisi kamera: {self.x}")
        
        # Update dan gambar efek daun beterbangan
        # Kumpulkan posisi pohon yang terlihat untuk spawn daun
        visible_tree_positions = []
        for obj_data in self.nature_positions:
            if obj_data['type'] in ['pohon', 'pohon_medium', 'tumbuhan']:
                obj_x = obj_data['x'] - self.x
                obj_y = obj_data['y']
                
                # Hanya pohon yang terlihat di layar
                if -300 <= obj_x <= self.screen.get_width() + 300:
                    visible_tree_positions.append({
                        'x': obj_x,
                        'y': obj_y
                    })
        
        # Update efek daun dengan posisi pohon yang terlihat
        self.leaf_effect.update(visible_tree_positions)
        
        # Gambar efek daun di atas semua objek alam
        self.leaf_effect.draw(screen)

    def reset(self):
        """Reset semua posisi dan state ke kondisi awal."""
        self.x = 0
        self.road_x = 0
        self.scene = 0
        self.background_x1 = 0
        self.background_x2 = self.screen.get_width()
        self.is_downfall = False
        self.x_downfall = []
        
        # Reset boss mode ke normal
        self.boss_mode = False
        # Reset max_scene ke nilai normal (bukan BOSS_SCENE)
        from constants import MAX_SCENE
        self.max_scene = MAX_SCENE
        
        # Reset posisi jurang berdasarkan mode
        if self.boss_mode:
            self.downfall_positions = []     # Tidak ada jurang di mode boss
        else:
            self.downfall_positions = [6, 9, 11, 14, 15, 18, 22, 25, 28, 31, 35, 38, 42, 45, 48, 52, 55, 58, 62, 65, 68, 72, 75, 78, 82, 85]  # Daftar posisi di mana jurang muncul
        
        # Regenerate objek alam dengan pola baru
        self.nature_positions = []  # Reset posisi objek alam
        
        # Buat pola alam yang realistis dengan seed tetap
        import random
        random.seed(42)  # Gunakan seed tetap agar pola konsisten seperti permainan awal
        
        # Tempatkan objek alam dengan pola natural (hanya di area tiles yang aman)
        for section in range(0, 80):  # Buat 80 bagian lingkungan untuk scene yang sangat panjang
            section_x = section * 300  # Setiap bagian selebar 300 pixel

            # Pohon besar (jarang, di belakang jalan)
            if random.random() < 0.3:  # 30% kemungkinan ada pohon besar
                for attempt in range(10):  # Coba maksimal 10 kali untuk posisi aman
                    obj_x = section_x + random.randint(0, 200)
                    obj_width = self.nature_objects['pohon'].get_width() if 'pohon' in self.nature_objects else 100
                    if self._is_safe_position(obj_x, obj_width):
                        # Hitung posisi Y agar bagian bawah objek berada di Y=360 dengan offset tambahan
                        obj_height = self.nature_objects['pohon'].get_height() if 'pohon' in self.nature_objects else 100
                        offset_tambahan = 100  # Offset untuk menurunkan objek lebih jauh
                        self.nature_positions.append({
                            'type': 'pohon',
                            'x': obj_x,
                            'y': 360 - obj_height + offset_tambahan  # Bagian bawah objek di Y=360 + offset
                        })
                        break

            # Pohon medium (lebih sering, di samping jalan)
            if random.random() < 0.5:  # 50% kemungkinan ada pohon medium
                for attempt in range(10):  # Coba maksimal 10 kali untuk posisi aman
                    obj_x = section_x + random.randint(50, 250)
                    obj_width = self.nature_objects['pohon_medium'].get_width() if 'pohon_medium' in self.nature_objects else 80
                    if self._is_safe_position(obj_x, obj_width):
                        # Hitung posisi Y agar bagian bawah objek berada di Y=360 dengan offset tambahan
                        obj_height = self.nature_objects['pohon_medium'].get_height() if 'pohon_medium' in self.nature_objects else 80
                        offset_tambahan = 100  # Offset untuk menurunkan objek lebih jauh
                        self.nature_positions.append({
                            'type': 'pohon_medium',
                            'x': obj_x,
                            'y': 360 - obj_height + offset_tambahan  # Bagian bawah objek di Y=360 + offset
                        })
                        break

            # Tumbuhan datar (sering, di tepi jalan)
            for _ in range(random.randint(1, 3)):  # 1-3 tumbuhan per bagian
                for attempt in range(10):  # Coba maksimal 10 kali untuk posisi aman
                    obj_x = section_x + random.randint(0, 280)
                    obj_width = self.nature_objects['tumbuhan'].get_width() if 'tumbuhan' in self.nature_objects else 60
                    if self._is_safe_position(obj_x, obj_width):
                        # Hitung posisi Y agar bagian bawah objek berada di Y=360 dengan offset tambahan
                        obj_height = self.nature_objects['tumbuhan'].get_height() if 'tumbuhan' in self.nature_objects else 60
                        offset_tambahan = 100  # Offset untuk menurunkan objek lebih jauh
                        self.nature_positions.append({
                            'type': 'tumbuhan',
                            'x': obj_x,
                            'y': 360 - obj_height + offset_tambahan  # Bagian bawah objek di Y=360 + offset
                        })
                        break

            # Rumput (banyak, di area jalan)
            for _ in range(random.randint(2, 5)):  # 2-5 rumput per bagian
                for attempt in range(10):  # Coba maksimal 10 kali untuk posisi aman
                    obj_x = section_x + random.randint(0, 300)
                    obj_width = self.nature_objects['rumput'].get_width() if 'rumput' in self.nature_objects else 40
                    if self._is_safe_position(obj_x, obj_width):
                        # Hitung posisi Y agar bagian bawah objek berada di Y=360 dengan offset tambahan
                        obj_height = self.nature_objects['rumput'].get_height() if 'rumput' in self.nature_objects else 40
                        offset_tambahan = 100  # Offset untuk menurunkan objek lebih jauh
                        self.nature_positions.append({
                            'type': 'rumput',
                            'x': obj_x,
                            'y': 360 - obj_height + offset_tambahan  # Bagian bawah objek di Y=360 + offset
                        })
                        break

            # Bunga (cantik, di area jalan yang aman)
            if random.random() < 0.7:  # 70% kemungkinan ada bunga
                for _ in range(random.randint(1, 2)):  # 1-2 bunga per bagian
                    for attempt in range(10):  # Coba maksimal 10 kali untuk posisi aman
                        obj_x = section_x + random.randint(20, 280)
                        obj_width = self.nature_objects['bunga'].get_width() if 'bunga' in self.nature_objects else 30
                        if self._is_safe_position(obj_x, obj_width):
                            # Hitung posisi Y agar bagian bawah objek berada di Y=360 dengan offset tambahan
                            obj_height = self.nature_objects['bunga'].get_height() if 'bunga' in self.nature_objects else 30
                            offset_tambahan = 100  # Offset untuk menurunkan objek lebih jauh
                            self.nature_positions.append({
                                'type': 'bunga',
                                'x': obj_x,
                                'y': 360 - obj_height + offset_tambahan  # Bagian bawah objek di Y=360 + offset
                            })
                            break

            # Batu (jarang, di area jalan yang aman)
            if random.random() < 0.4:  # 40% kemungkinan ada batu
                for attempt in range(10):  # Coba maksimal 10 kali untuk posisi aman
                    obj_x = section_x + random.randint(0, 300)
                    obj_width = self.nature_objects['batu'].get_width() if 'batu' in self.nature_objects else 50
                    if self._is_safe_position(obj_x, obj_width):
                        # Hitung posisi Y agar bagian bawah objek berada di Y=360 dengan offset tambahan
                        obj_height = self.nature_objects['batu'].get_height() if 'batu' in self.nature_objects else 50
                        offset_tambahan = 100  # Offset untuk menurunkan objek lebih jauh
                        self.nature_positions.append({
                            'type': 'batu',
                            'x': obj_x,
                            'y': 360 - obj_height + offset_tambahan  # Bagian bawah objek di Y=360 + offset
                        })
                        break

            # Plang (sangat jarang, strategis di area jalan)
            if random.random() < 0.1:  # 10% kemungkinan ada plang
                for attempt in range(10):  # Coba maksimal 10 kali untuk posisi aman
                    obj_x = section_x + random.randint(50, 250)
                    obj_width = self.nature_objects['plang'].get_width() if 'plang' in self.nature_objects else 70
                    if self._is_safe_position(obj_x, obj_width):
                        # Hitung posisi Y agar bagian bawah objek berada di Y=360 dengan offset tambahan
                        obj_height = self.nature_objects['plang'].get_height() if 'plang' in self.nature_objects else 70
                        offset_tambahan = 100  # Offset untuk menurunkan objek lebih jauh
                        self.nature_positions.append({
                            'type': 'plang',
                            'x': obj_x,
                            'y': 360 - obj_height + offset_tambahan  # Bagian bawah objek di Y=360 + offset
                        })
                        break
        
        # Reset efek daun beterbangan
        self.leaf_effect = LeafEffect(self.screen.get_width(), self.screen.get_height())
