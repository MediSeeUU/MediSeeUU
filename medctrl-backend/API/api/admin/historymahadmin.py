# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.contrib import admin
from import_export import resources, admin as import_admin
from api.models.medicine_models import (
    Medicine,
    Historymah,
)
from api.admin.common import import_foreign_key
from api.admin.cachemodeladmin import CacheModelAdmin


class HistorymahResource(resources.ModelResource):
    """
    Resource for the Historymah model.
    Has explicit foreign keys so Django import/export can automatically create the values if needed.
    """

    eunumber = import_foreign_key("eunumber", Medicine)

    class Meta:
        """
        Meta class for HistorymahResource
        """

        model = Historymah
        import_id_fields = (
            "eunumber",
            "mahdate",
        )


class HistorymahAdmin(import_admin.ImportExportModelAdmin, CacheModelAdmin):
    """
    Admin View for Historymah
    """

    resource_class = HistorymahResource
    list = (
        "eunumber",
        "mah",
        "mahdate",
    )


admin.site.register(Historymah, HistorymahAdmin)
