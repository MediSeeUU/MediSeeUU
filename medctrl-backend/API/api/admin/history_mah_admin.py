# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.contrib import admin
from import_export import resources, admin as import_admin
from api.models.medicine_models import (
    Medicine,
    HistoryMAH,
)
from api.admin.common import import_foreign_key
from api.admin.cachemodeladmin import CacheModelAdmin


class HistoryMAHResource(resources.ModelResource):
    """
    Necessary resource class for the HistoryMAH admin view.
    Has explicit foreign keys so Django import/export can automatically create the values if needed.
    ModelResource is Resource subclass for handling Django models.
    """
    eu_pnumber = import_foreign_key("eu_pnumber", Medicine)

    class Meta:
        """
        Meta class for HistoryMAHResource
        """
        model = HistoryMAH
        import_id_fields = (
            "eu_pnumber",
        )


class HistoryMAHAdmin(import_admin.ImportExportModelAdmin, CacheModelAdmin):
    """
    Admin View for HistoryMAH
    """
    resource_class = HistoryMAHResource
    list = (
        "id",
        "eu_pnumber",
        "change_date",
        "eu_mah",
    )


admin.site.register(HistoryMAH, HistoryMAHAdmin)
