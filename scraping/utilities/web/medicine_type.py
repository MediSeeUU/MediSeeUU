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


# Files named 'public-assessment-report' will be the highest priority in the search.
epar_priority_list: list[str] = [
    "public-assessment-report",
    "procedural-steps-taken-authorisation",
    "epar",
    "procedural-steps",
    "scientific-discussion"
]

omar_priority_list: list[str] = [
    "orphan-maintenance-assessment-report",
    "orphan-medicine-assessment-report",
    "orphan-medicine",
    "orphan-designation-assessment-report"
]

odwar_priority_list: list[str] = [
    "orphan-designation-withdrawal-assessment-report"
]
