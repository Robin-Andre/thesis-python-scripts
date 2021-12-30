DEFAULT_VAL = 100


class Limit:

    def __init__(self, config):
        self.limits = {}
        for param in config.get_parameter_list():
            self.limits[param] = (-DEFAULT_VAL, DEFAULT_VAL)


class ModeLimitSimple(Limit):

    def __init__(self, config):
        self.limits = {}
        for param in config.get_parameter_list():
            self.limits[param] = self.__get_limit_by_parameter(param)

    def __get_limit_by_parameter(self, parameter):
        if parameter == "b_tt_ped":
            # This is a special case where values beyond -0.8 caused crashes
            return -1, 0
        if parameter.__contains__("sig"):
            # TODO Disabled sigma values for current experiment, figure out which values fit better
            return 0, 0

        if parameter.__contains__("b_tt"):
            # If the parameter is based on travel time positive values seem unfeasible:
            return -15, 0

        return -15, 15


class DestinationLimitSimple(Limit):

    def __init__(self, config):
        self.limits = {}
        for param in config.get_parameter_list():
            self.limits[param] = self.__get_limit_by_parameter(param)


    def __get_limit_by_parameter(self, parameter):

        if parameter.__contains__("b_tt"):
            # If the parameter is based on travel time positive values seem unfeasible:
            return -1, 0

        return -50, 50