import unittest

import experiment_manager


class MyTestCase(unittest.TestCase):

    def test_something(self):
        #print(experiment_manager.get_experiments())  # add assertion here
        #experiment_manager.find_failed_data("neural_network_random_data")
        #experiment_manager.find_failed_data("broken_sets")
        temp = experiment_manager.find_failed_data("neural_network_dest_data")
        #print(temp)
        print(f"Amount of failures: {len(temp)}")
        all_keys = ['asc_car_d_mu', 'asc_car_d_sig', 'asc_car_p_mu', 'asc_car_p_sig', 'asc_put_mu', 'asc_put_sig',
                    'asc_ped_mu', 'asc_ped_sig', 'asc_bike_mu', 'asc_bike_sig', 'b_tt_car_p_mu', 'b_tt_car_p_sig',
                    'b_tt_car_d_mu', 'b_tt_car_d_sig', 'b_tt_put_mu', 'b_tt_put_sig', 'b_tt_bike_mu', 'b_tt_bike_sig',
                    'b_tt_ped', 'b_cost', 'b_cost_put', 'b_u_put', 'b_logsum_acc_put', 'b_park_car_d', 'b_mode_bef_put',
                    'b_mode_bef_ped', 'b_mode_bef_bike', 'b_home_car_p', 'b_home_put']

        lol = experiment_manager.get_configs_from_failures(temp)
        dest_configs = experiment_manager.get_dest_configs_from_failures(temp)
        all_keys = dest_configs[0].entries.keys()
        print(all_keys)
        for key in all_keys:
            seq = [x.entries[key] for x in dest_configs]

            print(f"Bounds for parameter {key}: {min(seq)} -> {max(seq)}")
        #print(lol)

    def test_locate_broken_data(self):
        expected_result = [('C:\\Users\\Admin\\Desktop\\master-thesis\\neural_network_data\\neural_network_random_data\\iteration60', 'iteration60'), ('C:\\Users\\Admin\\Desktop\\master-thesis\\neural_network_data\\neural_network_random_data\\iteration61', 'iteration61'), ('C:\\Users\\Admin\\Desktop\\master-thesis\\neural_network_data\\neural_network_random_data\\iteration63', 'iteration63'), ('C:\\Users\\Admin\\Desktop\\master-thesis\\neural_network_data\\neural_network_random_data\\iteration66', 'iteration66')]

        self.assertEqual([(str(x), x.name) for x in experiment_manager.find_failed_data("neural_network_random_data")], expected_result)

    def test_move_broken_data(self):
        print(experiment_manager.get_experiments())
        experiment_manager.move_data_to_failure("neural_network_random_data")

    def test_verify_all_clean(self):
        experiment_manager.test_cleanliness("neural_network_random_data")

if __name__ == '__main__':
    unittest.main()
