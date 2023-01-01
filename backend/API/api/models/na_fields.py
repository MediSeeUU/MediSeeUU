from django import forms
from django.db import models
from django.core.exceptions import ValidationError
import datetime
import validators
from api.models.common import DataFormats


class BooleanWithNAField(models.Field):

    values = ["True", "False"] + DataFormats.Bool.na_values

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
        elif value is None or value == "":
            return None
        elif value in self.values:
            return value
        else:
            raise ValidationError(f"{self.name}: {value} must be either a boolean or a NA message")

    def formfield(self, **kwargs):
        defaults = {'form_class': self.FormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)

    class FormField(forms.ChoiceField):
        def __init__(self, **kwargs):
            super().__init__(
                widget=forms.Select,
                choices=[("", "----")] + [(value, value) for value in BooleanWithNAField.values],
                **kwargs
            )


class TypeWithNAWidget(forms.MultiWidget):
    def __init__(self, value_check, first_widget, second_widget, na_values, **kwargs):
        self.value_check = value_check
        super().__init__(
            widgets=[
                        first_widget(
                            attrs={"oninput": "{if (this.value) {this.nextSibling.value = \"\"}}"},
                        ),
                        second_widget(
                            attrs={
                                "onfocus": "{this.firstChild.hidden = true}",
                                "oninput": "{if (this.value) {this.previousSibling.value = \"\"}}",
                            },
                            choices=[(value, value) for value in [""] + na_values],
                        ),
                    ],
            **kwargs
        )

    def decompress(self, value):
        if self.value_check(value):
            return [value, None]
        else:
            return [None, value]

    def value_from_datadict(self, data, files, name):
        value, na_value = super().value_from_datadict(data, files, name)
        if value is not None and value != "":
            return value
        else:
            return na_value


class IntegerWithNAField(models.Field):

    values = DataFormats.Number.na_values

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
        elif value is None or str.isdigit(value) or value in self.values:
            return value
        else:
            raise ValidationError(f"{self.name}: {value} must be either a integer or a NA message")

    def formfield(self, **kwargs):
        defaults = {'form_class': self.FormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)

    class FormField(forms.Field):
        def __init__(self, **kwargs):
            super().__init__(
                widget=TypeWithNAWidget(
                    lambda value: isinstance(value, int) or value.isdigit(),
                    forms.NumberInput,
                    forms.Select,
                    IntegerWithNAField.values,
                ),
                **kwargs
            )


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
        except TypeError:
            raise ValidationError(f"{self.name}: {value} must be a string containing a date or a NA message")
        else:
            return value



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

