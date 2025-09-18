# File untuk efek partikel abu gelap
# File ini mengatur partikel abu yang beterbangan untuk atmosfer suram

import pygame
import random
import math

class AshParticle:
    """Kelas untuk partikel abu individual"""
    def __init__(self, x, y, screen_width, screen_height):
        self.x = x
        self.y = y
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Properti partikel abu
        self.size = random.uniform(1, 4)  # Ukuran abu kecil
        self.speed_x = random.uniform(-0.5, 0.5)  # Gerakan horizontal lambat
        self.speed_y = random.uniform(0.2, 1.0)  # Jatuh ke bawah
        self.alpha = random.randint(30, 120)  # Transparansi
        self.life = random.uniform(3.0, 8.0)  # Durasi hidup dalam detik
        self.max_life = self.life
        
        # Warna abu gelap dengan variasi
        gray_value = random.randint(40, 80)
        self.color = (gray_value, gray_value, gray_value)
        
        # Efek bergoyang
        self.sway_offset = random.uniform(0, math.pi * 2)
        self.sway_amplitude = random.uniform(0.3, 0.8)
        self.sway_frequency = random.uniform(0.02, 0.05)
        
    def update(self, dt):
        """Update posisi dan status partikel abu"""
        # Gerakan jatuh dengan efek bergoyang
        self.sway_offset += self.sway_frequency
        sway_x = math.sin(self.sway_offset) * self.sway_amplitude
        
        self.x += self.speed_x + sway_x
        self.y += self.speed_y
        
        # Kurangi life time
        self.life -= dt
        
        # Fade out seiring waktu
        life_ratio = self.life / self.max_life
        self.alpha = int(120 * life_ratio) if life_ratio > 0 else 0
        
        # Reset posisi jika keluar layar
        if self.y > self.screen_height + 10:
            self.y = -10
            self.x = random.uniform(0, self.screen_width)
            self.life = random.uniform(3.0, 8.0)
            self.max_life = self.life
            
        if self.x < -10:
            self.x = self.screen_width + 10
        elif self.x > self.screen_width + 10:
            self.x = -10
            
    def is_alive(self):
        """Cek apakah partikel masih hidup"""
        return self.life > 0
        
    def draw(self, screen):
        """Gambar partikel abu"""
        if self.alpha > 0:
            # Buat surface dengan alpha untuk transparansi
            ash_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            color_with_alpha = (*self.color, self.alpha)
            pygame.draw.circle(ash_surface, color_with_alpha, 
                             (int(self.size), int(self.size)), int(self.size))
            screen.blit(ash_surface, (int(self.x - self.size), int(self.y - self.size)))

class AshEffect:
    """Kelas untuk mengelola efek partikel abu gelap"""
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.particles = []
        self.max_particles = 25  # Jumlah partikel abu
        self.spawn_timer = 0
        self.spawn_interval = 0.3  # Spawn partikel baru setiap 0.3 detik
        
        # Inisialisasi partikel awal
        for _ in range(self.max_particles // 2):
            x = random.uniform(0, screen_width)
            y = random.uniform(0, screen_height)
            self.particles.append(AshParticle(x, y, screen_width, screen_height))
            
    def update(self, dt):
        """Update semua partikel abu"""
        # Update partikel yang ada
        for particle in self.particles[:]:
            particle.update(dt)
            if not particle.is_alive():
                self.particles.remove(particle)
                
        # Spawn partikel baru
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval and len(self.particles) < self.max_particles:
            # Spawn dari atas layar
            x = random.uniform(0, self.screen_width)
            y = random.uniform(-50, -10)
            self.particles.append(AshParticle(x, y, self.screen_width, self.screen_height))
            self.spawn_timer = 0
            
    def render(self, screen):
        """Render semua partikel abu"""
        for particle in self.particles:
            particle.draw(screen)
            
    def draw(self, screen):
        """Gambar semua partikel abu (alias untuk render)"""
        self.render(screen)
            
    def set_intensity(self, intensity):
        """Atur intensitas efek abu (0.0 - 1.0)"""
        self.max_particles = int(25 * intensity)
        self.spawn_interval = 0.5 - (0.2 * intensity)  # Spawn lebih cepat saat intensitas tinggi