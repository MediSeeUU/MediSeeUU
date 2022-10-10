# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

# This file contains all necessary information about the fields in the
# database that are used in the frontend. Because the data is send
# to the frontend in JSON format it is necessary to send over additional information
# concerning each field. This additional data is used in the filter function
# and additional medicine information page among others.
# ----------------------------------------------------------------------------

import json

# returns a list of json components depending on permission level, this list is for the filters and for the detailed information page
def get_medicine_info(perm):

    # List with dictionaries
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
            "data-key": "decisiondate",
            "data-front-key": "DecisionYear",
            "data-format": "number",
            "data-value": "Decision Year",
        },
        {
            "data-key": "atccode",
            "data-front-key": "ATCCodeL2",
            "data-format": "string",
            "data-value": "ATC Code",
        },
        {
            "data-key": "status",
            "data-front-key": "Status",
            "data-format": "string",
            "data-value": "Status",
        },
    ]

    # List with dictionaries
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

    # List with dictionaries
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

    # List with dictionaries
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

    # List with dictionaries
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

    # List with dictionaries
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

    Additional_Resources = [
        {
            "data-key": "emaurl",
            "data-front-key": "EMAurl",
            "data-format": "link",
            "data-value": "EMA url",
        },
        {
            "data-key": "ecurl",
            "data-front-key": "ECurl",
            "data-format": "link",
            "data-value": "EC url",
        },
    ]

    # The data object constructs the json that will be returned, each item is filterd on the acces level a user has
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
        "Additional Resources": [
            x for x in Additional_Resources if filterFunc(perm, x)
        ],
    }

    return data


# Checks wether the user has permission for this item
def filterFunc(perm, item):
    for key, value in item.items():
        if value in perm:
            return True
    return False
