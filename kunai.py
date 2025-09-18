# File untuk senjata kunai ninja
# Kunai adalah pisau lempar yang digunakan ninja untuk menyerang zombie

class Kunai:
    """Kelas Kunai - Cetakan untuk membuat senjata ninja
    
    Kunai adalah pisau lempar ninja yang bisa terbang dan mengenai zombie.
    Setiap kunai punya posisi, kecepatan, dan gambar sendiri.
    """
    
    def __init__(self, screen, image, x, y, speed):
        """Membuat kunai baru
        
        Parameter:
        - screen: Layar game
        - image: Gambar kunai
        - x, y: Posisi awal kunai
        - speed: Seberapa cepat kunai terbang
        """
        self.image = image    # Gambar kunai
        self.x = x           # Posisi kiri-kanan kunai
        self.y = y           # Posisi atas-bawah kunai
        self.speed = speed   # Seberapa cepat kunai terbang
        self.screen = screen # Layar game
        self.active = True   # Apakah kunai masih aktif (belum hilang)

    def get_x(self):
        """Mendapatkan posisi kiri-kanan kunai
        
        Fungsi ini memberitahu di mana kunai berada secara horizontal.
        """
        return self.x
    
    def get_y(self):
        """Mendapatkan posisi atas-bawah kunai
        
        Fungsi ini memberitahu di mana kunai berada secara vertikal.
        """
        return self.y
    
    def get_current_sprite(self):
        """Mendapatkan gambar kunai
        
        Fungsi ini memberikan gambar kunai yang akan ditampilkan.
        """
        return self.image

    def update(self):
        """Menggerakkan kunai setiap frame
        
        Fungsi ini membuat kunai terbang ke kanan dan menghilang
        jika sudah keluar dari layar.
        """
        self.x += self.speed  # Gerakkan kunai ke arah kanan
        
        # Cek apakah kunai sudah keluar dari layar
        if self.x > self.screen.get_width() or self.x < -50:
            self.active = False  # Matikan kunai karena sudah hilang
    
    def draw(self, screen):
        """Menggambar kunai di layar
        
        Fungsi ini menampilkan gambar kunai di posisi yang tepat.
        """
        screen.blit(self.image, (self.x, self.y))  # Tempel gambar kunai
