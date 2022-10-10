# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

# This file contains all necessary information about the fields in the
# database that are used in the frontend. Because the data is sent
# to the frontend in JSON format it is necessary to send over additional information
# concerning each field. This additional data is used in the filter function
# and additional medicine information page among others.
# ----------------------------------------------------------------------------

from api.models.medicine_models.common import Category
from api.models.medicine_models import (
    Medicine,
    Authorisation,
    Procedure,
    Historybrandname,
    Historymah,
    Historyorphan,
    Historyprime,
)


# returns a list of json components using medicine_models,
# this list is for the filters and for the detailed information page
def get_medicine_info(perm):

    # place all models here
    models = [
        Medicine,
        Authorisation,
        Procedure,
        Historybrandname,
        Historymah,
        Historyorphan,
        Historyprime,
    ]

    # make a JSON list for every category in medicine_models.common.Category
    data = {}
    for category in Category:
        data[category.value] = []

    # make a list containing all the fields from all the models
    models_fields = []
    for model in models:
        models_fields += model._meta.get_fields()

    # for every field created with create_dashboard_column(), add it to the correct category in JSON
    for field in models_fields:
        if hasattr(field, "category") and hasattr(field, "data_format") \
                and hasattr(field, "data_value") and has_permission(perm, field):
            data[field.category].append({
                "data-key": field.name,
                "data-format": field.data_format,
                "data-value": field.data_value,
            })

    return data


# checks if user has permission to view a field
def has_permission(perm, field):
    return field.name in perm
