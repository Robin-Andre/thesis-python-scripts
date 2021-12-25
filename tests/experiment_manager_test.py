import unittest

import experiment_manager


class MyTestCase(unittest.TestCase):

    def test_something(self):
        #print(experiment_manager.get_experiments())  # add assertion here
        #experiment_manager.find_failed_data("neural_network_random_data")
        #experiment_manager.find_failed_data("broken_sets")
        temp = experiment_manager.find_failed_data("neural_network_only_change_main_params")
        #print(temp)
        print(f"Amount of failures: {len(temp)}")
        all_keys = ['asc_car_d_mu', 'asc_car_d_sig', 'asc_car_p_mu', 'asc_car_p_sig', 'asc_put_mu', 'asc_put_sig',
                    'asc_ped_mu', 'asc_ped_sig', 'asc_bike_mu', 'asc_bike_sig', 'b_tt_car_p_mu', 'b_tt_car_p_sig',
                    'b_tt_car_d_mu', 'b_tt_car_d_sig', 'b_tt_put_mu', 'b_tt_put_sig', 'b_tt_bike_mu', 'b_tt_bike_sig',
                    'b_tt_ped', 'b_cost', 'b_cost_put', 'b_u_put', 'b_logsum_acc_put', 'b_park_car_d', 'b_mode_bef_put',
                    'b_mode_bef_ped', 'b_mode_bef_bike', 'b_home_car_p', 'b_home_put']

        lol = experiment_manager.get_configs_from_failures(temp)
        for key in all_keys:
            seq = [x.entries[key] for x in lol]

            print(f"Bounds for parameter {key}: {min(seq)} -> {max(seq)}")
        #print(lol)

if __name__ == '__main__':
    unittest.main()
