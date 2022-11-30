from enum import Enum


# This is an enum that indicates the medicine type
# TODO: file that contains all enums so that every script can make use of it
class MedicineType(Enum):
    HUMAN_USE_ACTIVE = 0
    HUMAN_USE_WITHDRAWN = 1
    ORPHAN_ACTIVE = 2
    ORPHAN_WITHDRAWN = 3
    HUMAN_USE_REFUSED = 4
    ORPHAN_REFUSED = 5
