# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

# This file contains all necessary information about the fields in the
# database that are used in the frontend. Because the data is sent
# to the frontend in JSON format it is necessary to send over additional information
# concerning each field. This additional data is used in the filter function
# and additional medicine information page among others.
# ----------------------------------------------------------------------------

from api.models.create_dashboard_columns import Category
from api.models import models


# returns a list of json components using medicine_models,
# this list is for the filters and for the detailed information page
def get_medicine_info(perm, mock=None):
    """
    returns a list of json components using medicine_models,
    this list is for the filters and for the detailed information page.

    Args:
        perm (list[attributes]): the permissions of the current user 
        mock (list[models], optional): If it has a value, the mockdata 
        will be used instead of generating new data. Defaults to None.

    Returns:
        JSON: medicine data in JSON format
    """    
    # make a JSON list for every category in medicine_models.common.Category
    data = {}
    for category in Category:
        data[category.value] = []

    models_fields = []

    if mock is None:
        # make a list containing all the fields from all the models
        for model in models:
            models_fields += model._meta.get_fields()
    else:
        models_fields = mock

    # for every field created with create_dashboard_column(), add it to the correct category in JSON
    for field in models_fields:
        if hasattr(field, "dashboard_column") and has_permission(perm, field.name):
            data_key = field.dashboard_column.get_data_key(field.name)
            if has_permission(perm, data_key):
                data[field.dashboard_column.category.value].append({
                    "data-key": data_key,
                    "data-format": field.dashboard_column.data_format,
                    "data-value": field.dashboard_column.data_value,
                })

    return data


# checks if user has permission to view a field
def has_permission(perm, name):
    """
    checks if user has permission to view a field

    Args:
        perm (list[attributes]): the permissions of the current user 
        name (string): the field name

    Returns:
        bool: true if the name is in the permissions
    """    
    return name in perm
