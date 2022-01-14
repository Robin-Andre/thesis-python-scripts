import unittest

from configurations.parameter import Mode, AgeGroup


class MyTestCase(unittest.TestCase):
    def test_something(self):
        print(Mode.TAXI)
        print(AgeGroup.FROM_0_TO_17.value)


if __name__ == '__main__':
    unittest.main()
