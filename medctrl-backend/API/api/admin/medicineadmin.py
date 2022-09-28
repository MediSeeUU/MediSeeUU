# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.contrib import admin
from import_export import resources, admin as import_admin
from api.models.medicine_models import Medicine
from .common import import_foreign_key
from .cachemodeladmin import CacheModelAdmin


class MedicineResource(resources.ModelResource):
    """
    Resource for the Medicine model.
    Has explicit foreign keys so Django import/export can automatically create the values if needed.
    """

    atccode = import_foreign_key("atccode", Medicine)
    legalbasis = import_foreign_key("legalbasis", Medicine)
    legalscope = import_foreign_key("legalscope", Medicine)
    medicinetype = import_foreign_key("medicinetype", Medicine)
    status = import_foreign_key("status", Medicine)
    activesubstance = import_foreign_key("activesubstance", Medicine)

    class Meta:
        """
        Meta class for MedicineResource
        """

        model = Medicine
        import_id_fields = ("eunumber",)


class MedicineAdmin(import_admin.ImportExportModelAdmin, CacheModelAdmin):
    """
    Admin View for Medicine
    """

    resource_class = MedicineResource
    list = (
        "eunumber",
        "emanumber",
        "atccode",
        "activesubstance",
        "newactivesubstance",
        "legalbasis",
        "legalscope",
        "atmp",
        "status",
        "referral",
        "suspension",
        "emaurl",
        "ecurl",
    )

    def save_model(self, request, obj, form, change):
        # Get reference to previous object
        med = Medicine.objects.filter(eunumber=obj.eunumber).first()

        # Check if the manually updated checkbox has been unchecked
        if not med.manually_updated:
            obj.manually_updated = True
        super().save_model(request, obj, form, change)


admin.site.register(Medicine, MedicineAdmin)
