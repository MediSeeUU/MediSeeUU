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
from ...models.medicine_models.medicine import Medicine
from ...models.medicine_models.procedure import Procedure
from ...models.medicine_models.authorisation import Authorisation


# returns a list of json components depending on permission level, this list is for the filters and for the detailed information page
def get_medicine_info(perm):

    # List with dictionaries
    General_Information = [
        {
            "data-key": "test",
            "data-format": "string",
            "data-value": "test",
        },
        {
            "data-key": "brandname",
            "data-format": "string",
            "data-value": "Brand Name",
        },
        {
            "data-key": "mah",
            "data-format": "string",
            "data-value": "Marketing Authorisation Holder",
        },
        {
            "data-key": "activesubstance",
            "data-format": "string",
            "data-value": "Active Substance",
        },
        {
            "data-key": "decisiondate",
            "data-format": "date",
            "data-value": "Decision Date",
        },
        {
            "data-key": "decisionyear",
            "data-format": "number",
            "data-value": "Decision Year",
        },
        {
            "data-key": "atccode",
            "data-format": "string",
            "data-value": "ATC Code",
        },
        {
            "data-key": "status",
            "data-format": "string",
            "data-value": "Status",
        },
    ]

    # List with dictionaries
    Identifying_Information = [
        {
            "data-key": "emanumber",
            "data-format": "number",
            "data-value": "Application Number",
        },
        {
            "data-key": "eunumber",
            "data-format": "number",
            "data-value": "Short EU Number",
        },
    ]

    # List with dictionaries
    Co_Rapporteur = [
        {
            "data-key": "rapporteur",
            "data-format": "string",
            "data-value": "Rapporteur",
        },
        {
            "data-key": "corapporteur",
            "data-format": "string",
            "data-value": "Co-Rapporteur",
        },
    ]

    # List with dictionaries
    Medicine_Designations = [
        {
            "data-key": "atmp",
            "data-format": "bool",
            "data-value": "ATMP",
        },
        {
            "data-key": "orphan",
            "data-format": "bool",
            "data-value": "Orphan Designation",
        },
        {
            "data-key": "newactivesubstance",
            "data-format": "bool",
            "data-value": "NAS Qualified",
        },
        {
            "data-key": "prime",
            "data-format": "bool",
            "data-value": "PRIME",
        },
    ]

    # List with dictionaries
    Legal_Information = [
        {
            "data-key": "legalscope",
            "data-format": "string",
            "data-value": "Legal Scope",
        },
        {
            "data-key": "legalbasis",
            "data-format": "string",
            "data-value": "Legal Type",
        },
    ]

    # List with dictionaries
    Authorisation_Timing = [
        {
            "data-key": "acceleratedgranted",
            "data-format": "bool",
            "data-value": "Accelerated Granted",
        },
        {
            "data-key": "acceleratedmaintained",
            "data-format": "bool",
            "data-value": "Accelerated Executed",
        },
        {
            "data-key": "authorisationactivetime",
            "data-format": "number",
            "data-value": "Active Time Elapsed (days)",
        },
        {
            "data-key": "authorisationstoppedtime",
            "data-format": "number",
            "data-value": "Clock Stop Elapsed (days)",
        },
        {
            "data-key": "authorisationtotaltime",
            "data-format": "number",
            "data-value": "Total Time Elapsed (days)",
        },
    ]

    Additional_Resources = [
        {
            "data-key": "emaurl",
            "data-format": "link",
            "data-value": "EMA url",
        },
        {
            "data-key": "ecurl",
            "data-format": "link",
            "data-value": "EC url",
        },
    ]

    # The Data object constructs the json that will be returned, each item is filterd on the acces level a user has
    data = {
        "General Information": General_Information,
        "Identifying Information": Identifying_Information,
        "(Co-)Rapporteur": Co_Rapporteur,
        "Medicine Designations": Medicine_Designations,
        "Legal Information": Legal_Information,
        "Authorisation Timing": Authorisation_Timing,
        "Additional Resources": Additional_Resources
    }

    return data