import unittest

import experiment_manager


class MyTestCase(unittest.TestCase):

    def test_something(self):
        print(experiment_manager.get_experiments())  # add assertion here
        experiment_manager.find_failed_data("neural_network_random_data")
        experiment_manager.find_failed_data("broken_sets")

if __name__ == '__main__':
    unittest.main()
