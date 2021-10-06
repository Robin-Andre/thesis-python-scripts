# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import random
import subprocess
import configloader
import yamlloader
import evaluation


def load_config():
    print(NotImplemented)


def interpret_yaml():
    NotImplemented


def run_mobitopp(directory):
    process = subprocess.Popen(["./gradlew",
                                "runRastatt_100p_ShortTermModule"],
                               cwd=directory,
                               stdout=subprocess.PIPE)

    stdout = process.communicate()[0]
    print('STDOUT:{}'.format(stdout))
    process.wait()


def any_constructor(loader, tag_suffix, node):
    if isinstance(node, yaml.MappingNode):
        return loader.construct_mapping(node)
    if isinstance(node, yaml.SequenceNode):
        return loader.construct_sequence(node)
    return loader.construct_scalar(node)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    evaluation.evaluate("/home/paincrash/Desktop/master-thesis/mobitopp-example-rastatt/output/results/simulation/demandsimulationResult.csv")
    exit(0)
    cwd = "/home/paincrash/Desktop/master-thesis/mobitopp-example-rastatt/"
    yaml_file = "config/rastatt/short-term-module-100p.yaml"
    run_mobitopp(cwd)
    exit(0)
    yaml = yamlloader.YAML(cwd + yaml_file)

    configs = []
    for key in yaml.data['destinationChoice']:
        print(yaml.data['destinationChoice'][key])
        co = configloader.Config(cwd, yaml.data['destinationChoice'][key])
        configs.append(co)
        co.set_path("calibration/" + co.name)
        yaml.data['destinationChoice'][key] = co.path
    for i in configs:
        if i.name != "destination_choice_utility_calculation_parameters.txt":
            break
        i.set_path("calibration/" + i.name)
        for item in i.get_parameter_list():
            val = 20 * random.random()
            print(item + " " + str(val))
            i.set_parameter(item, val)
        i.print()
        i.write()
    yaml.data['seed'] = 1
    yaml.data['fractionOfPopulation'] = 0.01
    yaml.data['resultFolder'] = "output/results/calibration/experiment_shuffled_configs/seed_1"
    yaml.write()
    run_mobitopp(cwd)
    yaml.reset()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
