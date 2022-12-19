# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

from django.db import models
from django.core.exceptions import ValidationError


class BooleanWithNAField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs["choices"] = BooleanChoices.choices
        kwargs["max_length"] = 32
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["choices"]
        del kwargs["max_length"]
        return name, path, args, kwargs


class IntegerWithNAField(models.TextField):
    def from_db_value(self, value, expression, connection):
        if value is None or not str.isdigit(value):
            return value
        else:
            return int(value)

    def get_prep_value(self, value):
        if isinstance(value, int):
            return str(value)
        elif str.isdigit(value) or value in ["Not found", "Not available at release"]:
            return value
        else:
            raise ValidationError(f"{value} must be either a integer or a NA message")


class BooleanChoices(models.TextChoices):
    TRUE = "True",
    FALSE = "False",
    NotFound = "Not found",
    NotAvailableAtRelease = "Not available at release",
    ExpectedButUnableToExtract = "Expected, but unable to extract",


class AutTypes(models.TextChoices):
    """
    Choice types for eu_aut_type. Is derived from the enumerated choice class.
    """    
    CONDITIONAL = "CONDITIONAL",
    EXCEPTIONAL = "EXCEPTIONAL",
    STANDARD = "STANDARD"
    UNCERTAIN = "EXCEPTIONAL OR CONDITIONAL"


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
