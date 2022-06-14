# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.contrib import admin
from import_export import resources, admin as import_admin
from api.models.medicine_models import (
    Medicine,
    Lookupatccode,
    Lookuplegalbasis,
    Lookuplegalscope,
    Lookupmedicinetype,
    Lookupstatus,
    Lookupactivesubstance,
)
from .common import import_foreign_key
from .cachemodeladmin import CacheModelAdmin


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
