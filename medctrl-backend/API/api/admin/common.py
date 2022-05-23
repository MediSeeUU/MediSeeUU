from django.contrib import admin
from import_export import fields, widgets, admin


def import_foreign_key(field, model):
    """
    Create a ForeignKey field for a given field and model.
    Can be used to automatically create foreign key fields for import if they don't exist already.

    :param field: The field to create a ForeignKey for
    :param model: The model to create a ForeignKey for
    """
    return fields.Field(
        column_name=field, attribute=field, widget=CustomForeignKeyWidget(model, field)
    )


class CustomForeignKeyWidget(widgets.ForeignKeyWidget):
    """
    Custom ForeignKeyWidget that creates a new object if it doesn't exist already.
    """

    def clean(self, value, row, *args, **kwargs):
        if value is not None:
            value, _ = self.model.objects.get_or_create(**{self.field: value})

        return value


admin.site.index_template = "adminIndex.html"
