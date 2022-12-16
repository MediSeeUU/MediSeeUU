# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from enum import Enum


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


class DashboardColumn:
    """
    Holds values used in medicine_info_json to create a column in the dashboard.
    """

    def __init__(self, category: Category, data_format: str, data_value: str):
        """
        Creates a DashboardColumn

        Args:
            category (Category): Category the variable should be shown in on the dashboard.
            data_format (str): Data format for the dashboard. Example: `link`.
            data_value (str): Title for the variable to be shown on the dashboard.
        """
        self.category = category
        self.data_format = data_format
        self.data_value = data_value

    @staticmethod
    def get_data_key(field_name: str) -> str:
        return field_name


class DashBoardHistoryInitialColumn(DashboardColumn):
    pass


class DashBoardHistoryCurrentColumn(DashboardColumn):
    def __init__(self, category: Category, data_format: str, data_value: str, suffix: str = "_current"):
        super().__init__(category, data_format, data_value)
        self.suffix = suffix

    def get_data_key(self, field_name: str) -> str:
        return f"{field_name}{self.suffix}"


def create_dashboard_column(field: models.Field, category: Category, data_format: str,
                            display_name: str) -> models.Field:
    """
    Sets attributes on a model field that's used in medicine_info_json.

    Args:
        field (models.Field): The type that the database attribute will have (CharField, BooleanField, etc.).
        category (Category): Which category the attribute should belong to.
        data_format (str): Defines what data format the attribute should have.
        display_name (str): This is the name that the attribute displays in the database.

    Returns:
        Field: Returns the original field, but updated with the correct information.
    """
    dashboard_column = DashboardColumn(category, data_format, display_name)
    setattr(field, "dashboard_column", dashboard_column)
    return field


def create_dashboard_history_initial_column(field: models.Field, category: Category, data_format: str,
                                            display_name: str) -> models.Field:
    """
    Sets attributes on a model field that's used in medicine_info_json.

    Args:
        field (models.Field): The type that the database attribute will have (CharField, BooleanField, etc.).
        category (Category): Which category the attribute should belong to.
        data_format (str): Defines what data format the attribute should have.
        display_name (str): This is the name that the attribute displays in the database.

    Returns:
        Field: Returns the original field, but updated with the correct information.
    """
    dashboard_column = DashBoardHistoryInitialColumn(category, data_format, display_name)
    setattr(field, "dashboard_column", dashboard_column)
    return field


def create_dashboard_history_current_column(field: models.Field, category: Category,
                                            data_format: str, display_name: str) -> models.Field:
    """
    Creates the current column for a history column in a history model.

    Args:
        field (models.Field): The type that the database attribute will have (CharField, BooleanField, etc.).
        category (Category): Which category the attribute should belong to.
        data_format (str): Defines what data format the attribute should have.
        display_name (str): This is the name that the attribute displays in the database.

    Returns:
        Field: Returns the original field, but updated with the correct information.
    """
    dashboard_column = DashBoardHistoryCurrentColumn(category, data_format, display_name)

    setattr(field, "dashboard_column", dashboard_column)
    return field
