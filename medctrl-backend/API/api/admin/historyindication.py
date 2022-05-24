from django.contrib import admin
from import_export import resources, admin as import_admin
from api.models.medicine_models import (
    Medicine,
    Historyindication,
)
from .common import import_foreign_key
from .cachemodeladmin import CacheModelAdmin


class HistoryindicationResource(resources.ModelResource):
    """
    Resource for the Historyindication model.
    Has explicit foreign keys so Django import/export can automatically create the values if needed.
    """

    eunumber = import_foreign_key("eunumber", Medicine)

    class Meta:
        """
        Meta class for HistoryindicationResource
        """

        model = Historyindication
        import_id_fields = (
            "eunumber",
            "indicationdate",
        )


class HistoryindicationAdmin(import_admin.ImportExportModelAdmin, CacheModelAdmin):
    """
    Admin View for Historyindication
    """

    resource_class = HistoryindicationResource
    list = (
        "eunumber",
        "indication",
        "indicationdate",
    )


admin.site.register(Historyindication, HistoryindicationAdmin)
