from django.db import models
from django.core.exceptions import ValidationError
import datetime
import validators
from api.models.common import DataFormats


class BooleanWithNAField(models.Field):
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 45
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

    def get_prep_value(self, value):
        if isinstance(value, bool):
            return str(value)
        elif value is None or value in ["True", "False"] or value in DataFormats.Bool.na_values:
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

    def get_prep_value(self, value):
        if isinstance(value, int):
            return str(value)
        elif value is None or str.isdigit(value) or value in DataFormats.Number.na_values:
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
        if value is None or value in DataFormats.Date.na_values:
            return value
        try:
            date = datetime.datetime.strptime(value, '%Y-%m-%d')
        except ValueError as e:
            raise ValidationError(f"{self.name}: {value} has failed to be converted to a date with exception: "
                                  f"\"{str(e)}\". {self.name} must be either a date or a NA message")
        else:
            # check if valid date
            if date.year >= 0 and date.month <= 12 and date.day <= 31:
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
        if value is None or value in DataFormats.Link.na_values:
            return value
        elif validators.url(value):
            return value
        else:
            raise ValidationError(f"{self.name}: {value} must be either an url or a NA message")

