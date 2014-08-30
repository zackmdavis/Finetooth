def diffract(hex_encoding):
    return [int(band, 16) for band in (hex_encoding[i:i+2] for i in (0, 2, 4))]

def undiffract(rgb):
    return "".join(hex(int(band))[2:].zfill(2) for band in rgb)
    
def interpolate(rgb1, rgb2, weighting):
    return list(map(lambda c1, c2: c1 + weighting *(c2 - c1), rgb1, rgb2))

def interpolate_stop(color_stops, x):
    stops = sorted(color_stops.keys())
    closest_above = min(stop for stop in stops if (stop - x) > 0)
    closest_below = max(stop for stop in stops if (stop - x) < 0)
    # TODO: finish
