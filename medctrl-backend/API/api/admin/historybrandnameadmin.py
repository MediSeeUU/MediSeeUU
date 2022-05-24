from django.contrib import admin
from import_export import resources, admin as import_admin
from api.models.medicine_models import (
    Medicine,
    Historybrandname,
)
from .common import import_foreign_key
from .cachemodeladmin import CacheModelAdmin


class HistorybrandnameResource(resources.ModelResource):
    """
    Resource for the Historybrandname model.
    Has explicit foreign keys so Django import/export can automatically create the values if needed.
    """

    eunumber = import_foreign_key("eunumber", Medicine)

    class Meta:
        """
        Meta class for HistorybrandnameResource
        """

        model = Historybrandname
        import_id_fields = (
            "eunumber",
            "brandnamedate",
        )


class HistorybrandnameAdmin(import_admin.ImportExportModelAdmin, CacheModelAdmin):
    """
    Admin View for Historybrandname
    """

    resource_class = HistorybrandnameResource
    list = (
        "eunumber",
        "brandname",
        "brandnamedate",
    )


admin.site.register(Historybrandname, HistorybrandnameAdmin)
