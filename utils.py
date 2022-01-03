import re


def extract_values_of_iteration(config, iteration):
    lines = config._text.split("\n")
    results = []
    for line in lines:
        test = re.sub("=\s*([-+])", "= \\1", line)
        test = re.split("(?<!=\s)([-+])", test)
        temp = 2 * iteration + 1
        results.append(" ".join(test[0:temp]))
    return "\n".join(results)
