from enum import Enum


class ActivityGroup(Enum):
    WORK = 0
    BUSINESS = 1
    EDUCATION = 2
    SHOPPING = 3
    LEISURE = 4 # DEFAULT VALUE
    SERVICE = 5

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
            11: ActivityGroup.SHOPPING, # TODO is this accurate?
        }
        if val in d.keys():
            return d[val]
        else:
            return ActivityGroup.LEISURE # DEFAULT case since everything uses this