# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

# This file contains all necessary information about the fields in the
# database that are used in the frontend. Because the data is send
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

# returns a list of json components, this list is for the filters and for the detailed information page
def get_medicine_info():

    models = [
        Medicine, 
        Authorisation,
        Procedure,
        Historybrandname,
        Historymah,
        Historyorphan,
        Historyprime,
    ]

    data = {}
    for category in Category:
        data[category.value] = []

    models_fields = []
    for model in models:
        models_fields += model._meta.get_fields()

    for field in models_fields:
        if hasattr(field, "category") and hasattr(field, "data_format") and hasattr(field, "data_value"):
            data[field.category].append({
                "data-key": field.name,
                "data-format": field.data_format,
                "data-value": field.data_value,
                })

    return data
    