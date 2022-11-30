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
    General_Information = "General Information"
    Identifying_Information = "Identifying Information"
    Co_Rapporteur = "(Co-)Rapporteur"
    Medicine_Designations = "Medicine Designations"
    Legal_Information = "Legal Information"
    Authorisation_Timing = "Authorisation Timing"
    Additional_Resources = "Additional Resources"


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


class DashboardRelatedColumn(DashboardColumn):
    def __init__(self, category: Category, data_format: str, data_value: str, public_serializer, scraper_serializer):
        """
        Creates a DashboardColumn

        Args:
            category (Category): Category the variable should be shown in on the dashboard.
            data_format (str): Data format for the dashboard. Example: `link`.
            data_value (str): Title for the variable to be shown on the dashboard.
        """
        super().__init__(category, data_format, data_value)
        self.public_serializer = public_serializer
        self.scraper_serializer = scraper_serializer


class DashboardListColumn(DashboardRelatedColumn):
    pass


class DashBoardHistoryInitialColumn(DashboardRelatedColumn):
    pass


class DashBoardHistoryCurrentColumn(DashboardRelatedColumn):
    @staticmethod
    def get_data_key(field_name: str) -> str:
        return f"{field_name}_current"


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
    setattr(field, "dashboard_columns", [dashboard_column])
    return field


def create_dashboard_related_column(field: models.Field, category: Category, data_format: str,
                                    display_name: str, public_serializer, scraper_serializer) -> models.Field:
    """

    Args:
        field:
        category:
        data_format:
        display_name:
        public_serializer:
        scraper_serializer:

    Returns:

    """
    dashboard_column = DashboardRelatedColumn(category, data_format, display_name,
                                              public_serializer, scraper_serializer)
    setattr(field, "dashboard_columns", [dashboard_column])
    return field


def create_dashboard_list_column(field: models.Field, category: Category, data_format: str,
                                 display_name: str, public_serializer, scraper_serializer) -> models.Field:
    """

    Args:
        field:
        category:
        data_format:
        display_name:
        public_serializer:
        scraper_serializer:

    Returns:

    """
    dashboard_column = DashboardListColumn(category, data_format, display_name, public_serializer, scraper_serializer)
    setattr(field, "dashboard_columns", [dashboard_column])
    return field


def create_dashboard_history_initial_column(field: models.Field, category: Category, data_format: str,
                                            display_name: str, public_serializer, scraper_serializer) -> models.Field:
    """
    Creates the initial column for a Foreign Key to a history model.

    Args:
        field (models.Field): The type that the database attribute will have (CharField, BooleanField, etc.).
        category (Category): Which category the attribute should belong to.
        data_format (str): Defines what data format the attribute should have.
        display_name (str): This is the name that the attribute displays in the database.

    Returns:
        Field: Returns the original field, but updated with the correct information.
    """
    dashboard_column = DashBoardHistoryInitialColumn(category, data_format, display_name,
                                                     public_serializer, scraper_serializer)
    setattr(field, "dashboard_columns", [dashboard_column])
    return field


def create_dashboard_history_current_column(field: models.Field, category: Category, data_format: str,
                                            display_name: str, public_serializer, scraper_serializer) -> models.Field:
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
    dashboard_column = DashBoardHistoryCurrentColumn(category, data_format, display_name,
                                                     public_serializer, scraper_serializer)

    setattr(field, "dashboard_columns", [dashboard_column])
    return field
