# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

from django.db.models import Model


def get_history_info(perm, models: list[Model]):
    data = []

    for model in models:
        for field in model._meta.get_fields():
            if hasattr(field, "history_dashboard_column") and has_permission(perm, field.name):
                data_info = field.history_dashboard_column.get_all_data_info(field.name)
                for data_key, data_format, data_value in data_info:
                    if has_permission(perm, data_key):
                        data.append({
                            "data-key": data_key,
                            "data-format": data_format,
                            "data-value": data_value,
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
