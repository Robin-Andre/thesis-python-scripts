import unittest
from pathlib import Path

from configurations import configloader
from configurations.limits import Limit, ModeLimitSimple


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.mc_c = configloader.ModeChoiceConfig(Path("resources/example_config_load/configs/mode_choice_main_parameters.txt"))

    def test_base_limit(self):

        limiter = Limit(self.mc_c)
        self.assertEqual(len(limiter.limits), 228)
        for a, b in limiter.limits.values():
            self.assertEqual(a, -100)
            self.assertEqual(b, 100)

    def test_mode_choice_limit(self):

        limiter = ModeLimitSimple(self.mc_c)
        self.assertEqual(len(limiter.limits), 228)
        for key, (a, b) in limiter.limits.items():
            if key.__contains__("sig"):
                self.assertEqual((a, b), (0, 0))


if __name__ == '__main__':
    unittest.main()
