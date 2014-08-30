from django.test import TestCase

from core.colorize import diffract, undiffract

class ColorTest(TestCase):

    def test_can_diffract(self):
        self.assertEqual([127, 2, 255], diffract("7f02ff"))

    def test_can_undiffract(self):
        self.assertEqual("7f02ff", undiffract([127, 2, 255]))

