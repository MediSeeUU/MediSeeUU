# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from enum import Enum
from typing import Callable, Tuple, Any
from .common import DataFormats


class Category(Enum):
    """
    Defines the categories for a column on the dashboard data table.
    It derives from the enumeration class.
    """
    Medicinal_product = "Medicinal product"
    Ingredients_and_substances = "Ingredients & substances"
    Marketing_authorisation = "Marketing authorisation"
    Procedures = "Procedures"
    Orphan_product = "Orphan Product"


class ExtraDashBoardColumn:
    def __init__(self, category: Category, data_key: str, data_format: DataFormats,
                 data_value: str, function: Callable[[str], Any]):
        """
        Creates an extra DashboardColumn

        Args:
            category (Category): Category the variable should be shown in on the dashboard.
            data_key (str):
            data_format (DataFormats): Data format for the dashboard. Example: `link`.
            data_value (str): Title for the variable to be shown on the dashboard.
            function (Callable[[str], Any]):
        """
        self.category = category
        self.data_key = data_key
        self.data_format = data_format
        self.data_value = data_value
        self.function = function


class DashboardColumn:
    """
    Holds values used in medicine_info_json to create a column in the dashboard.
    """

    def __init__(self, category: Category, data_format: DataFormats, data_value: str,
                 extra_dashboard_columns: list[ExtraDashBoardColumn] = None, data_key: str = None):
        """
        Creates a DashboardColumn

        Args:
            category (Category): Category the variable should be shown in on the dashboard.
            data_format (DataFormats): Data format for the dashboard. Example: `link`.
            data_value (str): Title for the variable to be shown on the dashboard.
        """
        self.category = category
        self.data_format = data_format
        self.data_value = data_value
        self.extra_dashboard_columns = extra_dashboard_columns
        self.data_key = data_key

    def get_data_key(self, field_name: str) -> str:
        if self.data_key:
            return self.data_key
        else:
            return field_name

    def get_all_data_info(self, field_name: str) -> list[Tuple[str, str, str]]:
        data_info = [(self.get_data_key(field_name), self.data_format.data_format, self.data_value)]
        if extra_dashboard_columns := self.extra_dashboard_columns:
            for extra_dashboard_column in extra_dashboard_columns:
                data_info.append((
                    extra_dashboard_column.data_key,
                    extra_dashboard_column.data_format.data_format,
                    extra_dashboard_column.data_value,
                ))
        return data_info


class DashBoardHistoryForeignKeyColumn(DashboardColumn):
    pass


def create_dashboard_column(field: models.Field, category: Category, data_format: DataFormats, display_name: str,
                            extra_dashboard_columns: list[ExtraDashBoardColumn] = None, data_key: str = None) \
        -> models.Field:
    """
    Sets attributes on a model field that's used in medicine_info_json.

    Args:
        field (models.Field): The type that the database attribute will have (CharField, BooleanField, etc.).
        category (Category): Which category the attribute should belong to.
        data_format (DataFormats): Defines what data format the attribute should have.
        display_name (str): This is the name that the attribute displays in the database.
        extra_dashboard_columns (list[ExtraDashboardColumn]):

    Returns:
        Field: Returns the original field, but updated with the correct information.
    """
    dashboard_column = DashboardColumn(category, data_format, display_name, extra_dashboard_columns, data_key)
    setattr(field, "dashboard_column", dashboard_column)
    return field


def create_dashboard_history_foreign_key_column(field: models.Field, category: Category,
                                                data_format: DataFormats, display_name: str,
                                                extra_dashboard_columns: list[ExtraDashBoardColumn] = None,
                                                data_key: str = None) -> models.Field:
    """
    Sets attributes on a model field that's used in medicine_info_json.

    Args:
        field (models.Field): The type that the database attribute will have (CharField, BooleanField, etc.).
        category (Category): Which category the attribute should belong to.
        data_format (DataFormats): Defines what data format the attribute should have.
        display_name (str): This is the name that the attribute displays in the database.
        extra_dashboard_columns (list[ExtraDashBoardColumn):

    Returns:
        Field: Returns the original field, but updated with the correct information.
    """
    dashboard_column = DashBoardHistoryForeignKeyColumn(category, data_format, display_name,
                                                        extra_dashboard_columns, data_key)
    setattr(field, "dashboard_column", dashboard_column)
    return field
