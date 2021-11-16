import subprocess


def run_mobitopp(directory, yaml):
    process = subprocess.Popen(["./gradlew",
                                yaml],
                               cwd=directory,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout = process.communicate()[0]
    stderr = process.communicate()[1]
    return_code = process.returncode
    #print(stdout)
    #print('STDOUT:{}'.format(stdout))

    process.wait()
    return return_code


def run():
    default_path = "/home/paincrash/Desktop/master-thesis/mobitopp-example-rastatt/"
    return run_mobitopp(default_path, "runRastatt_100p_ShortTermModule")


def restore_experimental_configs():
    standard_config_path = "/home/paincrash/Desktop/master-thesis/mobitopp-example-rastatt/"
    original_configs = "config/shared/parameters/"
    calibration_configs = "calibration/"
    configs = ["destination_choice_utility_calculation_parameters.txt", "destination_choice_parameters_SHOPPING.txt",
               "destination_choice_parameters_SERVICE.txt", "destination_choice_parameters_LEISURE.txt",
               "destination_choice_parameters_BUSINESS.txt", "mode_choice_main_parameters.txt"]
    for config in configs:
        input_file = open(standard_config_path + original_configs + config, "r")
        text = input_file.read()
        output_file = open(standard_config_path + calibration_configs + config, "w")
        output_file.write(text)
        input_file.close()
        output_file.close()
    return


def run_experiment():
    default_path = "/home/paincrash/Desktop/master-thesis/mobitopp-example-rastatt/"
    return run_mobitopp(default_path, "runRastatt_100p_ShortTermModule")
