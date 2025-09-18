# File helper - Fungsi pembantu untuk game
# File ini berisi fungsi-fungsi yang membantu mengatur gambar

import pygame  # Library untuk membuat game

def resize_with_aspect_ratio(image, MAX_WIDTH, MAX_HEIGHT):
    """Mengubah ukuran gambar tanpa membuatnya gepeng
    
    Fungsi ini seperti mengecilkan atau membesarkan foto
    tanpa membuatnya terlihat aneh (tetap proporsional).
    
    Parameter:
    - image: Gambar yang mau diubah ukurannya
    - MAX_WIDTH: Lebar maksimal yang diinginkan
    - MAX_HEIGHT: Tinggi maksimal yang diinginkan
    """
    # Ukur gambar asli
    original_width, original_height = image.get_size()
    # Hitung perbandingan lebar dan tinggi
    aspect_ratio = original_width / original_height

    # Cek apakah gambar terlalu besar
    if original_width > MAX_WIDTH or original_height > MAX_HEIGHT:
        # Tentukan ukuran baru berdasarkan bentuk gambar
        if aspect_ratio > 1:  # Gambar lebih lebar daripada tinggi
            new_width = MAX_WIDTH
            new_height = int(MAX_WIDTH / aspect_ratio)
        else:  # Gambar lebih tinggi daripada lebar
            new_height = MAX_HEIGHT
            new_width = int(MAX_HEIGHT * aspect_ratio)
        # Ubah ukuran gambar dengan halus
        return pygame.transform.smoothscale(image, (new_width, new_height))
    # Gambar sudah pas ukurannya, tidak perlu diubah
    return image
