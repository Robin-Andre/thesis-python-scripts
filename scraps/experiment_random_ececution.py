import random
import visualization as plot
import pandas

import evaluation
import mobitopp_execution as simulation
import yamlloader

def shuffle_config_within_parameters(config):
    lower_bound_array = [16384, 16384, 16384, 16384, 16384, 16384, 16384, 16384, 16384, 16384,
                         16384, 16384, 16384, 16384, 16384, 16384, 16384, 16384, 16384, 16384,
                         16384, 16384, 16384, 4.359375]
    upper_bound_array = [576.0, 576.0, 576.0, 576.0, 576.0, 16384, 16384, 16384, 576.0, 16384,
                         7.265625, 6.890625, 2.109375, 0.703125, 2.109375, 16384, 16384, 16384,
                         36.75, 16384, 16384, 16384, 16384, 0.703125]
    parameter_list = config.get_parameter_list()
    hard_clamp = 10
    for i in range(len(parameter_list)):

        low_clamp = min(lower_bound_array[i], hard_clamp)
        high_clamp = min(upper_bound_array[i], hard_clamp)
        new_param = random.uniform(-low_clamp, high_clamp)
        print(parameter_list[i] + " is within [-" + str(lower_bound_array[i]) + "," + str(upper_bound_array[i]) + "] ==> " + str(new_param))
        config.override_parameter(parameter_list[i], new_param)
    config.write()


if __name__ == '__main__':
    simulation.restore_experimental_configs()
    cwd = "/home/paincrash/Desktop/master-thesis/mobitopp-example-rastatt/"
    csv_path = cwd + "output/results/calibration/throwaway/demandsimulationResult.csv"
    yaml_file = "config/rastatt/short-term-module-100p.yaml"
    yaml = yamlloader.YAML(cwd, yaml_file)
    yaml.data["fractionOfPopulation"] = 0.05
    yaml.write()
    directory = "/home/paincrash/Desktop/master-thesis/experiment_results_permanent/experiment_random_execution/"
    config_list = yaml.find_configs(cwd)
    for i in range(11):
        for config in config_list:
            if config.name == "destination_choice_utility_calculation_parameters.txt":
                shuffle_config_within_parameters(config)
        #simulation_failed = simulation.run_experiment()
        #print("Simulation has return value: " + str(simulation_failed))
        #evaluation.save_compressed_output("Iteration" + str(i),
        #                                "/home/paincrash/Desktop/master-thesis/mobitopp-example-rastatt/output/results"
        #                                "/calibration/throwaway/demandsimulationResult.csv",
        #                                directory
        #                                ,"")
    yaml.data["fractionOfPopulation"] = 1
    yaml.write()
    simulation.restore_experimental_configs()

    for i in range(10):
        df_cur = pandas.read_csv(directory + "Iteration" + str(i))
        df_cur["identifier"] = "Iteration" + str(i)
        df_cur_modal = pandas.read_csv(directory + "Iteration" + str(i) + "MODAL")
        df_cur_modal["identifier"] = "Iteration" + str(i)
        #title = config.split(".")[0] + " Iteration " + str(i)
        j = i + 1
        df_next = pandas.read_csv(directory + "Iteration" + str(j))
        df_next["identifier"] = "Iteration" + str(j)
        df_next_modal = pandas.read_csv(directory + "Iteration" + str(j) + "MODAL")
        df_next_modal["identifier"] = "Iteration" + str(j)

        plot.draw(pandas.concat([df_cur, df_next]), plot.aggregate_traffic_two_sets)
        plot.draw(pandas.concat([df_cur_modal, df_next_modal]), plot.aggregate_traffic_modal_two_sets)
