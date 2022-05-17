import json


def get_medicine_info():
    data = {
        "General Information": [
            {"data-key": "brandname", "data-value": "Brand Name"},
            {"data-key": "mah", "data-value": "Marketing Authorisation Holder"},
            {"data-key": "activesubstance", "data-value": "Active Substance"},
            {"data-key": "decisiondate", "data-value": "Decision Date"},
            {"data-key": "atccode", "data-value": "ATC Code"},
        ],
        "Identifying Information": [
            {"data-key": "emanumber", "data-value": "Application Number"},
            {"data-key": "eunumber", "data-value": "Short EU Number"},
        ],
        "(Co-)Rapporteur": [
            {"data-key": "rapporteur", "data-value": "Rapporteur"},
            {"data-key": "corapporteur", "data-value": "Co-Rapporteur"},
        ],
        "Medicine Designations": [
            {"data-key": "atmp", "data-value": "ATMP"},
            {"data-key": "orphan", "data-value": "Orphan Designation"},
            {"data-key": "newactivesubstance", "data-value": "NAS Qualified"},
            {"data-key": "prime", "data-value": "PRIME"},
        ],
        "Legal Information": [
            {"data-key": "legalscope", "data-value": "Legal Scope"},
            {"data-key": "legalbasis", "data-value": "Legal Type"},
        ],
        "Authorisation Timing": [
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
        ],
    }
    return data
