# File untuk efek daun beterbangan
# File ini mengatur efek daun yang jatuh dari pohon dan bergerak dengan angin

import pygame
import random
import math

class Leaf:
    """Kelas untuk satu daun yang beterbangan"""

    def __init__(self, x, y, screen_width, screen_height):
        """Inisialisasi daun baru"""
        self.x = x
        self.y = y
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Properti gerakan daun
        self.fall_speed = random.uniform(0.5, 2.0)  # Kecepatan jatuh
        self.wind_speed = random.uniform(-1.0, 1.0)  # Kecepatan angin horizontal
        self.swing_amplitude = random.uniform(10, 30)  # Amplitudo ayunan
        self.swing_frequency = random.uniform(0.02, 0.05)  # Frekuensi ayunan
        self.time = random.uniform(0, 2 * math.pi)  # Waktu untuk ayunan

        # Properti visual daun
        self.size = random.randint(3, 8)  # Ukuran daun
        self.rotation = random.uniform(0, 360)  # Rotasi awal
        self.rotation_speed = random.uniform(-2, 2)  # Kecepatan rotasi

        # Warna daun (variasi musim gugur)
        colors = [
            (139, 69, 19),   # Coklat
            (255, 140, 0),   # Orange gelap
            (255, 165, 0),   # Orange
            (218, 165, 32),  # Emas
            (160, 82, 45),   # Coklat sedang
            (205, 133, 63),  # Peru
            (222, 184, 135), # Burlywood
        ]
        self.color = random.choice(colors)

        # Transparansi
        self.alpha = random.randint(180, 255)

    def update(self):
        """Update posisi dan rotasi daun"""
        # Update waktu untuk ayunan
        self.time += self.swing_frequency

        # Gerakan jatuh dengan ayunan
        self.y += self.fall_speed
        self.x += self.wind_speed + math.sin(self.time) * self.swing_amplitude * 0.1

        # Rotasi daun
        self.rotation += self.rotation_speed
        if self.rotation > 360:
            self.rotation -= 360
        elif self.rotation < 0:
            self.rotation += 360

        # Reset daun jika keluar dari layar
        if self.y > self.screen_height + 50:
            self.y = -50
            self.x = random.randint(-50, self.screen_width + 50)

        if self.x < -100:
            self.x = self.screen_width + 50
        elif self.x > self.screen_width + 100:
            self.x = -50

    def draw(self, screen):
        """Gambar daun di layar"""
        # Buat surface untuk daun dengan transparansi
        leaf_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)

        # Gambar bentuk daun sederhana (oval)
        pygame.draw.ellipse(leaf_surface, (*self.color, self.alpha),
                          (0, 0, self.size * 2, self.size))

        # Rotasi daun
        rotated_leaf = pygame.transform.rotate(leaf_surface, self.rotation)

        # Posisi untuk menggambar (tengah rotasi)
        rect = rotated_leaf.get_rect(center=(self.x, self.y))

        # Gambar daun ke layar
        screen.blit(rotated_leaf, rect)

class LeafEffect:
    """Kelas untuk mengatur efek daun beterbangan"""

    def __init__(self, screen_width, screen_height):
        """Inisialisasi efek daun"""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.leaves = []
        self.max_leaves = 30  # Maksimal daun di layar
        self.spawn_rate = 0.3  # Kemungkinan spawn daun baru per frame

        # Buat beberapa daun awal
        for _ in range(15):
            x = random.randint(0, screen_width)
            y = random.randint(-screen_height, 0)
            self.leaves.append(Leaf(x, y, screen_width, screen_height))

    def add_leaf_from_tree(self, tree_x, tree_y):
        """Tambahkan daun yang jatuh dari pohon tertentu"""
        if len(self.leaves) < self.max_leaves:
            # Tambahkan sedikit variasi posisi dari pohon
            x = tree_x + random.randint(-20, 20)
            y = tree_y + random.randint(-10, 10)
            self.leaves.append(Leaf(x, y, self.screen_width, self.screen_height))

    def update(self, tree_positions=None):
        """Update semua daun dan spawn daun baru dari pohon"""
        # Update semua daun yang ada
        for leaf in self.leaves:
            leaf.update()

        # Spawn daun baru dari pohon jika ada
        if tree_positions and random.random() < self.spawn_rate:
            for tree_pos in tree_positions:
                if random.random() < 0.1:  # 10% chance per pohon
                    self.add_leaf_from_tree(tree_pos['x'], tree_pos['y'])

        # Spawn daun random dari atas layar
        if len(self.leaves) < self.max_leaves and random.random() < self.spawn_rate * 0.5:
            x = random.randint(-50, self.screen_width + 50)
            y = -50
            self.leaves.append(Leaf(x, y, self.screen_width, self.screen_height))

    def draw(self, screen):
        """Gambar semua daun"""
        for leaf in self.leaves:
            leaf.draw(screen)

    def set_wind_strength(self, strength):
        """Atur kekuatan angin untuk semua daun"""
        for leaf in self.leaves:
            leaf.wind_speed = random.uniform(-strength, strength)
