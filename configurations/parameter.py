from enum import Enum


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
        return NumberOfCars.NO_CAR.value
    elif param.__contains__("pkw_1"):
        return NumberOfCars.ONE_CAR.value
    return None


def get_employment_from_string(param):
    if param.__contains__("beruft_on"):
        return Employment.EMPLOYED.value
    elif param.__contains__("student_on") or param.__contains__("educ_on_"):
        return Employment.STUDENT.value
    elif param.__contains__("home_on") or param.__contains__("arb_on"):
        return Employment.HOME.value
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
        return HouseholdSize.SIZE_2.value
    elif param.__contains__("hhgr_34"):
        return HouseholdSize.SIZE_3_OR_BIGGER.value
    return None


def get_umland_from_string(param):
    if param.__contains__("_uml_"):
        return True
    return None





def get_economical_group_from_string(param):
    if param.__contains__("inc_high") or param.__contains__("high_inc"):
        return EconomicalGroup.RICH.value
    elif param.__contains__("inc_low"):
        return EconomicalGroup.POOR.value
    return None


def get_age_group_from_string(param):
    if param.__contains__("age_0_17") or param.__contains__("age_1_on"):
        return 0
    elif param.__contains__("age_18_29"):
        return 18
    elif param.__contains__("age_50_59"):
        return 50
    elif param.__contains__("age_60_69"):
        return 60
    elif param.__contains__("age_70_100"):
        return 70
    elif param.__contains__("age_56_on"):
        return [50, 60]
    elif param.__contains__("age_78_on"):
        return [70, 100]


def get_activity_from_string(param):
    if param.__contains__("arbeit"):
        return ActivityGroup.WORK.value
    elif param.__contains__("ausb"):
        return ActivityGroup.EDUCATION.value
    elif param.__contains__("eink"):
        return ActivityGroup.SHOPPING.value
    elif param.__contains__("freiz"):
        return ActivityGroup.LEISURE.value
    elif param.__contains__("service"):
        return ActivityGroup.SERVICE.value
    elif param.__contains__("_home_") and not param.__contains__("_home_on"):
        # This is a conflict with parameters in destination choice
        # for Home-keeper/Unemployment and therefore checked more closely
        return ActivityGroup.HOME.value
    elif param.__contains__("dienst"):
        return ActivityGroup.BUSINESS.value
    return None


def get_mode_from_string(string):
    d = {
        "_ped": 3,
        "_bike": 0,
        "_car_d": 1,
        "_car_p": 2,
        "_put": 4,
        "_taxi": 7,
        "_bs": 9001,
        "_cs": 9002,
        "_rp": 9003,
        "b_cost": 1,
        "elasticity_parken": 1
    }
    for x in d.keys():
        if x in string:
            return d[x]
    return None


mode_and_decipher = [("tripMode", get_mode_from_string),
                     ("activityType", get_activity_from_string),
                     ("age", get_age_group_from_string),
                     ("employment", get_employment_from_string),
                     ("gender", get_gender_from_string),
                     ("hasCommuterTicket", get_commuter_ticket_from_string),
                     ("economicalStatus", get_economical_group_from_string),
                     ("totalNumberOfCars", get_number_of_cars_from_string),

                     ("nominalSize", get_household_size_from_string),

                     # All of the following methods have yet to be extracted from the simulation output.
                     ("workdayNotImplemented", get_workday_from_string),  # Weekday
                     ("reliefNotImplemented", get_relief_from_string),
                     ("PreviousTripNotImplemented", get_prev_mode_from_string),
                     ("CarsPerAdultNotImplemented", get_carav_from_string),
                     ("HasEBikeNotImplemented", get_ebike_from_string),
                     ("HasCSMembershipNotImplemented", get_cs_membership_from_string),
                     ("isUmlandNotImplemented", get_umland_from_string)
                     ]


def get_all_parameter_limitations(param):
    ret_dict = {}
    for name, f in mode_and_decipher:
        if f(param) is not None:
            ret_dict[name] = f(param)
    return ret_dict


def group_employment(df):
    group_list(df, "employment", ['STUDENT_PRIMARY',  'STUDENT_SECONDARY', 'STUDENT_TERTIARY', 'EDUCATION'], "STUDENT")
    group_list(df, "employment", ['FULLTIME', 'PARTTIME', "MARGINAL"], "EMPLOYED")
    group_list(df, "employment", ['UNEMPLOYED', 'HOMEKEEPER'], "HOME")
    group_list(df, "employment", ["INFANT", "RETIRED", "UNKNOWN"], "UNSPECIFIED")



class Employment(Enum):
    EMPLOYED = "EMPLOYED"
    STUDENT = "STUDENT"
    HOME = "HOME"
    UNCLASSIFIED = "UNSPECIFIED"

    @classmethod
    def get_employment_from_int(cls, val):
        if val in ['STUDENT_PRIMARY',  'STUDENT_SECONDARY', 'STUDENT_TERTIARY', 'EDUCATION']:
            return Employment.STUDENT.value
        elif val in ['FULLTIME', 'PARTTIME', "MARGINAL"]:
            return Employment.EMPLOYED.value
        elif val in ['UNEMPLOYED', 'HOMEKEEPER']:
            return Employment.HOME.value
        return Employment.UNCLASSIFIED.value


def group_household_size(df):
    group(df, "nominalSize", 3, 6)


class HouseholdSize(Enum):
    SIZE_2 = 0
    SIZE_3_OR_BIGGER = 1
    UNSPECIFIED = -1

    @classmethod
    def get_hh_size_from_int(cls, val):
        if val == 2:
            return HouseholdSize.SIZE_2.value
        elif val >= 3:
            return HouseholdSize.SIZE_3_OR_BIGGER.value
        return HouseholdSize.UNSPECIFIED.value


def group_number_of_cars(df):
    group(df, "totalNumberOfCars", 2, 6)


class NumberOfCars(Enum):
    NO_CAR = 0
    ONE_CAR = 1
    UNSPECIFIED = 2

    @classmethod
    def get_num_cars_from_int(cls, val):
        if val == 0:
            return NumberOfCars.NO_CAR.value
        elif val == 1:
            return NumberOfCars.ONE_CAR.value
        return NumberOfCars.UNSPECIFIED.value


def group_economical_status(df):
    group(df, "economicalStatus", 1, 2)
    group(df, "economicalStatus", 4, 5)


class EconomicalGroup(Enum):
    POOR = 1
    RICH = 5
    UNSPECIFIED = 3

    @classmethod
    def get_eco_group_from_int(cls, val):
        if 1 <= val <= 2:
            return EconomicalGroup.POOR.value
        elif 4 <= val <= 5:
            return EconomicalGroup.RICH.value
        return EconomicalGroup.UNSPECIFIED.value


def group(df, colname, valfrom, valto, target=None):
    if target is None:
        target = valfrom
    df.loc[(df[colname] >= valfrom) & (df[colname] <= valto), [colname]] = target

def group_list(df, colname, list, target):
    df.loc[df[colname].isin(list), [colname]] = target

def group_age(df):
    group(df, "age", 0, 17)
    group(df, "age", 18, 29)
    group(df, "age", 30, 49)
    group(df, "age", 50, 59)
    group(df, "age", 60, 69)
    group(df, "age", 70, 100)
    group(df, "age", 100, 120)


class AgeGroup(Enum):
    """
    Age is not used by the precise year but rather by a group, so we can aggregate further when using this mode
    """
    FROM_0_TO_17 = 0
    FROM_18_TO_29 = 1
    FROM_50_TO_59 = 2
    FROM_60_TO_69 = 3
    FROM_70_TO_100 = 4
    FROM_100_TO_120 = 5
    FROM_70_TO_120 = 6
    FROM_50_TO_69 = 7

    UNCLASSIFIED = 9

    @classmethod
    def int_to_group(cls, value):
        if 0 <= value <= 17:
            return AgeGroup.FROM_0_TO_17.value
        elif 18 <= value <= 29:
            return AgeGroup.FROM_18_TO_29.value
        elif 50 <= value <= 59:
            return AgeGroup.FROM_50_TO_59.value
        elif 60 <= value <= 69:
            return AgeGroup.FROM_60_TO_69.value
        elif 70 <= value <= 100:
            return AgeGroup.FROM_70_TO_100.value
        elif 100 <= value <= 120:
            return AgeGroup.FROM_100_TO_120.value
        return AgeGroup.UNCLASSIFIED.value


def group_activity(df):
    group(df, "activityType", 31, 34, target=ActivityGroup.EDUCATION.value)
    group(df, "activityType", 41, 42, target=ActivityGroup.SHOPPING.value)
    group(df, "activityType", 51, 52, target=ActivityGroup.LEISURE.value)
    group(df, "activityType", 12, 12, target=ActivityGroup.LEISURE.value)
    group(df, "activityType", 11, 11, target=ActivityGroup.SHOPPING.value)  # Is this correct?


class ActivityGroup(Enum):
    WORK = 1
    BUSINESS = 2
    EDUCATION = 3
    SHOPPING = 4
    LEISURE = 5 # DEFAULT VALUE
    SERVICE = 6
    HOME = 7

    @classmethod
    def activity_int_to_mode(cls, val):

        if val == 1:
            return ActivityGroup.WORK.value
        elif val == 2:
            return ActivityGroup.BUSINESS.value
        elif val in [3, 31, 32, 33, 34]:
            return ActivityGroup.EDUCATION.value
        elif val in [4, 41, 42, 11]:  # TODO verify that activity 11 (Private_visit) maps to shopping
            return ActivityGroup.SHOPPING.value
        elif val == 6:
            return ActivityGroup.SERVICE.value
        elif val == 7:
            return ActivityGroup.HOME.value
        return ActivityGroup.LEISURE.value  # LEISURE is the default for all actions


class Mode(Enum):
    BIKE = 0
    DRIVER = 1
    PASSENGER = 2
    PEDESTRIAN = 3
    PUBLIC_TRANSPORT = 4
    TAXI = 7
    BIKE_SHARING = 9001  # TODO these modes have multiple representors in mobitopp and are not yet in the simulation
    CAR_SHARING = 9002
    RIDE_POOLING = 9003


def get_parameter_bounds(name):
    return -15, 15


class Parameter:
    def __init__(self, name, value=0):
        self.name = name
        self.value = value
        self.lower_bound, self.upper_bound = get_parameter_bounds(name)
        self.requirements = get_all_parameter_limitations(name)

    def __str__(self):
        return f"{self.name}, {self.value} [{self.lower_bound}, {self.upper_bound}], {self.requirements}"

    def set(self, value):
        self.value = value

