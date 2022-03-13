from calibration.evolutionary.individual import Individual


def tune(tuning_parameter_list, comparison_data):
    individual = Individual(42, tuning_parameter_list)
    individual.make_basic(nullify_exponential_b_tt=True)
    individual.run()
