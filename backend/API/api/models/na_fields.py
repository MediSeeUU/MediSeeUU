from django import forms
from django.contrib.admin import widgets
from django.db import models
from django.core.exceptions import ValidationError
import datetime
import validators
from api.models.common import DataFormats


class BooleanWithNAField(models.Field):
    def __init__(self, *args, **kwargs):
        self.values = ["True", "False"] + DataFormats.Bool.na_values
        if "extra_na_values" in kwargs:
            self.values += kwargs["extra_na_values"]
            del kwargs["extra_na_values"]
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

    def from_db_value(self, value, *_):
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
        setattr(self.FormField, "values", self.values)
        defaults = {'form_class': self.FormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)

    class FormField(forms.ChoiceField):
        def __init__(self, **kwargs):
            super().__init__(
                widget=forms.Select,
                choices=[("", "----")] + [(value, value) for value in getattr(self, "values")],
                **kwargs
            )


class TypeWithNAWidget(forms.MultiWidget):
    def __init__(self, na_values, **kwargs):
        self.na_values = na_values
        super().__init__(**kwargs)

    def decompress(self, value):
        if value in self.na_values:
            return [None, value]
        else:
            return [value, None]

    def value_from_datadict(self, data, files, name):
        value, na_value = super().value_from_datadict(data, files, name)
        if value is not None and value != "":
            return value
        else:
            return na_value


class IntegerWithNAField(models.Field):
    def __init__(self, *args, **kwargs):
        self.values = DataFormats.Number.na_values
        if "extra_na_values" in kwargs:
            self.values += kwargs["extra_na_values"]
            del kwargs["extra_na_values"]
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

    def from_db_value(self, value, *_):
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
        setattr(self.FormField, "values", self.values)
        defaults = {'form_class': self.FormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)

    class FormField(forms.Field):
        def __init__(self, **kwargs):
            super().__init__(
                widget=TypeWithNAWidget(
                    getattr(self, "values"),
                    widgets=[
                        forms.NumberInput(
                            attrs={"oninput": "{if (this.value) {this.nextSibling.value = \"\"}}"},
                        ),
                        forms.Select(
                            attrs={
                                "onfocus": "{this.firstChild.hidden = true}",
                                "oninput": "{if (this.value) {this.previousSibling.value = \"\"}}",
                            },
                            choices=[(value, value) for value in [""] + getattr(self, "values")],
                        ),
                    ],
                ),
                **kwargs
            )


class DateWithNAField(models.Field):
    def __init__(self, *args, **kwargs):
        self.values = DataFormats.Date.na_values
        if "extra_na_values" in kwargs:
            self.values += kwargs["extra_na_values"]
            del kwargs["extra_na_values"]
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
        if value is None or value in self.values:
            return value
        try:
            datetime.datetime.strptime(value, '%Y-%m-%d')
        except ValueError as e:
            raise ValidationError(f"{self.name}: {value} has failed to be converted to a date with exception: "
                                  f"\"{str(e)}\". {self.name} must be either a date or a NA message")
        except TypeError:
            raise ValidationError(f"{self.name}: {value} must be a string containing a date or a NA message")
        else:
            return value

    def formfield(self, **kwargs):
        setattr(self.FormField, "values", self.values)
        defaults = {'form_class': self.FormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)

    class FormField(forms.Field):
        def __init__(self, **kwargs):
            super().__init__(
                widget=TypeWithNAWidget(
                    getattr(self, "values"),
                    widgets=[
                        widgets.AdminDateWidget(
                            attrs={
                                "onfocus": "{if (this.value) {this.nextSibling.nextSibling.value = \"\"}}",
                                "oninput": "{if (this.value) {this.nextSibling.nextSibling.value = \"\"}}",
                            },
                        ),
                        forms.Select(
                            attrs={
                                "onfocus": "{this.firstChild.hidden = true}",
                                "oninput": "{if (this.value) {this.previousSibling.previousSibling.value = \"\"}}",
                            },
                            choices=[(value, value) for value in [""] + getattr(self, "values")],
                        ),
                    ],
                ),
                **kwargs
            )


class URLWithNAField(models.Field):
    def __init__(self, *args, **kwargs):
        self.values = DataFormats.Link.na_values
        if "extra_na_values" in kwargs:
            self.values += kwargs["extra_na_values"]
            del kwargs["extra_na_values"]
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
        if value is None or value in self.values:
            return value
        elif validators.url(value):
            return value
        else:
            raise ValidationError(f"{self.name}: {value} must be either an url or a NA message")

    def formfield(self, **kwargs):
        setattr(self.FormField, "values", self.values)
        defaults = {'form_class': self.FormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)

    class FormField(forms.Field):
        def __init__(self, **kwargs):
            super().__init__(
                widget=TypeWithNAWidget(
                    getattr(self, "values"),
                    widgets=[
                        forms.URLInput(
                            attrs={"oninput": "{if (this.value) {this.nextSibling.value = \"\"}}"},
                        ),
                        forms.Select(
                            attrs={
                                "onfocus": "{this.firstChild.hidden = true}",
                                "oninput": "{if (this.value) {this.previousSibling.value = \"\"}}",
                            },
                            choices=[(value, value) for value in [""] + getattr(self, "values")],
                        ),
                    ],
                ),
                **kwargs
            )
