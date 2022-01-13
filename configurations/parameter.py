from enum import Enum

from configurations.enums.agegroup import get_age_group_from_string
from configurations.enums.economicalgroup import get_economical_group_from_string
from configurations.enums.activitygroup import get_activity_from_string
from configurations.enums.mode import Mode


def get_relief_from_string(param):
    if param.__contains__("relief_high"):
        return True
    return None


def get_workday_from_string(param):
    if param.__contains__("arbwo"):
        return True
    return None


def get_gender_from_string(param):
    if param.__contains__("female"):
        return True
    return None


def get_number_of_cars_from_string(param):
    if param.__contains__("pkw_0") or param.__contains__("nocar"):
        return NumberOfCars.NO_CAR
    elif param.__contains__("pkw_1"):
        return NumberOfCars.ONE_CAR
    return None


def get_employment_from_string(param):
    if param.__contains__("beruft_on"):
        return Employment.EMPLOYED
    elif param.__contains__("student_on") or param.__contains__("educ_on_"):
        return Employment.STUDENT
    elif param.__contains__("home_on") or param.__contains__("arb_on"):
        return Employment.HOME
    return None


def get_commuter_ticket_from_string(param):
    if param.__contains__("zk_on"):
        return True
    return None


def get_prev_mode_from_string(param):
    if param.__contains__("mode_bef"):
        return True
    return None


def get_carav_from_string(param):
    if param.__contains__("carav_on"):
        return True
    return None


def get_ebike_from_string(param):
    if param.__contains__("ebike"):
        return True
    return None


def get_cs_membership_from_string(param):
    if param.__contains__("csmit_on"):
        return True
    return None


def get_household_size_from_string(param):
    if param.__contains__("hhgr_2"):
        return HouseholdSize.SIZE_2
    elif param.__contains__("hhgr_34"):
        return HouseholdSize.SIZE_3_OR_BIGGER
    return None


def get_umland_from_string(param):
    if param.__contains__("_uml_"):
        return True
    return None


mode_and_decipher = [("tripMode", Mode.get_mode_from_string),
                     ("activityType", get_activity_from_string),
                     ("age", get_age_group_from_string),
                     ("employment", get_employment_from_string),
                     ("gender", get_gender_from_string),
                     ("hasCommuterTicket", get_commuter_ticket_from_string),
                     ("economicalStatus", get_economical_group_from_string),
                     ("totalNumberOfCars", get_number_of_cars_from_string),
                     ("timeBegin", get_workday_from_string),  # Weekday
                     ("nominalSize", get_household_size_from_string),

                     # All of the following methods have yet to be extracted from the simulation output.
                     ("reliefNotImplemented", get_relief_from_string),
                     ("PreviousTripNotImplemented", get_prev_mode_from_string),
                     ("CarsPerAdultNotImplemented", get_carav_from_string),
                     ("HasEBikeNotImplemented", get_ebike_from_string),
                     ("HasCSMembershipNotImplemented", get_cs_membership_from_string),
                     ("isUmlandNotImplemented", get_umland_from_string)
                     ]


def get_all_parameter_limitations(param):
    temp_list = []
    ret_list = []
    for name, f in mode_and_decipher:
        if f(param) is not None:
            temp_list.append(name + "=" + str(f(param)))
            ret_list.append((name, f(param)))
    return ret_list


def get_parameter_bounds(param):
    return -15, 15


class Employment(Enum):
    EMPLOYED = 0,
    STUDENT = 1,
    HOME = 2


class HouseholdSize(Enum):
    SIZE_2 = 0,
    SIZE_3_OR_BIGGER = 1,
    UNSPECIFIED = -1


class NumberOfCars(Enum):
    NO_CAR = 0,
    ONE_CAR = 1


class Parameter:
    def __init__(self, name):
        self.name = name
        self.lower_bound, self.upper_bound = get_parameter_bounds(name)
        self.requirements = get_all_parameter_limitations(name)

    def __str__(self):
        return f"{self.name}, {self.lower_bound}, {self.upper_bound}, {len(self.requirements)} : {self.requirements}"
