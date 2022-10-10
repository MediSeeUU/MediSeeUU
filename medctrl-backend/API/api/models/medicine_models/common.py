# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from enum import Enum


class Category(Enum):
    """
    Defines the categories for a column on the dashboard data table
    """
    General_Information = "General Information"
    Identifying_Information = "Identifying Information"
    Co_Rapporteur = "(Co-)Rapporteur"
    Medicine_Designations = "Medicine Designations"
    Legal_Information = "Legal Information"
    Authorisation_Timing = "Authorisation Timing"
    Additional_Resources = "Additional Resources"


def create_dashboard_column(field, header: Category, data_format, display_name: str):
    """
    Sets attributes on a model field that's used in medicine_info_json
    """
    setattr(field, "category", header.value)
    setattr(field, "data_format", data_format)
    setattr(field, "data_value", display_name)
    return field
