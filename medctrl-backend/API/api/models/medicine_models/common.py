# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from dataclasses import Field
from enum import Enum
from django.db import models


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
    NieuweCategorie = "Nieuwe Categorie"


class NotVarCharField(models.CharField):
    """
    Special field type that enforces CHAR instead of VARCHAR
    It derives from the Django CharField.
    """    
    def db_type(self, connection):
        """
        db_type returns the database field type for the given connection. 
        This function specifically returns CHAR instead of VARCHAR.

        Args:
            connection (_type_): Connection with the database.

        Returns:
            str: It returns the column data type for the given connection as string,
            but it will return 'char' if it would be a 'varchar'.
        """        
        varchar: str = super().db_type(connection)
        char: str = varchar.replace('varchar', 'char')
        return char


class AutTypes(models.TextChoices):
    """
    Choice types for eu_aut_type. Is derived from the enumerated choice class.
    """    
    CONDITIONAL = "CONDITIONAL",
    EXCEPTIONAL = "EXCEPTIONAL",
    STANDARD = "STANDARD"


class AutStatus(models.TextChoices):
    """
    Choice types for eu_aut_status. Is derived from the enumerated choice class.
    """   
    ACTIVE = "ACTIVE",
    WITHDRAWAL = "WITHDRAWN",
    REFUSALS = "REFUSED"


class LegalBasesTypes(models.TextChoices):
    """
    Choice types for legal bases. Is derived from the enumerated choice class.
    """
    article48 = "article 4.8",
    article4_8 = "article 4(8)"
    article48_1 = "article 4.8(1)",
    article48_2 = "article 4.8(2)",
    article48_3 = "article 4.8(3)",
    article83 = "article 8.3",
    article8_3 = "article 8(3)",
    article101 = "article 10.1",
    article10_1 = "article 10(1)",
    article102 = "article 10.2",
    article10_2 = "article 10(2)",
    article103 = "article 10.3",
    article10_3 = "article 10(3)",
    article104 = "article 10.4",
    article10_4 = "article 10(4)",
    article10a = "article 10a",
    article10_a = "article 10(a)",
    article10b = "article 10b",
    article10_b = "article 10(b)",
    article10c = "article 10c",
    article10_c = "article 10(c)"


class DashboardColumn:
    """
    Holds values used in medicine_info_json to create a column in the dashboard.
    """
    def __init__(self, category, data_key, data_format, data_value):
        self.category = category
        self.data_key = data_key
        self.data_format = data_format
        self.data_value = data_value


def create_dashboard_column(field: Field, category: Category, data_format: str, display_name: str):
    """
    Sets attributes on a model field that's used in medicine_info_json.

    Args:
        field (Field): The type that the database attribute will have (CharField, BooleanField, etc.).
        category (Category): Which category the attribute should belong to.
        data_format (str): Defines what data format the attribute should have.
        display_name (str): This is the name that the attribute displays in the database.

    Returns:
        Field: Returns the original field, but updated with the correct information.
    """    
    dashboard_column = DashboardColumn(category, field.db_column, data_format, display_name)
    setattr(field, "dashboard_columns", [dashboard_column])
    return field

def create_dashboard_history_columns(field: Field, category: Category, data_format: str, display_name: str):
    """
    Creates two dashboard columns out of a single model column, an initial and a current one for histories.

    Args:
        field (Field): The type that the database attribute will have (CharField, BooleanField, etc.).
        category (Category): Which category the attribute should belong to.
        data_format (str): Defines what data format the attribute should have.
        display_name (str): This is the name that the attribute displays in the database.

    Returns:
        Field: Returns the original field, but updated with the correct information.
    """    
    initial_dashboard_column = DashboardColumn(
        category,
        field.db_column + "_initial",
        data_format,
        "Initial " + display_name
    )

    current_dashboard_column = DashboardColumn(
        category,
        field.db_column + "_current",
        data_format,
        "Current " + display_name
    )
    setattr(field, "dashboard_columns", [initial_dashboard_column, current_dashboard_column])
    return field


def create_dashboard_history_column_initial(field: Field, category: Category, data_format: str, display_name: str):
    """
    Creates the initial column for a history column.

    Args:
        field (Field): The type that the database attribute will have (CharField, BooleanField, etc.).
        category (Category): Which category the attribute should belong to.
        data_format (str): Defines what data format the attribute should have.
        display_name (str): This is the name that the attribute displays in the database.

    Returns:
        Field: Returns the original field, but updated with the correct information.
    """    
    initial_dashboard_column = DashboardColumn(
        category,
        field.db_column + "_initial",
        data_format,
        "Initial " + display_name
    )
    setattr(field, "dashboard_columns", [initial_dashboard_column])
    return field


def create_dashboard_history_column_current(field: Field, category: Category, data_format: str, display_name: str):
    """
    Creates the current column for a history column.

    Args:
        field (Field): The type that the database attribute will have (CharField, BooleanField, etc.).
        category (Category): Which category the attribute should belong to.
        data_format (str): Defines what data format the attribute should have.
        display_name (str): This is the name that the attribute displays in the database.

    Returns:
        Field: Returns the original field, but updated with the correct information.
    """   
    current_dashboard_column = DashboardColumn(
        category,
        field.db_column + "_current",
        data_format,
        "Current " + display_name
    )
    setattr(field, "dashboard_columns", [current_dashboard_column])
    return field
