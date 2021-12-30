import unittest
from pathlib import Path

from configurations import configloader
from configurations.limits import Limit, ModeLimitSimple


class MyTestCase(unittest.TestCase):

    def test_something(self):
        mc_c = configloader.ModeChoiceConfig(Path("resources/example_config_load/configs/mode_choice_main_parameters.txt"))
        limiter = Limit(mc_c)
        print(limiter.limits)
        self.assertEqual(len(limiter.limits), 228)

    def test_limit1(self):
        mc_c = configloader.ModeChoiceConfig(Path("resources/example_config_load/configs/mode_choice_main_parameters.txt"))
        limiter = ModeLimitSimple(mc_c)
        print(limiter.limits)

if __name__ == '__main__':
    unittest.main()
