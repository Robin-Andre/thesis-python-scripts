from enum import Enum

def get_economical_group_from_string(param):
    if param.__contains__("inc_high") or param.__contains__("high_inc"):
        return EconomicalGroup.RICH
    elif param.__contains__("inc_low"):
        return EconomicalGroup.POOR
    return None


class EconomicalGroup(Enum):
    POOR = 0
    RICH = 1
    UNSPECIFIED = 2

    @classmethod
    def get_eco_group_from_int(cls, val):
        if 1 <= val <= 2:
            return EconomicalGroup.POOR
        elif 4 <= val <= 5:
            return EconomicalGroup.RICH
        return EconomicalGroup.UNSPECIFIED


