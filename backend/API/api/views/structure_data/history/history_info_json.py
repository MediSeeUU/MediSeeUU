# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

from django.db.models import Model


def get_history_info(perm, models: list[Model]):
    data = []
    for model in models:
        if hasattr(model, "HistoryInfo") and has_permission(perm, model.HistoryInfo.timeline_name):
            data.append({
                "data-key": model.HistoryInfo.timeline_name,
                "data-format": model.HistoryInfo.data_format.data_format,
                "data-value": model.HistoryInfo.timeline_title,
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
