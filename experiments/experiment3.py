import subprocess
from pathlib import Path
import evaluation
import yamlloader


def run_mobitopp(directory):
    process = subprocess.Popen(["./gradlew",
                                "runRastatt_100p_ShortTermModule"],
                               cwd=directory,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout = process.communicate()[1]
    return_code = process.returncode
    print(stdout)
    #print('STDOUT:{}'.format(stdout))

    process.wait()
    return return_code


def save_compressed_output(param_name, input_path, output_path, identifier):
    Path(output_path).mkdir(parents=True, exist_ok=True)

    temp = evaluation.evaluate_modal(input_path)
    temp.to_csv(output_path + param_name + identifier + "MODAL")
    temp = evaluation.evaluate(input_path)
    temp.to_csv(output_path + param_name + identifier)


if __name__ == '__main__':
    cwd = "/home/paincrash/Desktop/master-thesis/mobitopp-example-rastatt/"
    yaml_file = "config/rastatt/short-term-module-100p.yaml"
    yaml = yamlloader.YAML(cwd + yaml_file)
    yaml.data['resultFolder'] = "output/results/calibration/throwaway"
    fractions = [0.01, 0.1, 1]
    for fraction in fractions:
        yaml.data['fractionOfPopulation'] = fraction
        for seed in range(10, 11):
            yaml.data['seed'] = seed
            yaml.write()
            print("Running mobitopp seed: " + str(seed) + " frac: " + str(fraction))
            ret_val = run_mobitopp(cwd)
            print("Run complete: " + str(ret_val))
            save_compressed_output(str(seed) + "Seed",
                                   "/home/paincrash/Desktop/master-thesis/mobitopp-example-rastatt/output/results"
                                   "/calibration/throwaway/demandsimulationResult.csv",
                                   "/home/paincrash/Desktop/master-thesis/experiment_results_permanent"
                                   "/seed_experiment/" + str(fraction) + "/",
                                   "")
    yaml.reset()



