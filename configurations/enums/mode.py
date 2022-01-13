from enum import Enum


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

    @classmethod
    def get_mode_from_string(cls, string):
        d = {
            "ped": 3,
            "bike": 0,
            "car_d": 1,
            "car_p": 2,
            "put": 4,
            "taxi": 7,
            "bs": 9001,
            "cs": 9002,
            "rp": 9003,
            "b_cost": 1,
            "elasticity_parken": 1
        }
        for x in d.keys():
            if x in string:
                return Mode(d[x])
        return None