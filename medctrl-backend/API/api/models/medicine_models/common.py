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


class NotVarCharField(models.CharField):
    """
    Special fieldtype that enforces CHAR instead of VARCHAR
    """

    def db_type(self, connection):
        varchar: str = super().db_type(connection)
        char: str = varchar.replace('varchar', 'char')
        return char


"""
Series of choice fields for certain categorical attributes
"""


class AutTypes(models.TextChoices):
    """
    Choice types for eu_aut_type
    """
    CONDITIONAL = "CONDITIONAL",
    EXCEPTIONAL = "EXCEPTIONAL",
    STANDARD = "STANDARD"


class AutStatus(models.TextChoices):
    """
    Choice types for eu_aut_status
    """
    ACTIVE = "ACTIVE",
    WITHDRAWAL = "WITHDRAWAL",
    REFUSALS = "REFUSALS"


class LegalBases(models.TextChoices):
    """
    Choice types for eu_legal_basis
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


def create_dashboard_column(field, header: Category, data_format, display_name: str):
    """
    Sets attributes on a model field that's used in medicine_info_json
    """
    setattr(field, "category", header)
    setattr(field, "data_format", data_format)
    setattr(field, "data_value", display_name)
    return field
