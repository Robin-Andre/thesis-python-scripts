from enum import Enum


def get_activity_from_string(param):
    if param.__contains__("arbeit"):
        return ActivityGroup.WORK
    elif param.__contains__("ausb"):
        return ActivityGroup.EDUCATION
    elif param.__contains__("eink"):
        return ActivityGroup.SHOPPING
    elif param.__contains__("freiz"):
        return ActivityGroup.LEISURE
    elif param.__contains__("service"):
        return ActivityGroup.SERVICE
    elif param.__contains__("_home_") and not param.__contains__("_home_on"):
        # This is a conflict with parameters in destination choice
        # for Home-keeper/Unemployment and therefore checked more closely
        return ActivityGroup.HOME
    elif param.__contains__("dienst"):
        return ActivityGroup.BUSINESS
    return None


class ActivityGroup(Enum):
    WORK = 0
    BUSINESS = 1
    EDUCATION = 2
    SHOPPING = 3
    LEISURE = 4  # DEFAULT VALUE
    SERVICE = 5
    HOME = 7

    @classmethod
    def activity_int_to_mode(cls, val):
        d = {
            1: ActivityGroup.WORK,
            2: ActivityGroup.BUSINESS,
            3: ActivityGroup.EDUCATION,
            4: ActivityGroup.SHOPPING,
            5: ActivityGroup.LEISURE,
            6: ActivityGroup.SERVICE,
            31: ActivityGroup.EDUCATION,
            32: ActivityGroup.EDUCATION,
            33: ActivityGroup.EDUCATION,
            34: ActivityGroup.EDUCATION,
            41: ActivityGroup.SHOPPING,
            42: ActivityGroup.SHOPPING,
            11: ActivityGroup.SHOPPING,  # TODO is this accurate?
        }
        if val in d.keys():
            return d[val]
        else:
            return ActivityGroup.LEISURE  # DEFAULT case since everything uses this
