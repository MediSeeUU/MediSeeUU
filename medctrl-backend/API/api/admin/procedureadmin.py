# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.contrib import admin
from import_export import resources, admin as import_admin
from api.models.medicine_models import (
    Medicine,
    Procedure
)
from .common import import_foreign_key
from .cachemodeladmin import CacheModelAdmin


class ProcedureResource(resources.ModelResource):
    """
    Resource for the Procedure model.
    Has explicit foreign keys so Django import/export can automatically create the values if needed.
    """

    eunumber = import_foreign_key("eunumber", Medicine)

    class Meta:
        """
        Meta class for ProcedureResource
        """

        model = Procedure
        import_id_fields = ("commisionnumber")


class ProcedureAdmin(import_admin.ImportExportModelAdmin, CacheModelAdmin):
    """
    Admin View for Procedure
    """

    resource_class = ProcedureResource
    list = (
        "eunumber",
        "procedurecount",
        "commisionnumber",
        "emanumber",
        "proceduredate",
        "proceduretype",
        "decisiondate",
        "decisionnumber",
        "decisionurl",
        "annexurl",
    )

    def save_model(self, request, obj, form, change):
        # Get reference to the old procedure object
        proc = Procedure.objects.filter(commisionnumber=obj.commisionnumber).first()

        # Check if the manually updated checkbox has been unchecked
        if not proc.manually_updated:
            obj.manually_updated = True

        super().save_model(request, obj, form, change)


admin.site.register(Procedure, ProcedureAdmin)
