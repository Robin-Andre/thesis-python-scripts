import time
import unittest
import numpy as np
import pandas

import evaluation
import metric

import visualization as plot
import yamlloader
import mobitopp_execution as simulation


class MyTestCase(unittest.TestCase):

    def test_temporary(self):
        yaml, data = simulation.load("resources/example_config_load/")
        config_dest = yaml.configs[4]
        config_mode = yaml.configs[5]
        dest_items = config_dest.entries.keys()
        print(dest_items)
        print(config_mode.entries.keys())

if __name__ == '__main__':
    unittest.main()
