import re
from pathlib import Path

from configurations import SPECS


def search_regex(parameter_name, text):
    regex = "\W" + parameter_name + "\W"
    if re.search(regex, text) is None:
        return True
    return False

def rename_helper_method(config, parameter_list, remove=False):
    if remove:
        for p in parameter_list:
            del config.parameters[p]
    else:
        print(f"{config.name} missing {len(parameter_list)} Parameters.")
        print(parameter_list)

def check_in_modes(config, remove_invalid=False):
    gen_files = SPECS.CWD + "config/choice-models/"
    mode_path = Path(gen_files + "mode_choice_mixed_logit.gen")
    time_sens_path = Path(gen_files + "mode_choice_mixed_logit_time_sensitivity.gen")
    mode_pref_path = Path(gen_files + "mode_choice_mixed_logit_mode_preference.gen")

    with open(mode_path, "r") as file, open(time_sens_path, "r") as file2, open(mode_pref_path, "r") as file3:
        text1 = file.read()
        text2 = file2.read()
        text3 = file3.read()
    parameters_not_in_gen = []
    for p in config.parameters:
        if all([search_regex(p, text1), search_regex(p, text2), search_regex(p, text3)]):
            parameters_not_in_gen.append(p)

    rename_helper_method(config, parameters_not_in_gen, remove_invalid)




def check_in_dest(config, remove_invalid=False):
    gen_files = SPECS.CWD + "config/choice-models/"
    dest_path = Path(gen_files + "destination-choice.gen")
    with open(dest_path, "r") as file:
        text = file.read()
    parameters_not_in_gen = []
    for p in config.parameters:
        if search_regex(p, text):
            parameters_not_in_gen.append(p)

    rename_helper_method(config, parameters_not_in_gen, remove_invalid)


def check_config(config, remove_invalid_parameters=False):
    if config.name.__contains__("mode_choice_main"):
        check_in_modes(config, remove_invalid_parameters)
    else:
        check_in_dest(config, remove_invalid_parameters)


def check_yaml(yaml, remove_invalid_parameters=False):
    for config in yaml.configs:
        check_config(config, remove_invalid_parameters)


