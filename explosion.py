# File untuk efek ledakan
# File ini membuat efek visual ledakan saat projectile boss mengenai ninja

import pygame
import math
import random

class Explosion:
    """Kelas Explosion - Cetakan untuk membuat efek ledakan
    
    Explosion adalah efek visual yang muncul saat projectile boss mengenai ninja.
    Ledakan terdiri dari partikel-partikel yang menyebar ke segala arah dengan warna yang berubah.
    """
    
    def __init__(self, x, y, size=50):
        """Membuat ledakan baru
        
        Parameter:
        - x: Posisi X ledakan
        - y: Posisi Y ledakan  
        - size: Ukuran maksimum ledakan
        """
        self.x = x
        self.y = y
        self.size = size
        self.max_size = size
        self.current_size = 0
        self.particles = []
        self.alive = True
        self.duration = 30  # Frame durasi ledakan
        self.frame_count = 0
        
        # Buat partikel ledakan
        self.create_particles()
    
    def create_particles(self):
        """Buat partikel-partikel ledakan"""
        particle_count = random.randint(15, 25)
        
        for _ in range(particle_count):
            # Arah acak untuk setiap partikel
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            
            # Posisi awal partikel (di tengah ledakan)
            particle_x = self.x
            particle_y = self.y
            
            # Kecepatan partikel berdasarkan arah
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed
            
            # Warna partikel (gradasi dari putih ke merah ke hitam)
            color_phase = random.uniform(0, 1)
            if color_phase < 0.3:
                color = (255, 255, 255)  # Putih (inti ledakan)
            elif color_phase < 0.7:
                color = (255, random.randint(100, 200), 0)  # Orange-merah
            else:
                color = (255, 0, 0)  # Merah
            
            # Ukuran partikel
            particle_size = random.randint(2, 6)
            
            particle = {
                'x': particle_x,
                'y': particle_y,
                'vel_x': vel_x,
                'vel_y': vel_y,
                'color': color,
                'size': particle_size,
                'life': random.randint(15, 25)
            }
            
            self.particles.append(particle)
    
    def update(self):
        """Update ledakan dan partikel-partikelnya"""
        if not self.alive:
            return
            
        self.frame_count += 1
        
        # Update ukuran ledakan utama
        progress = self.frame_count / self.duration
        if progress < 0.3:
            # Fase ekspansi cepat
            self.current_size = self.max_size * (progress / 0.3)
        elif progress < 0.7:
            # Fase stabil
            self.current_size = self.max_size
        else:
            # Fase kontraksi
            fade_progress = (progress - 0.7) / 0.3
            self.current_size = self.max_size * (1 - fade_progress)
        
        # Update partikel
        for particle in self.particles[:]:
            # Update posisi partikel
            particle['x'] += particle['vel_x']
            particle['y'] += particle['vel_y']
            
            # Tambahkan gravitasi ringan
            particle['vel_y'] += 0.1
            
            # Reduksi kecepatan (friction)
            particle['vel_x'] *= 0.98
            particle['vel_y'] *= 0.98
            
            # Kurangi life partikel
            particle['life'] -= 1
            
            # Fade warna partikel
            if particle['life'] < 10:
                fade_factor = particle['life'] / 10
                r, g, b = particle['color']
                particle['color'] = (
                    int(r * fade_factor),
                    int(g * fade_factor), 
                    int(b * fade_factor)
                )
            
            # Hapus partikel yang sudah mati
            if particle['life'] <= 0:
                self.particles.remove(particle)
        
        # Cek apakah ledakan sudah selesai
        if self.frame_count >= self.duration and len(self.particles) == 0:
            self.alive = False
    
    def draw(self, screen):
        """Gambar ledakan di layar"""
        if not self.alive:
            return
            
        # Gambar lingkaran ledakan utama
        if self.current_size > 0:
            # Efek ledakan berlapis
            for i in range(3):
                alpha = 100 - (i * 30)
                size = int(self.current_size - (i * 5))
                if size > 0:
                    # Buat surface dengan alpha untuk transparansi
                    explosion_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                    
                    # Warna ledakan berdasarkan fase
                    progress = self.frame_count / self.duration
                    if progress < 0.3:
                        color = (255, 255, 255, alpha)  # Putih terang
                    elif progress < 0.6:
                        color = (255, 200, 0, alpha)    # Orange
                    else:
                        color = (255, 100, 0, alpha)    # Merah
                    
                    pygame.draw.circle(explosion_surface, color, (size, size), size)
                    screen.blit(explosion_surface, (self.x - size, self.y - size))
        
        # Gambar partikel
        for particle in self.particles:
            if particle['size'] > 0:
                pygame.draw.circle(screen, particle['color'], 
                                 (int(particle['x']), int(particle['y'])), 
                                 particle['size'])
    
    def is_alive(self):
        """Cek apakah ledakan masih aktif"""
        return self.alive