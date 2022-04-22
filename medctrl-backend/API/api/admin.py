# from django.contrib import admin

# Register your models here.

from django.contrib import admin
from import_export import fields, resources, widgets, admin as import_admin

from api.models.medicine_models.medicine import Medicine, Lookupatccode
from api.models.medicine_models import (
    Lookuplegalbasis,
    Lookuplegalscope,
    Lookupmedicinetype,
    Lookupstatus,
    Lookupactivesubstance,
)


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


class MedicineResource(resources.ModelResource):
    """
    Resource for the Medicine model.
    Has explicit foreign keys so Django import/export can automatically create the values if needed.
    """

    atccode = import_foreign_key("atccode", Lookupatccode)
    legalbasis = import_foreign_key("legalbasis", Lookuplegalbasis)
    legalscope = import_foreign_key("legalscope", Lookuplegalscope)
    medicinetype = import_foreign_key("medicinetype", Lookupmedicinetype)
    status = import_foreign_key("status", Lookupstatus)
    activesubstance = import_foreign_key("activesubstance", Lookupactivesubstance)

    class Meta:
        """
        Meta class for MedicineResource
        """

        model = Medicine
        import_id_fields = ("eunumber",)


class MedicineAdmin(import_admin.ImportExportModelAdmin, admin.ModelAdmin):
    """
    Admin View for Medicine
    """

    resource_class = MedicineResource
    list = (
        "eu_nr",
        "ema_nr",
        "legal_basis",
        "legal_scope",
        "atc_code",
        "prime",
        "orphan",
        "atmp",
        "ema_url",
    )


admin.site.register(Medicine, MedicineAdmin)
