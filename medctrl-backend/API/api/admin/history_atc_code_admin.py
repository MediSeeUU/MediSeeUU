# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.contrib import admin
from import_export import resources, admin as import_admin
from api.models.medicine_models import (
    Medicine,
    HistoryATCCode,
)
from api.admin.common import import_foreign_key
from api.admin.cachemodeladmin import CacheModelAdmin


class HistoryATCCodeResource(resources.ModelResource):
    """
    Resource for the HistoryATCCode model.
    Has explicit foreign keys so Django import/export can automatically create the values if needed.
    """

    eu_pnumber = import_foreign_key("eu_pnumber", Medicine)

    class Meta:
        """
        Meta class for HistoryATCCodeResource
        """

        model = HistoryATCCode
        import_id_fields = (
            "eu_pnumber",
        )


class HistoryATCCodeAdmin(import_admin.ImportExportModelAdmin, CacheModelAdmin):
    """
    Admin View for HistoryATCCode
    """

    resource_class = HistoryATCCodeResource
    list = (
        "atc_code_id",
        "eu_pnumber",
        "change_date",
        "atc_code",
    )


admin.site.register(HistoryATCCode, HistoryATCCodeAdmin)
