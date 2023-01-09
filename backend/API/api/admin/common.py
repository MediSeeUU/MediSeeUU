# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.contrib import admin
from import_export import fields, widgets


def import_foreign_key(field, model):
    """
    Create a ForeignKey field for a given field and model.
    Can be used to automatically create foreign key fields for import if they do not exist already.

    Args:
        field (Any): The field to create the ForeignKey for.
        model (Any): The model to create the ForeignKey for.

    Returns:
        fields.Field: Returns a field with the added ForeignKey.
    """    
    return fields.Field(
        column_name=field, attribute=field, widget=CustomForeignKeyWidget(model, field)
    )


class CustomForeignKeyWidget(widgets.ForeignKeyWidget):
    """
    This is a Custom ForeignKeyWidget that creates a new object if it does not exist already.
    """
    def clean(self, value, row, *args, **kwargs):
        if value is not None:
            value, _ = self.model.objects.get_or_create(**{self.field: value})

        return value


admin.site.index_template = "adminIndex.html"
