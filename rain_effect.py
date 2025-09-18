import pygame
import random

class RainDrop:
    """Kelas untuk satu tetes hujan"""
    def __init__(self, x, y, speed, length):
        self.x = x
        self.y = y
        self.speed = speed
        self.length = length
        self.angle = random.uniform(-0.2, 0.2)  # Sedikit miring untuk efek angin

    def update(self, screen_height):
        """Update posisi tetes hujan"""
        self.y += self.speed
        self.x += self.angle * self.speed

        # Reset jika sudah keluar layar
        if self.y > screen_height + 10:
            self.y = -random.randint(10, 50)
            self.x = random.randint(-50, 850)  # Sedikit lebih lebar dari layar

    def draw(self, screen):
        """Gambar tetes hujan"""
        # Warna biru muda untuk hujan
        color = (173, 216, 230, 180)  # Light blue dengan transparansi

        # Gambar garis untuk tetes hujan
        start_pos = (int(self.x), int(self.y))
        end_pos = (int(self.x + self.angle * self.length), int(self.y - self.length))

        # Buat surface dengan alpha untuk transparansi
        rain_surface = pygame.Surface((abs(end_pos[0] - start_pos[0]) + 2, self.length + 2), pygame.SRCALPHA)
        pygame.draw.line(rain_surface, color[:3],
                        (1, self.length + 1),
                        (abs(end_pos[0] - start_pos[0]) + 1, 1), 2)

        screen.blit(rain_surface, (min(start_pos[0], end_pos[0]) - 1, start_pos[1] - self.length - 1))

class RainEffect:
    """Kelas untuk efek hujan lengkap"""
    def __init__(self, screen_width, screen_height, intensity=100):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.intensity = intensity
        self.raindrops = []

        # Buat tetes hujan
        for _ in range(intensity):
            x = random.randint(-50, screen_width + 50)
            y = random.randint(-screen_height, 0)
            speed = random.uniform(8, 15)
            length = random.randint(10, 20)
            self.raindrops.append(RainDrop(x, y, speed, length))

        # Overlay untuk efek gelap
        self.rain_overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        self.rain_overlay.fill((50, 50, 80, 30))  # Warna gelap dengan transparansi

    def update(self):
        """Update semua tetes hujan"""
        for raindrop in self.raindrops:
            raindrop.update(self.screen_height)

    def draw(self, screen):
        """Gambar efek hujan"""
        # Gambar overlay gelap terlebih dahulu
        screen.blit(self.rain_overlay, (0, 0))

        # Gambar semua tetes hujan
        for raindrop in self.raindrops:
            raindrop.draw(screen)

    def set_intensity(self, new_intensity):
        """Ubah intensitas hujan"""
        if new_intensity > len(self.raindrops):
            # Tambah tetes hujan
            for _ in range(new_intensity - len(self.raindrops)):
                x = random.randint(-50, self.screen_width + 50)
                y = random.randint(-self.screen_height, 0)
                speed = random.uniform(8, 15)
                length = random.randint(10, 20)
                self.raindrops.append(RainDrop(x, y, speed, length))
        elif new_intensity < len(self.raindrops):
            # Kurangi tetes hujan
            self.raindrops = self.raindrops[:new_intensity]

        self.intensity = new_intensity
