# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

from api.models import models
from api.models.create_dashboard_columns import Category


def get_history_info(perm, categories: list[Category]):
    data = []
    for model in models:
        if hasattr(model, "HistoryInfo") and hasattr(model.HistoryInfo, "timeline_items"):
            for timeline_item in model.HistoryInfo.timeline_items:
                if timeline_item["category"] in categories and has_permission(perm, timeline_item["data-key"]):
                    data.append({
                        "data-key": timeline_item["data-key"],
                        "data-format": timeline_item["data-format"].data_format,
                        "data-value": timeline_item["data-value"],
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
