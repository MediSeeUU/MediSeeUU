from django.db import models
from api.models.create_dashboard_columns import DashBoardHistoryInitialColumn


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
                if isinstance(field.dashboard_column, DashBoardHistoryInitialColumn):
                    result.append(field.name)
    return result


def get_data_key(model: models.Model, field_name: str) -> str:
    for field in model._meta.get_fields():
        if field.name == field_name and hasattr(field, "dashboard_column"):
            return field.dashboard_column.get_data_key(field.name)


def insert_extra_dashboard_columns(data, models):
    for medicine in data:
        for model in models:
            for field in model._meta.get_fields():
                if hasattr(field, "dashboard_column"):
                    data_key = field.dashboard_column.get_data_key(field.name)
                    if data_key in medicine and medicine[data_key] is not None \
                            and medicine[data_key] not in field.dashboard_column.data_format.na_values:
                        if extra_dashboard_columns := field.dashboard_column.extra_dashboard_columns:
                            for extra_dashboard_column in extra_dashboard_columns:
                                medicine[extra_dashboard_column.data_key] = \
                                    extra_dashboard_column.function(medicine[data_key])
    return data
