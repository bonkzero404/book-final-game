import pygame, random, math  # Library untuk game, random, dan matematika

class Lightning:
    """Kelas untuk satu kilatan petir"""
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.active = False
        self.duration = 0
        self.max_duration = random.randint(3, 8)  # Frame durasi kilatan
        self.branches = []
        self.flash_alpha = 0
        
    def trigger(self):
        """Memicu kilatan petir"""
        self.active = True
        self.duration = 0
        self.flash_alpha = 255
        self.branches = []
        
        # Buat cabang-cabang petir
        num_branches = random.randint(3, 6)
        for _ in range(num_branches):
            branch = self._create_branch()
            self.branches.append(branch)
            
    def _create_branch(self):
        """Buat satu cabang petir"""
        # Titik awal dari atas layar
        start_x = random.randint(100, self.screen_width - 100)
        start_y = 0
        
        points = [(start_x, start_y)]
        current_x = start_x
        current_y = start_y
        
        # Buat jalur zigzag ke bawah
        segments = random.randint(8, 15)
        for i in range(segments):
            # Gerakan ke bawah dengan variasi horizontal
            current_y += random.randint(30, 60)
            current_x += random.randint(-40, 40)
            
            # Batasi agar tidak keluar layar
            current_x = max(50, min(self.screen_width - 50, current_x))
            current_y = min(self.screen_height, current_y)
            
            points.append((current_x, current_y))
            
            # Berhenti jika sudah sampai bawah
            if current_y >= self.screen_height - 50:
                break
                
        return points
        
    def update(self):
        """Update efek petir"""
        if self.active:
            self.duration += 1
            
            # Fade out flash
            self.flash_alpha = max(0, 255 - (self.duration * 40))
            
            # Matikan petir setelah durasi habis
            if self.duration >= self.max_duration:
                self.active = False
                self.flash_alpha = 0
                
    def draw(self, screen):
        """Gambar efek petir"""
        if not self.active:
            return
            
        # Gambar flash putih di seluruh layar
        if self.flash_alpha > 0:
            flash_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            flash_surface.fill((255, 255, 255, min(self.flash_alpha, 100)))
            screen.blit(flash_surface, (0, 0))
            
        # Gambar cabang-cabang petir
        for branch in self.branches:
            if len(branch) > 1:
                # Gambar garis utama petir
                for i in range(len(branch) - 1):
                    # Warna putih terang untuk petir
                    color = (255, 255, 255)
                    thickness = random.randint(2, 4)
                    
                    pygame.draw.line(screen, color, branch[i], branch[i + 1], thickness)
                    
                    # Tambah efek glow
                    glow_color = (200, 200, 255, 100)
                    glow_surface = pygame.Surface((abs(branch[i+1][0] - branch[i][0]) + 10, 
                                                 abs(branch[i+1][1] - branch[i][1]) + 10), pygame.SRCALPHA)
                    pygame.draw.line(glow_surface, glow_color[:3], 
                                   (5, 5), 
                                   (abs(branch[i+1][0] - branch[i][0]) + 5, 
                                    abs(branch[i+1][1] - branch[i][1]) + 5), thickness + 4)
                    
                    screen.blit(glow_surface, (min(branch[i][0], branch[i+1][0]) - 5, 
                                             min(branch[i][1], branch[i+1][1]) - 5))

class LightningEffect:
    """Kelas untuk efek petir lengkap"""
    def __init__(self, screen_width, screen_height, ground_explosion_callback=None):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.lightning = Lightning(screen_width, screen_height)
        self.next_strike_time = 0
        self.strike_interval = random.randint(120, 300)  # Frame antara petir (2-5 detik di 60fps)
        
        # Callback untuk efek ledakan tanah
        self.ground_explosion_callback = ground_explosion_callback
        
        # Suara petir (placeholder untuk implementasi suara nanti)
        self.thunder_ready = False
        
    def update(self):
        """Update efek petir"""
        self.next_strike_time += 1
        
        # Trigger petir secara random
        if self.next_strike_time >= self.strike_interval and not self.lightning.active:
            self.lightning.trigger()
            self.next_strike_time = 0
            self.strike_interval = random.randint(120, 300)  # Reset interval
            self.thunder_ready = True
            
            # Trigger efek ledakan tanah jika callback tersedia
            if self.ground_explosion_callback and self.lightning.branches:
                # Ambil titik akhir dari cabang petir pertama sebagai lokasi ledakan
                last_point = self.lightning.branches[0][-1]
                explosion_x, explosion_y = last_point
                self.ground_explosion_callback(explosion_x, explosion_y)
            
        # Update lightning
        self.lightning.update()
        
    def draw(self, screen):
        """Gambar efek petir"""
        self.lightning.draw(screen)
        
    def force_strike(self):
        """Paksa petir menyambar (untuk efek dramatis)"""
        if not self.lightning.active:
            self.lightning.trigger()
            self.thunder_ready = True
            
            # Trigger efek ledakan tanah jika callback tersedia
            if self.ground_explosion_callback and self.lightning.branches:
                # Ambil titik akhir dari cabang petir pertama sebagai lokasi ledakan
                last_point = self.lightning.branches[0][-1]
                explosion_x, explosion_y = last_point
                self.ground_explosion_callback(explosion_x, explosion_y)
            
    def is_striking(self):
        """Cek apakah sedang ada petir"""
        return self.lightning.active
        
    def get_thunder_ready(self):
        """Cek apakah suara guntur siap diputar"""
        if self.thunder_ready:
            self.thunder_ready = False
            return True
        return False