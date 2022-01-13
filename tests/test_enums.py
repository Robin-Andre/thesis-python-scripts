import unittest

from configurations.enums.agegroup import AgeGroup
from configurations.enums.mode import Mode



class MyTestCase(unittest.TestCase):
    def test_something(self):
        print(Mode.TAXI)
        print(AgeGroup.FROM_0_TO_17.value)


if __name__ == '__main__':
    unittest.main()
