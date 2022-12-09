# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.contrib import admin
from import_export import resources, admin as import_admin
from api.models.human_models import (
    MedicinalProduct,
    HistoryOD,
)
from api.admin.common import import_foreign_key
from api.admin.cachemodeladmin import CacheModelAdmin


class HistoryODResource(resources.ModelResource):
    """
    Necessary resource class for the HistoryOD admin view.
    Has explicit foreign keys so Django import/export can automatically create the values if needed.
    ModelResource is Resource subclass for handling Django models.
    """
    eu_pnumber = import_foreign_key("eu_pnumber", MedicinalProduct)

    class Meta:
        """
        Meta class for HistoryODResource
        """
        model = HistoryOD
        import_id_fields = (
            "eu_pnumber",
        )


class HistoryODAdmin(import_admin.ImportExportModelAdmin, CacheModelAdmin):
    """
    Admin View for HistoryOD
    """
    resource_class = HistoryODResource
    list = (
        "id",
        "eu_pnumber",
        "change_date",
        "eu_od",
    )


admin.site.register(HistoryOD, HistoryODAdmin)
