import json


def get_medicine_info(perm):
    General_Information = [
        {"data-key": "brandname", "data-value": "Brand Name"},
        {"data-key": "mah", "data-value": "Marketing Authorisation Holder"},
        {"data-key": "activesubstance", "data-value": "Active Substance"},
        {"data-key": "decisiondate", "data-value": "Decision Date"},
        {"data-key": "atccode", "data-value": "ATC Code"},
    ]

    Identifying_Information = [
        {"data-key": "emanumber", "data-value": "Application Number"},
        {"data-key": "eunumber", "data-value": "Short EU Number"},
    ]

    Co_Rapporteur = [
        {"data-key": "rapporteur", "data-value": "Rapporteur"},
        {"data-key": "corapporteur", "data-value": "Co-Rapporteur"},
    ]

    Medicine_Designations = [
        {"data-key": "atmp", "data-value": "ATMP"},
        {"data-key": "orphan", "data-value": "Orphan Designation"},
        {"data-key": "newactivesubstance", "data-value": "NAS Qualified"},
        {"data-key": "prime", "data-value": "PRIME"},
    ]

    Legal_Information = [
        {"data-key": "legalscope", "data-value": "Legal Scope"},
        {"data-key": "legalbasis", "data-value": "Legal Type"},
    ]

    Authorisation_Timing = [
        {"data-key": "acceleratedgranted", "data-value": "Accelerated Granted"},
        {"data-key": "acceleratedmaintained", "data-value": "Accelerated Executed"},
        {
            "data-key": "authorisationactivetime",
            "data-value": "Active Time Elapsed (days)",
        },
        {
            "data-key": "authorisationstoppedtime",
            "data-value": "Clock Stop Elapsed (days)",
        },
        {
            "data-key": "authorisationtotaltime",
            "data-value": "Total Time Elapsed (days)",
        },
    ]

    data = {
        "General Information": [x for x in General_Information if filterFunc(perm, x)],
        "Identifying Information": [
            x for x in Identifying_Information if filterFunc(perm, x)
        ],
        "(Co-)Rapporteur": [x for x in Co_Rapporteur if filterFunc(perm, x)],
        "Medicine Designations": [
            x for x in Medicine_Designations if filterFunc(perm, x)
        ],
        "Legal Information": [x for x in Legal_Information if filterFunc(perm, x)],
        "Authorisation Timing": [
            x for x in Authorisation_Timing if filterFunc(perm, x)
        ],
    }

    return data


def filterFunc(perm, item):
    for key, value in item.items():
        if value in perm:
            return True
    return False
