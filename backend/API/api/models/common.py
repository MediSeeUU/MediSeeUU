# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

from django.db import models
from django.core.exceptions import ValidationError
import datetime
import validators

na_values = [
    "Not found",
    "Not available at time of document publication",
    "Value should be present in document",
    ""
]


class BooleanWithNAField(models.Field):
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 32
        # Set the field to support null values
        kwargs["null"] = True
        kwargs["blank"] = True
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        del kwargs["null"]
        del kwargs["blank"]
        return name, path, args, kwargs

    def db_type(self, connection):
        return f"VARCHAR({self.max_length})"

    def from_db_value(self, value, expression, connection):
        if value == "True":
            return True
        elif value == "False":
            return False
        return value

    def to_python(self, value):
        if value == "True":
            return True
        elif value == "False":
            return False
        return value

    def get_prep_value(self, value):
        bool_na_values = ["True", "False"] + na_values
        if isinstance(value, bool):
            return str(value)
        elif value is None or value in bool_na_values:
            return value
        else:
            raise ValidationError(f"{self.name}: {value} must be either a boolean or a NA message")


class IntegerWithNAField(models.Field):
    def __init__(self, *args, **kwargs):
        # Set the field to support null values
        kwargs["null"] = True
        kwargs["blank"] = True
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["null"]
        del kwargs["blank"]
        return name, path, args, kwargs

    def db_type(self, connection):
        return "LONGTEXT"

    def from_db_value(self, value, expression, connection):
        if value is None or not str.isdigit(value):
            return value
        else:
            return int(value)

    def to_python(self, value):
        if value == "True":
            return True
        elif value == "False":
            return False
        return value

    def get_prep_value(self, value):
        if isinstance(value, int):
            return str(value)
        elif value is None or str.isdigit(value) or value in na_values:
            return value
        else:
            raise ValidationError(f"{self.name}: {value} must be either a integer or a NA message")


class DateWithNAField(models.Field):
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 32
        # Set the field to support null values
        kwargs["null"] = True
        kwargs["blank"] = True
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        del kwargs["null"]
        del kwargs["blank"]
        return name, path, args, kwargs

    def db_type(self, connection):
        return f"VARCHAR({self.max_length})"

    def get_prep_value(self, value):
        date = datetime.datetime.strptime(value, '%Y-%m-%d')
        date_na_values = na_values + ["date is left blank in document"]
        # check if valid date
        if date.year >= 0 and date.month <= 12 and date.day <= 31:
            return value
        elif value is None or value in date_na_values:
            return value
        else:
            raise ValidationError(f"{self.name}: {value} must be either a date or a NA message")


class URLWithNAField(models.Field):
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 256
        # Set the field to support null values
        kwargs["null"] = True
        kwargs["blank"] = True
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        del kwargs["null"]
        del kwargs["blank"]
        return name, path, args, kwargs

    def db_type(self, connection):
        return f"VARCHAR({self.max_length})"

    def get_prep_value(self, value):
        if value is None or value in na_values:
            return value
        elif validators.url(value):
            return value
        else:
            raise ValidationError(f"{self.name}: {value} must be either an url or a NA message")


class AutTypes(models.TextChoices):
    """
    Choice types for eu_aut_type. Is derived from the enumerated choice class.
    """
    CONDITIONAL = "conditional",
    EXCEPTIONAL = "exceptional",
    STANDARD = "standard"
    UNCERTAIN = "exceptional or conditional"


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
    article4_8 = "article 4.8",
    article4_8_1 = "article 4.8.1",
    article4_8_2 = "article 4.8.2",
    article4_8_3 = "article 4.8.3",
    article8_3 = "article 8.3"
    article_10_1 = "article 10.1"
    article_10_2 = "article 10.2"
    article_10_3 = "article 10.3"
    article_10_4 = "article 10.4"
    article_10_a = "article 10.a"
    article_10_b = "article 10.b"
    article_10_c = "article 10.c"
