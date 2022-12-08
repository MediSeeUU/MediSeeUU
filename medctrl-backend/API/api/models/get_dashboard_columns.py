from django.db import models
from api.models.create_dashboard_columns import DashBoardHistoryInitialColumn, DashBoardHistoryCurrentColumn


def get_initial_history_columns(model_list: list[models.Model]) -> list[str]:
    """

    Args:
        model_list:

    Returns:

    """
    result = []
    for model in model_list:
        for field in model._meta.get_fields():
            if hasattr(field, "dashboard_column"):
                for dashboard_column in field.dashboard_columns:
                    if isinstance(dashboard_column, DashBoardHistoryInitialColumn):
                        result.append(field.name)
    return result


def get_data_key(model: models.Model, field_name: str) -> str:
    for field in model._meta.get_fields():
        if field.name == field_name and hasattr(field, "dashboard_column"):
            return field.dashboard_column.get_data_key(field.name)
