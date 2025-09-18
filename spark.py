# File untuk efek percikan darah
# File ini membuat efek visual saat zombie terkena serangan

import pygame, math  # Library untuk game dan perhitungan matematika

class Spark:
    """Kelas Spark - Cetakan untuk membuat percikan darah
    
    Spark adalah efek visual kecil yang muncul saat zombie terkena serangan.
    Setiap spark punya posisi, arah, kecepatan, dan warna sendiri.
    """
    def __init__(self, loc, angle, speed, color, scale=1, direction=1):
        """Membuat percikan darah baru
        
        Parameter:
        - loc: Posisi awal percikan [x, y]
        - angle: Arah terbang percikan (dalam radian)
        - speed: Seberapa cepat percikan bergerak
        - color: Warna percikan (biasanya merah untuk darah)
        - scale: Ukuran percikan (1 = normal)
        - direction: Arah umum (1 = kanan, -1 = kiri)
        """
        self.loc = loc      # Posisi percikan [x, y]
        # Tentukan arah berdasarkan direction
        self.angle = angle if direction == 1 else math.pi - angle
        self.speed = speed  # Kecepatan percikan
        self.scale = scale  # Ukuran percikan
        self.color = color  # Warna percikan
        self.alive = True   # Apakah percikan masih hidup (terlihat)



    def calculate_movement(self, dt):
        """Menghitung pergerakan percikan
        
        Fungsi ini menghitung seberapa jauh percikan bergerak
        berdasarkan arah dan kecepatannya.
        """
        return [math.cos(self.angle) * self.speed * dt, math.sin(self.angle) * self.speed * dt]

    def velocity_adjust(self, friction, force, terminal_velocity, dt):
        """Menyesuaikan kecepatan dengan gravitasi dan gesekan
        
        Fungsi ini membuat percikan bergerak lebih realistis dengan:
        - Gravitasi yang menarik ke bawah
        - Gesekan yang memperlambat gerakan horizontal
        """
        movement = self.calculate_movement(dt)  # Hitung gerakan dasar
        # Tambahkan efek gravitasi (tarikan ke bawah)
        movement[1] = min(terminal_velocity, movement[1] + force * dt)
        movement[0] *= friction  # Kurangi kecepatan horizontal karena gesekan
        # Perbarui arah berdasarkan gerakan baru
        self.angle = math.atan2(movement[1], movement[0])

    def move(self, dt):
        """Menggerakkan percikan setiap frame
        
        Fungsi ini membuat percikan bergerak dengan efek fisika realistis
        dan menghilang secara bertahap.
        """
        movement = self.calculate_movement(dt)  # Hitung pergerakan
        self.loc[0] += movement[0]  # Gerakkan secara horizontal
        self.loc[1] += movement[1]  # Gerakkan secara vertikal

        # Tambahkan efek fisika untuk gerakan yang natural
        self.velocity_adjust(0.98, 0.15, 6, dt)  # gesekan, gravitasi, kecepatan maksimal
        
        # Kurangi kecepatan secara bertahap (percikan melemah)
        self.speed -= 0.05

        # Matikan percikan jika sudah terlalu lambat
        if self.speed <= 0:
            self.alive = False

    def draw(self, surf, offset=[0, 0]):
        """Menggambar percikan di layar
        
        Fungsi ini menggambar percikan sebagai bentuk seperti tetesan
        yang menunjuk ke arah gerakan percikan.
        """
        if self.alive:  # Hanya gambar jika percikan masih hidup
            # Hitung titik-titik untuk membentuk percikan seperti tetesan
            points = [
                # Ujung depan percikan (menunjuk arah gerakan)
                [self.loc[0] + math.cos(self.angle) * self.speed * self.scale, 
                 self.loc[1] + math.sin(self.angle) * self.speed * self.scale],
                # Sisi atas percikan
                [self.loc[0] + math.cos(self.angle + math.pi / 2) * self.speed * self.scale * 0.3, 
                 self.loc[1] + math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3],
                # Ujung belakang percikan (ekor)
                [self.loc[0] - math.cos(self.angle) * self.speed * self.scale * 3.5, 
                 self.loc[1] - math.sin(self.angle) * self.speed * self.scale * 3.5],
                # Sisi bawah percikan
                [self.loc[0] + math.cos(self.angle - math.pi / 2) * self.speed * self.scale * 0.3, 
                 self.loc[1] - math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3],
            ]
            # Gambar percikan sebagai polygon dengan warna yang ditentukan
            pygame.draw.polygon(surf, self.color, points)
