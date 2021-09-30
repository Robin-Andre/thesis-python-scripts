# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import subprocess
import timeit

import configloader
import yaml_loader

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    cwd = "/home/paincrash/Desktop/master-thesis/mobitopp-example-rastatt/"
    yaml = "config/rastatt/short-term-module-100p.yaml"
    # run_mobitopp()
    c_files = configloader.find_relevant_config_files(cwd + yaml)
    config = yaml_loader.YAML(cwd + yaml)
    c_files.remove("config/shared/parameters/ChargingPower.txt")
    co = configloader.Config(cwd + c_files[0])
    #co.print()
    #print(co.get_parameter("b_tt_acc_put"))

    co.set_parameter("b_logsum_acc_cs", 20)
    co.set_parameter("b_logsum_acc_cs", 10)
    co.print()
    co.override_parameter("b_logsum_acc_cs", -900)
    co.print()
    config.set_pop_percentage(0.01)
    #for i in range(1, 11):
    #    config.set_seed(i)
    #    config.set_result_folder("output/results/calibration/experiment_small/seed_" + str(i))
    #    config.activate()
    #    start = timeit.timeit()
    #    run_mobitopp(cwd)
    #    end = timeit.timeit()
    #    print("Run of seed: " + str(i) + " took: " + str(end - start))
    #config.set_pop_percentage(1)
    #for i in range(1, 11):
    #    config.set_seed(i)
    #    config.set_result_folder("output/results/calibration/experiment_full/seed_" + str(i))
    #    config.activate()
    #    start = timeit.timeit()
    #    run_mobitopp(cwd)
    #    end = timeit.timeit()
    #    print("Run of seed: " + str(i) + " took: " + str(end - start))
    #config.set_pop_percentage(0.000025)
    #for i in range(1, 11):
    #    config.set_seed(i)
    #    config.set_result_folder("output/results/calibration/experiment_really_really_small/seed_" + str(i))
    #    config.activate()
    #    start = timeit.timeit()
     #   run_mobitopp(cwd)
    #    end = timeit.timeit()
    #    print("Run of seed: " + str(i) + " took: " + str(end - start))
    # for file in c_files:
    #    params = configloader.read_configuration_file(cwd + file)
        # configloader.write_configuration_file(params)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
