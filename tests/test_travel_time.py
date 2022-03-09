import unittest

import pandas

from metrics.data import Data


class MyTestCase(unittest.TestCase):
    def test_subtraction_from_self_is_zero(self):
        data = Data()
        data.load("resources/example_config_load/results/")
        travel_time = data.travel_time
        expected = travel_time.get_data_frame()
        test = travel_time - travel_time
        self.assertTrue(all(test.get_data_frame()["count"]) == 0)
        pandas.testing.assert_frame_equal(expected, travel_time.get_data_frame())


    @unittest.skip("Visual test/Graphic analysis")
    def test_draw(self):
        data = Data()
        data.load("resources/workday_individual/results/")
        data.travel_time.draw()

    @unittest.skip("Visual test/Graphic analysis")
    def test_draw_too_much_detail(self):
        data = Data()
        data.load("resources/even_more_detailed_individual/results/")
        data.travel_time.draw(reference=data.travel_time)

    def test_pdf(self):
        data = Data()
        data.load("resources/even_more_detailed_individual/results/")
        print(data.travel_time.pdf(0))
        print(data.travel_time.cdf(-1))

    def test_subtraction(self):
        data = Data()
        data.load("resources/workday_individual/results/")
        x = data.travel_time
        y = x.sub_all(x)
        z = x.sub_none(x)
        w = x - x
        self.assertTrue(not y.any(axis=None))
        self.assertFalse(y.any(axis=None))
        self.assertFalse(z.any(axis=None))
        self.assertFalse(w.any(axis=None))
        self.assertEqual(len(y.columns), 1)
        self.assertEqual(len(z.columns), 1)
        self.assertEqual(len(w.columns), 1)

    def test_unequal_subtraction(self):
        pass

if __name__ == '__main__':
    unittest.main()
