import unittest
from pathlib import Path

from configurations import configloader
from configurations.limits import Limit, ModeLimitSimple


class MyTestCase(unittest.TestCase):

    #TODO test properly in this
    def nontest_something(self):
        mc_c = configloader.ModeChoiceConfig(Path("resources/example_config_load/configs/mode_choice_main_parameters.txt"))
        limiter = Limit(mc_c)
        print(limiter.limits)
        self.assertEqual(len(limiter.limits), 228)
    #TODO test properly in this too
    def nontest_limit1(self):
        mc_c = configloader.ModeChoiceConfig(Path("resources/example_config_load/configs/mode_choice_main_parameters.txt"))
        limiter = ModeLimitSimple(mc_c)
        print(limiter.limits)
        self.assertEqual(len(limiter.limits), 228)

if __name__ == '__main__':
    unittest.main()
