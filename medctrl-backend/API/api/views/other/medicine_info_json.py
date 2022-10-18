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
    HistoryATCCode,
    HistoryAuthorisationStatus,
    HistoryAuthorisationType,
    HistoryBrandName,
    HistoryMAH,
    HistoryOD,
    HistoryPrime,
    HistoryEUOrphanCon
)


# returns a list of json components using medicine_models,
# this list is for the filters and for the detailed information page
def get_medicine_info(perm, mock=None):
    # make a JSON list for every category in medicine_models.common.Category
    data = {}
    for category in Category:
        data[category.value] = []

    models_fields = []

    if mock is None:
        # place all models here
        models = [
            Medicine,
            HistoryATCCode,
            HistoryAuthorisationStatus,
            HistoryAuthorisationType,
            HistoryBrandName,
            HistoryMAH,
            HistoryOD,
            HistoryPrime,
            HistoryEUOrphanCon
        ]

        # make a list containing all the fields from all the models
        for model in models:
            models_fields += model._meta.get_fields()
    else:
        models_fields = mock

    # for every field created with create_dashboard_column(), add it to the correct category in JSON
    for field in models_fields:
        if hasattr(field, "dashboard_columns") and has_permission(perm, field.name):
            for dashboard_column in field.dashboard_columns:
                if has_permission(perm, dashboard_column.data_key):
                    data[dashboard_column.category.value].append({
                        "data-key": dashboard_column.data_key,
                        "data-format": dashboard_column.data_format,
                        "data-value": dashboard_column.data_value,
                    })

    return data


# checks if user has permission to view a field
def has_permission(perm, name):
    return name in perm
