# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.contrib import admin
from import_export import resources, admin as import_admin
from api.models.medicine_models import (
    Medicine,
    HistoryNumberCheck,
)
from api.admin.common import import_foreign_key
from api.admin.cachemodeladmin import CacheModelAdmin


class HistoryNumberCheckResource(resources.ModelResource):
    """
    Resource for the HistoryNumberCheck model.
    Has explicit foreign keys so Django import/export can automatically create the values if needed.
    """

    eu_pnumber = import_foreign_key("eu_pnumber", Medicine)

    class Meta:
        """
        Meta class for HistoryNumberCheckResource
        """

        model = HistoryNumberCheck
        import_id_fields = (
            "eu_pnumber",
        )


class HistoryNumberCheckAdmin(import_admin.ImportExportModelAdmin, CacheModelAdmin):
    """
    Admin View for HistoryNumberCheck
    """

    resource_class = HistoryNumberCheckResource
    list = (
        "ema_number_check_id",
        "eu_pnumber",
        "change_date",
        "ema_number_check",
    )


admin.site.register(HistoryNumberCheck, HistoryNumberCheckAdmin)
