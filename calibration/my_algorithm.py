import visualization
from calibration import tuning
from calibration.evolutionary.individual import Individual


def tune(tuning_parameter_list, comparison_data, metric):
    individual = Individual(-1, tuning_parameter_list)
    start_values = individual.average_value_list()
    individual.set_list(start_values)
    individual.run()
    errors = individual.errors(comparison_data)
    errors.sort(key=lambda x: x[1])
    print(errors)
    #visualization.draw_grouped_modal_split(comparison_data.get_grouped_modal_split(["gender"]), "datoe")
    visualization.draw_grouped_modal_split(comparison_data.get_grouped_modal_split(), "Datasaurier")

    #visualization.draw_grouped_modal_split(individual.data.get_grouped_modal_split(["gender"]), "aetoa")
    visualization.draw_grouped_modal_split(individual.data.get_grouped_modal_split(), "Dinsoaurier")
    p_name = errors[0][0]
    individual = tuning.tune(individual, comparison_data, individual[p_name], epsilon=0.01)

    #visualization.draw_grouped_modal_split(individual.data.get_grouped_modal_split(["gender"]), "aetoa")
    visualization.draw_grouped_modal_split(individual.data.get_grouped_modal_split(), "Improvosaurier")

    p_name = errors[1][0]
    individual = tuning.tune(individual, comparison_data, individual[p_name], epsilon=0.01)

    #visualization.draw_grouped_modal_split(individual.data.get_grouped_modal_split(["gender"]), "aetoa")
    visualization.draw_grouped_modal_split(individual.data.get_grouped_modal_split(), "Improvosaurier")