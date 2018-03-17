import itertools
from typing import Dict, List, Union


def diffract(hex_encoding: str) -> List[int]:
    return [int(band, 16) for band in (hex_encoding[i:i+2] for i in (0, 2, 4))]

def undiffract(rgb: Union[List[int], List[float]]) -> str:
    return "".join(hex(int(band))[2:].zfill(2) for band in rgb)

def interpolate(rgb1: List[int], rgb2: List[int], weighting: float) -> List[float]:
    return list(map(lambda c1, c2: c1 + weighting*(c2 - c1), rgb1, rgb2))

def interpolate_stop(color_stops: Dict[int, str], x: int) -> str:
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

def populate_stops(color_stops: Dict[int, str]) -> Dict[int, str]:
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


def style_block(data_attribute, style_property, state, color):
    return "\n".join(["[data-{}=\"{}\"] {{".format(data_attribute, state),
                      "    {}: #{};".format(style_property, color),
                      "}\n"])

def value_style_block(value, color):
    return style_block("value", "color", value, color)

def mark_style_block(mark, color):
    return style_block("mark", "background-color", mark, color)


def stylesheet(low_score, low_color, high_score, high_color):
    stops = {0: "000000"}
    if low_score < 0:
        stops.update({low_score: low_color})
    if high_score > 0:
        stops.update({high_score: high_color})
    colors = populate_stops(stops)
    return "\n".join(
        itertools.chain(
            (value_style_block(value, color)
             for value, color in colors.items()),
            (mark_style_block(mark, color)
             for mark, color in ((-1, "FFD6D6"), (1, "D6D6FF")))
        )
    )
