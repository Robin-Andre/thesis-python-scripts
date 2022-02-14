import copy
import math
import unittest

from matplotlib import pyplot as plt

import visualization
from calibration.evolutionary.individual import Individual
import mobitopp_execution as simulation
from calibration.evolutionary.population import Population
from configurations import SPECS
from configurations.parameter import Parameter


class MyTestCase(unittest.TestCase):

    def test_load(self):
        x = Individual(0, [])
        try:
            x.load("resources/test_population/individual_0")
        except FileNotFoundError:
            self.fail("Test did not load the individual!")

        self.assertAlmostEqual(x["asc_car_d_mu"].value, 5.352656054767767)
        self.assertAlmostEqual(x["asc_put_sig"].value, -1.5723)

    def test_observation(self):
        x = Individual(21, [])
        y = Individual(13, [])
        z = Individual("number", [])
        x.load("resources/test_population/individual_0")
        y.load("resources/compare_individual")
        z.load("resources/test_population/individual_1")
        parameter = x["asc_car_d_mu"]
        print(parameter)
        print(parameter.observe(x, y.data))
        print(parameter.observe_detailed(x, z, y.data))




    def test_copy(self):
        x = Individual(21, [])
        x["asc_car_d_mu"].set(9)
        y = x.copy()
        self.assertEqual(y["asc_car_d_mu"].value, 9)
        y["asc_car_d_mu"].set(2)
        self.assertEqual(x["asc_car_d_mu"].value, 9)


    def test_change_value(self):
        x = Individual(9001, [])
        x["asc_car_d_mu"].set(34)
        self.assertEqual(x["asc_car_d_mu"].value, 34)

    def test_rand_remove(self):
        vals = [(-50, -0.1055588731090511), (-49, -0.10105606281604453), (-48, -0.09659328044872587),
                (-47, -0.09063301164965534), (-46, -0.08573078137780653), (-45, -0.0786214593470943),
                (-44, -0.07190629643369892), (-43, -0.0639742150109478), (-42, -0.05560301312839265),
                (-41, -0.047302338964356386), (-40, -0.0387642249663962), (-39, -0.029654135323851055),
                (-38, -0.021000110074182093), (-37, -0.012062072454837341), (-36, -0.0023845289375048206),
                (-35, 0.009279992778086998), (-34, 0.021488983428429476), (-33, 0.03238680434018362),
                (-32, 0.04419208524382906), (-31, 0.058342618330341434), (-30, 0.07333362655709419),
                (-29, 0.09080529599444007), (-28, 0.10945539857127087), (-27, 0.12953135640203667),
                (-26, 0.15165422857932015), (-25, 0.17559332308262166), (-24, 0.20055412637309789),
                (-23, 0.2269145705046684), (-22, 0.2547639886358702), (-21, 0.28320639207498904),
                (-20, 0.3120378699151829), (-19, 0.34060209736424624), (-18, 0.3713509248765564),
                (-17, 0.40179253456234754), (-16, 0.43333440079657615), (-15, 0.46526448005159415),
                (-14, 0.4983041279443816), (-13, 0.5316456804213257), (-12, 0.5674272882938287),
                (-11, 0.6009209354992449), (-10, 0.6348026366892188), (-9, 0.6703529804172932),
                (-8, 0.7048766505028343), (-7, 0.7358209083796837), (-6, 0.7647411154304709), (-5, 0.7900792727914896),
                (-4, 0.8094454083670605), (-3, 0.8255203561749637), (-2, 0.8381373354827308), (-1, 0.8471489029792936)]
        xva = [x[0] for x in vals]
        yva = [x[1] for x in vals]
        plt.plot(xva, yva)
        plt.show()


if __name__ == '__main__':
    unittest.main()
