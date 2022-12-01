from django.db import models
from api.models.create_dashboard_columns import DashBoardHistoryInitialColumn


def get_all_initial_history_columns(model_list: list[models.Model]) -> list[str]:
    """

    Args:
        model_list:

    Returns:

    """
    result = []
    for model in model_list:
        for field in model._meta.get_fields():
            if hasattr(field, "dashboard_columns"):
                for dashboard_column in field.dashboard_columns:
                    if isinstance(dashboard_column, DashBoardHistoryInitialColumn):
                        result.append(field.name)
    return result
