import random
import yamlloader


def main():
    cwd = "/home/paincrash/Desktop/master-thesis/mobitopp-example-rastatt/"
    yaml_file = "config/rastatt/short-term-module-100p.yaml"
    yaml = yamlloader.YAML(cwd, yaml_file)
    configs = yaml.find_configs(cwd)
    print(configs)
    temp_config = configs[0]
    for item in temp_config.get_parameter_list():
        print(item + ": " + str(temp_config.get_parameter(item)))
        temp_config.override_parameter(item, round(temp_config.get_parameter(item)))
    temp_config.write()
    exit()
    configs = []
    for i in configs:
        if i.name != "destination_choice_utility_calculation_parameters.txt":
            break
        i.set_path("calibration/" + i.name)
        for item in i.get_parameter_list():
            val = 200 * random.random()
            print(item + " " + str(val))
            i.set_parameter(item, val)
        i.print()
        i.write()
    yaml.data['seed'] = 1
    yaml.data['fractionOfPopulation'] = 0.01
    yaml.data['resultFolder'] = "output/results/calibration/experiment_shuffled_configs/seed_1"
    yaml.write()
    yaml.reset()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
