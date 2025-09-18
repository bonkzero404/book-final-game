# -*- coding: utf-8 -*-
# GAME NINJA MELAWAN ZOMBIE
# Ini adalah file utama untuk memulai permainan!
# Dibuat khusus untuk belajar programming dengan cara yang menyenangkan

# Import (mengambil) kode permainan dari file lain
from gameplay import GamePlay

def main():
    """Fungsi utama untuk memulai permainan
    
    Fungsi ini seperti tombol 'START' pada game!
    Ketika kita tekan, permainan akan dimulai.
    """
    # Membuat objek permainan baru (seperti menyiapkan papan permainan)
    game = GamePlay()
    
    # Menjalankan permainan (mulai bermain!)
    game.run()

# Bagian ini akan dijalankan ketika file ini dibuka langsung
# Seperti pintu masuk utama ke dalam permainan
if __name__ == '__main__':
    print("Selamat datang di Game Ninja vs Zombie!")
    print("Game ini dibuat untuk belajar programming")
    print("Mari kita mulai petualangan!")
    main()  # Panggil fungsi main untuk memulai permainan
