from enum import Enum


class ViolationType(Enum):
    # Car Violations
    PARKING = 1
    SPEEDING = 2
    RED_LIGHT = 3
    NO_PARKING = 4
    # Pedestrian Violations
    JAYWALKING = 5
    CROSSING = 6
    # Traffic Violations
    WRONG_WAY = 7
    NO_ENTRY = 8
    # Other Violations
    OTHER = 9
    UNKNOWN = 10


def print_violation_type(violation_type: ViolationType):
    print(violation_type)
