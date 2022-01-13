from enum import Enum

def get_age_group_from_string(param):
    if param.__contains__("age_0_17") or param.__contains__("age_1_on"):
        return AgeGroup.FROM_0_TO_17
    elif param.__contains__("age_18_29"):
        return AgeGroup.FROM_18_TO_29
    elif param.__contains__("age_50_59"):
        return AgeGroup.FROM_50_TO_59
    elif param.__contains__("age_60_69"):
        return AgeGroup.FROM_60_TO_69
    elif param.__contains__("age_70_100"):
        return AgeGroup.FROM_70_TO_100
    elif param.__contains__("age_70_120"):
        return AgeGroup.FROM_70_TO_120
    elif param.__contains__("age_56_on"):
        return AgeGroup.FROM_50_TO_69
    elif param.__contains__("age_78_on"):
        return AgeGroup.FROM_70_TO_120



class AgeGroup(Enum):
    """
    Age is not used by the precise year but rather by a group, so we can aggregate further when using this mode
    [0 <= AGE <= 17]
    [18 <= AGE <= 29]
    [50 <= AGE <= 59]
    [50 <= AGE <= 69]
    [60 <= AGE <= 69]
    [70 <= AGE <= 100]
    [70 <= AGE <= 120]
    """
    FROM_0_TO_17 = 0
    FROM_18_TO_29 = 1
    FROM_50_TO_59 = 2
    FROM_60_TO_69 = 3
    FROM_70_TO_100 = 4
    FROM_70_TO_120 = 5
    FROM_50_TO_69 = 6

    UNCLASSIFIED = 9

    @classmethod
    def int_to_group(cls, value):
        if 0 <= value <= 17:
            return AgeGroup.FROM_0_TO_17
        elif 18 <= value <= 29:
            return AgeGroup.FROM_18_TO_29
        elif 50 <= value <= 59:
            return AgeGroup.FROM_50_TO_59
        elif 60 <= value <= 69:
            return AgeGroup.FROM_60_TO_69
        elif 70 <= value <= 100:
            return AgeGroup.FROM_70_TO_100
        elif 100 <= value <= 120:
            return AgeGroup.FROM_100_TO_120
        return AgeGroup.UNCLASSIFIED



