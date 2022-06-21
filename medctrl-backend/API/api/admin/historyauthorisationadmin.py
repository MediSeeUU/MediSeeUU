# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.contrib import admin
from import_export import resources, admin as import_admin
from api.models.medicine_models import (
    Medicine,
    Historyauthorisation,
)
from .common import import_foreign_key
from .cachemodeladmin import CacheModelAdmin


class HistoryauthorisationResource(resources.ModelResource):
    """
    Resource for the Historyauthorisation model.
    Has explicit foreign keys so Django import/export can automatically create the values if needed.
    """

    eunumber = import_foreign_key("eunumber", Medicine)

    class Meta:
        """
        Meta class for HistoryauthorisationResource
        """

        model = Historyauthorisation
        import_id_fields = (
            "eunumber",
            "authorisationdate",
        )


class HistoryauthorisationAdmin(import_admin.ImportExportModelAdmin, CacheModelAdmin):
    """
    Admin View for Historyauthorisation
    """

    resource_class = HistoryauthorisationResource
    list = (
        "eunumber",
        "authorisationdate",
        "opiniondate",
        "decisionauthorisationtype",
        "annexauthorisationtype",
        "registerauthorisationtype",
    )


admin.site.register(Historyauthorisation, HistoryauthorisationAdmin)