# File untuk efek vignette gelap
# Efek ini membuat tepi layar menjadi gelap untuk atmosfer horor

import pygame
import math

class MovingShadowEffect:
    """Kelas untuk mengatur efek vignette gelap"""
    
    def __init__(self, screen_width, screen_height):
        """Inisialisasi efek vignette gelap"""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.intensity = 0.3  # Intensitas efek (0.0 - 1.0)
        self.active = True  # Status aktif efek
        self.time = 0  # Waktu untuk animasi
        
        # Properti vignette
        self.vignette_radius = min(screen_width, screen_height) * 0.6
        self.max_alpha = 120  # Transparansi maksimal tepi
        
        # Optimasi: cache untuk menghindari regenerasi
        self.last_alpha = 0
        self.update_threshold = 10  # Minimal perubahan alpha untuk update
        
        # Buat surface untuk vignette
        self.vignette_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        self.base_vignette = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        self.create_base_vignette()
        self.update_vignette_alpha()
    
    def create_base_vignette(self):
        """Buat base vignette melingkar halus (optimized)"""
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        
        # Bersihkan surface
        self.base_vignette.fill((0, 0, 0, 0))
        
        # Radius untuk vignette melingkar
        max_radius = math.sqrt(center_x**2 + center_y**2) * 1.2
        inner_radius = max_radius * 0.4  # Area tengah yang tidak terpengaruh
        
        # Buat vignette melingkar dengan gradien halus
        for y in range(self.screen_height):
            for x in range(self.screen_width):
                # Hitung jarak dari pusat
                distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                
                # Hitung alpha berdasarkan jarak
                if distance <= inner_radius:
                    alpha = 0  # Area tengah transparan
                elif distance >= max_radius:
                    alpha = 180  # Tepi maksimal gelap
                else:
                    # Gradien halus dari inner ke outer radius
                    progress = (distance - inner_radius) / (max_radius - inner_radius)
                    # Gunakan fungsi smoothstep untuk transisi yang lebih halus
                    smooth_progress = progress * progress * (3 - 2 * progress)
                    alpha = int(180 * smooth_progress)
                
                if alpha > 0:
                    color = (5, 5, 10, alpha)
                    pygame.draw.rect(self.base_vignette, color, (x, y, 1, 1))
    
    def update_vignette_alpha(self):
        """Update alpha vignette berdasarkan intensitas"""
        # Copy base vignette dan adjust alpha
        self.vignette_surface = self.base_vignette.copy()
        
        # Apply intensity scaling
        if self.intensity < 1.0:
            # Buat surface dengan alpha yang disesuaikan
            temp_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            temp_surface.fill((255, 255, 255, int(255 * self.intensity)))
            self.vignette_surface.blit(temp_surface, (0, 0), special_flags=pygame.BLEND_MULT)
            
    def set_intensity(self, intensity):
        """Atur intensitas efek vignette (0.0 - 1.0)"""
        new_intensity = max(0.0, min(1.0, intensity))
        
        # Hanya update jika perubahan signifikan
        if abs(new_intensity - self.intensity) > 0.05:
            self.intensity = new_intensity
            self.update_vignette_alpha()
            
    def activate(self):
        """Aktifkan efek vignette"""
        self.active = True
        
    def deactivate(self):
        """Nonaktifkan efek vignette"""
        self.active = False
        
    def update(self):
        """Update efek vignette dengan animasi halus (optimized)"""
        if not self.active:
            return
            
        # Update waktu untuk animasi (lebih lambat untuk mengurangi beban)
        self.time += 0.01
        
        # Animasi pulse halus pada intensitas (hanya setiap beberapa frame)
        if int(self.time * 60) % 3 == 0:  # Update setiap 3 frame
            pulse_factor = (math.sin(self.time) + 1) / 2  # 0 to 1
            target_intensity = self.intensity * (0.8 + 0.2 * pulse_factor)
            
            # Hanya update jika perubahan cukup signifikan
            current_alpha = int(120 * target_intensity)
            if abs(current_alpha - self.last_alpha) > self.update_threshold:
                self.last_alpha = current_alpha
                # Update intensity tanpa regenerasi base
                old_intensity = self.intensity
                self.intensity = target_intensity
                self.update_vignette_alpha()
                self.intensity = old_intensity
            
    def draw(self, screen):
        """Gambar efek vignette"""
        if not self.active:
            return
            
        # Gambar vignette ke layar
        screen.blit(self.vignette_surface, (0, 0))
            
    def create_horror_atmosphere(self, zombie_count=0):
        """Buat atmosfer horor berdasarkan jumlah zombie"""
        if zombie_count > 0:
            # Semakin banyak zombie, semakin intens vignette
            base_intensity = 0.3
            zombie_intensity = min(0.7, zombie_count * 0.1)
            self.set_intensity(base_intensity + zombie_intensity)
            self.activate()
        else:
            # Kurangi intensitas jika tidak ada zombie
            self.set_intensity(0.1)
            
    def reset(self):
        """Reset efek vignette"""
        self.intensity = 0.3
        self.time = 0
        self.max_alpha = int(120 * self.intensity)
        self.create_vignette()
        self.active = True