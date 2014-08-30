def diffract(hex_encoding):
    return [int(band, 16) for band in (hex_encoding[i:i+2] for i in (0, 2, 4))]

def undiffract(rgb):
    return "".join(hex(int(band))[2:].zfill(2) for band in rgb)
    
