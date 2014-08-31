def diffract(hex_encoding):
    return [int(band, 16) for band in (hex_encoding[i:i+2] for i in (0, 2, 4))]

def undiffract(rgb):
    return "".join(hex(int(band))[2:].zfill(2) for band in rgb)

def interpolate(rgb1, rgb2, weighting):
    return list(map(lambda c1, c2: c1 + weighting*(c2 - c1), rgb1, rgb2))

def interpolate_stop(color_stops, x):
    stops = sorted(color_stops.keys())
    closest_above = min(stop for stop in stops if (stop - x) > 0)
    closest_below = max(stop for stop in stops if (stop - x) < 0)
    diffracted_above, diffracted_below = [
        diffract(color_stops[s]) for s in (closest_above, closest_below)
    ]
    weighting = (x - closest_below) / (closest_above - closest_below)
    return undiffract(
        interpolate(diffracted_below, diffracted_above, weighting)
    )

def populate_stops(color_stops):
    full_stops = color_stops.copy()
    stops = color_stops.keys()
    heroism = max(stops)
    villainy = min(stops)
    for moral_quality in range(villainy, heroism + 1):
        if moral_quality not in color_stops:
            full_stops[moral_quality] = interpolate_stop(
                color_stops, moral_quality
            )
    return full_stops

def style_block(value, color):
    return "\n".join(["[data-value=\"{}\"] {{".format(value),
                      "    color: #{};".format(color),
                      "}\n"])

def stylesheet(low_score, low_color, high_score, high_color):
    color_stops = populate_stops({low_score: low_color, high_score: high_color})
    return "\n".join(style_block(value, color)
                     for value, color in color_stops.items())
