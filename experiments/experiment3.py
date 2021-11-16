import evaluation
import mobitopp_execution as simulation
import yamlloader


if __name__ == '__main__':
    cwd = "/home/paincrash/Desktop/master-thesis/mobitopp-example-rastatt/"
    csv_path = cwd + "output/results/calibration/throwaway/demandsimulationResult.csv"
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
            ret_val = simulation.run()
            print("Run complete: " + str(ret_val))
            evaluation.save_compressed_output(str(seed) + "Seed",
                                              csv_path,
                                   "/home/paincrash/Desktop/master-thesis/experiment_results_permanent"
                                   "/seed_experiment/" + str(fraction) + "/",
                                   "")
    yaml.reset()



