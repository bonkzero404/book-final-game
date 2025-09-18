import pygame
import math
import random

class BossProjectile:
    """Class untuk projectile bola bercahaya boss"""
    
    def __init__(self, screen, start_x, start_y, target_x, target_y, speed=8, homing=True):
        """Inisialisasi projectile boss"""
        self.screen = screen
        self.x = start_x
        self.y = start_y
        self.speed = speed
        self.active = True
        self.homing = homing  # Apakah projectile mengikuti target
        
        # Target awal
        self.target_x = target_x
        self.target_y = target_y
        
        # Hitung arah projectile menuju target
        distance = math.sqrt((target_x - start_x)**2 + (target_y - start_y)**2)
        if distance > 0:
            self.velocity_x = (target_x - start_x) / distance * speed
            self.velocity_y = (target_y - start_y) / distance * speed
        else:
            self.velocity_x = speed
            self.velocity_y = 0
            
        # Efek visual bola bercahaya
        self.radius = 15
        self.glow_radius = 25
        self.color = (255, 255, 100)  # Kuning terang
        self.glow_color = (255, 255, 150, 100)  # Kuning dengan transparansi
        
        # Efek berkedip
        self.pulse_timer = 0
        self.pulse_speed = 0.2
        
        # Damage projectile
        self.damage = 15
        
        # Batas layar untuk menghapus projectile
        self.max_distance = 800
        self.start_x = start_x
        self.start_y = start_y
        
    def update(self, ninja_x=None, ninja_y=None):
        """Update posisi dan efek projectile"""
        if not self.active:
            return
            
        # Update target jika homing dan ninja position diberikan
        if self.homing and ninja_x is not None and ninja_y is not None:
            self.target_x = ninja_x
            self.target_y = ninja_y
            
            # Recalculate velocity menuju target baru
            distance = math.sqrt((self.target_x - self.x)**2 + (self.target_y - self.y)**2)
            if distance > 0:
                self.velocity_x = (self.target_x - self.x) / distance * self.speed
                self.velocity_y = (self.target_y - self.y) / distance * self.speed
            
        # Gerakkan projectile
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Update efek pulse
        self.pulse_timer += self.pulse_speed
        
        # Hapus projectile jika sudah terlalu jauh
        distance_traveled = math.sqrt((self.x - self.start_x)**2 + (self.y - self.start_y)**2)
        if distance_traveled > self.max_distance:
            self.active = False
            
        # Hapus projectile jika keluar layar
        if (self.x < -50 or self.x > self.screen.get_width() + 50 or 
            self.y < -50 or self.y > self.screen.get_height() + 50):
            self.active = False
            
    def draw(self):
        """Gambar projectile dengan efek bercahaya"""
        if not self.active:
            return
            
        # Efek pulse untuk ukuran
        pulse_factor = 1 + 0.3 * math.sin(self.pulse_timer * 10)
        current_radius = int(self.radius * pulse_factor)
        current_glow_radius = int(self.glow_radius * pulse_factor)
        
        # Gambar efek glow (lingkaran luar)
        glow_surface = pygame.Surface((current_glow_radius * 2, current_glow_radius * 2), pygame.SRCALPHA)
        for i in range(5):
            alpha = 30 - i * 5
            radius = current_glow_radius - i * 3
            if radius > 0:
                pygame.draw.circle(glow_surface, (*self.glow_color[:3], alpha), 
                                 (current_glow_radius, current_glow_radius), radius)
        
        glow_rect = glow_surface.get_rect(center=(int(self.x), int(self.y)))
        self.screen.blit(glow_surface, glow_rect)
        
        # Gambar bola utama
        pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), current_radius)
        
        # Gambar highlight di tengah
        highlight_radius = max(1, current_radius // 3)
        highlight_color = (255, 255, 255)
        pygame.draw.circle(self.screen, highlight_color, 
                         (int(self.x - current_radius//3), int(self.y - current_radius//3)), 
                         highlight_radius)
        
        # Gambar partikel berkilau di sekitar bola
        for i in range(3):
            angle = self.pulse_timer * 5 + i * 120  # 120 derajat apart
            particle_x = self.x + math.cos(math.radians(angle)) * (current_radius + 10)
            particle_y = self.y + math.sin(math.radians(angle)) * (current_radius + 10)
            pygame.draw.circle(self.screen, (255, 255, 200), 
                             (int(particle_x), int(particle_y)), 2)
                             
    def get_rect(self):
        """Dapatkan rectangle untuk collision detection"""
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)
                          
    def hit_target(self):
        """Projectile mengenai target"""
        self.active = False
        # TODO: Tambahkan efek ledakan di sini jika diperlukan
        
    def get_damage(self):
        """Dapatkan damage projectile"""
        return self.damage
        
    def is_active(self):
        """Cek apakah projectile masih aktif"""
        return self.active