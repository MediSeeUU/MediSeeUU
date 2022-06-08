# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.contrib import admin
from import_export import resources, admin as import_admin
from api.models.medicine_models import (
    Medicine,
    Procedure,
    Lookupproceduretype,
)
from .common import import_foreign_key
from .cachemodeladmin import CacheModelAdmin


class ProcedureResource(resources.ModelResource):
    """
    Resource for the Procedure model.
    Has explicit foreign keys so Django import/export can automatically create the values if needed.
    """

    eunumber = import_foreign_key("eunumber", Medicine)
    proceduretype = import_foreign_key("proceduretype", Lookupproceduretype)

    class Meta:
        """
        Meta class for ProcedureResource
        """

        model = Procedure
        import_id_fields = ("commisionnumber",)


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


admin.site.register(Procedure, ProcedureAdmin)
