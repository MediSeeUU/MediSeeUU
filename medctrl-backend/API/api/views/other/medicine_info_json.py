import json


def get_medicine_info(perm):

    General_Information = [
        {
            "data-key": "brandname",
            "data-front-key": "BrandName",
            "data-format": "string",
            "data-value": "Brand Name",
        },
        {
            "data-key": "mah",
            "data-front-key": "MAH",
            "data-format": "string",
            "data-value": "Marketing Authorisation Holder",
        },
        {
            "data-key": "activesubstance",
            "data-front-key": "ActiveSubstance",
            "data-format": "string",
            "data-value": "Active Substance",
        },
        {
            "data-key": "decisiondate",
            "data-front-key": "DecisionDate",
            "data-format": "date",
            "data-value": "Decision Date",
        },
        {
            "data-key": "atccode",
            "data-front-key": "ATCCodeL2",
            "data-format": "string",
            "data-value": "ATC Code",
        },
    ]

    Identifying_Information = [
        {
            "data-key": "emanumber",
            "data-front-key": "ApplicationNo",
            "data-format": "number",
            "data-value": "Application Number",
        },
        {
            "data-key": "eunumber",
            "data-front-key": "EUNoShort",
            "data-format": "number",
            "data-value": "Short EU Number",
        },
    ]

    Co_Rapporteur = [
        {
            "data-key": "rapporteur",
            "data-front-key": "Rapporteur",
            "data-format": "string",
            "data-value": "Rapporteur",
        },
        {
            "data-key": "corapporteur",
            "data-front-key": "CoRapporteur",
            "data-format": "string",
            "data-value": "Co-Rapporteur",
        },
    ]

    Medicine_Designations = [
        {
            "data-key": "atmp",
            "data-front-key": "ATMP",
            "data-format": "bool",
            "data-value": "ATMP",
        },
        {
            "data-key": "orphan",
            "data-front-key": "OrphanDesignation",
            "data-format": "bool",
            "data-value": "Orphan Designation",
        },
        {
            "data-key": "newactivesubstance",
            "data-front-key": "NASQualified",
            "data-format": "bool",
            "data-value": "NAS Qualified",
        },
        {
            "data-key": "prime",
            "data-front-key": "PRIME",
            "data-format": "bool",
            "data-value": "PRIME",
        },
    ]

    Legal_Information = [
        {
            "data-key": "legalscope",
            "data-front-key": "LegalSCope",
            "data-format": "string",
            "data-value": "Legal Scope",
        },
        {
            "data-key": "legalbasis",
            "data-front-key": "LegalType",
            "data-format": "string",
            "data-value": "Legal Type",
        },
    ]

    Authorisation_Timing = [
        {
            "data-key": "acceleratedgranted",
            "data-front-key": "AcceleratedGranted",
            "data-format": "bool",
            "data-value": "Accelerated Granted",
        },
        {
            "data-key": "acceleratedmaintained",
            "data-front-key": "AcceleratedExecuted",
            "data-format": "bool",
            "data-value": "Accelerated Executed",
        },
        {
            "data-key": "authorisationactivetime",
            "data-front-key": "ActiveTimeElapsed",
            "data-format": "number",
            "data-value": "Active Time Elapsed (days)",
        },
        {
            "data-key": "authorisationstoppedtime",
            "data-front-key": "ClockStopElapsed",
            "data-format": "number",
            "data-value": "Clock Stop Elapsed (days)",
        },
        {
            "data-key": "authorisationtotaltime",
            "data-front-key": "TotalTimeElapsed",
            "data-format": "number",
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
