from django.contrib import admin
from import_export import resources, admin as import_admin
from api.models.medicine_models import (
    Medicine,
    Historyprime,
)
from .common import import_foreign_key
from .cachemodeladmin import CacheModelAdmin


class HistoryprimeResource(resources.ModelResource):
    """
    Resource for the Historyprime model.
    Has explicit foreign keys so Django import/export can automatically create the values if needed.
    """

    eunumber = import_foreign_key("eunumber", Medicine)

    class Meta:
        """
        Meta class for HistoryprimeResource
        """

        model = Historyprime
        import_id_fields = (
            "eunumber",
            "primedate",
        )


class HistoryprimeAdmin(import_admin.ImportExportModelAdmin, CacheModelAdmin):
    """
    Admin View for Historyprime
    """

    resource_class = HistoryprimeResource
    list = (
        "eunumber",
        "prime",
        "primedate",
    )


admin.site.register(Historyprime, HistoryprimeAdmin)
