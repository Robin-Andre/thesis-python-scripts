from enum import Enum


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
