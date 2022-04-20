# from django.contrib import admin

# Register your models here.

from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.contrib import admin
from .models.medicine_models.medicine import Medicine


class MedicineResource(resources.ModelResource):
    class Meta:
        model = Medicine
        import_id_fields = ("eunumber",)


class MedicineAdmin(ImportExportModelAdmin, admin.ModelAdmin):
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
