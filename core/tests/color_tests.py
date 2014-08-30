from django.test import TestCase
from unittest import skip

from core.colorize import diffract, undiffract, interpolate, interpolate_stop

class ColorTest(TestCase):

    def test_can_diffract(self):
        self.assertEqual([127, 2, 255], diffract("7f02ff"))

    def test_can_undiffract(self):
        self.assertEqual("7f02ff", undiffract([127, 2, 255]))

    def test_can_interpolate(self):
        self.assertEqual([127, 127, 127],
                         interpolate([0, 0, 0], [254, 254, 254], 0.5))

    @skip("not done yet")
    def test_can_interpolate_stop(self):
        self.assertEqual("7f7f7f",
                         interpolate_stop({1: "000000", 3: "fefefe"}, 2))
