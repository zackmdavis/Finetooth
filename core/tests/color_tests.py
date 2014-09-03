from django.test import TestCase

from core.colorize import (
    diffract, undiffract, interpolate, interpolate_stop, populate_stops
)

class ColorTest(TestCase):

    def test_can_diffract(self):
        self.assertEqual([127, 2, 255], diffract("7f02ff"))

    def test_can_undiffract(self):
        self.assertEqual("7f02ff", undiffract([127, 2, 255]))

    def test_can_interpolate(self):
        self.assertEqual([127, 127, 127],
                         interpolate([0, 0, 0], [254, 254, 254], 0.5))

    def test_can_interpolate_stop(self):
        self.assertEqual("7f7f7f",
                         interpolate_stop({1: "000000", 3: "fefefe"}, 2))

class StyleTest(TestCase):

    def test_can_populate_stops(self):
        self.assertEqual(
            {-4: 'ff0000', -3: 'df001f', -2: 'bf003f', -1: '9f005f',
             0: '7f007f', 1: '5f009f', 2: '3f00bf', 3: '1f00df', 4: '0000ff'},
            populate_stops({-4: "ff0000", 4: "0000ff"})
        )
