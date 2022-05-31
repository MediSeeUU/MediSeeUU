from django.contrib import admin
from import_export import fields, resources, admin as import_admin
from api.models.medicine_models import (
    Medicine,
    Authorisation,
    Lookuprapporteur,
)
from .common import CustomForeignKeyWidget, import_foreign_key
from .cachemodeladmin import CacheModelAdmin


class AuthorisationResource(resources.ModelResource):
    """
    Resource for the Authorisation model.
    Has explicit foreign keys so Django import/export can automatically create the values if needed.
    """

    eunumber = import_foreign_key("eunumber", Medicine)
    rapporteur = import_foreign_key("rapporteur", Lookuprapporteur)
    corapporteur = fields.Field(
        column_name="corapporteur",
        attribute="corapporteur",
        widget=CustomForeignKeyWidget(Lookuprapporteur, "rapporteur"),
    )

    class Meta:
        """
        Meta class for AuthorisationResource
        """

        model = Authorisation
        import_id_fields = ("eunumber",)


class AuthorisationAdmin(import_admin.ImportExportModelAdmin, CacheModelAdmin):
    """
    Admin View for Authorisation
    """

    resource_class = AuthorisationResource
    list = (
        "eunumber",
        "rapporteur",
        "corapporteur",
        "acceleratedgranted",
        "acceleratedmaintained",
        "authorisationtotaltime",
        "authorisationactivetime",
        "authorisationstoppedtime",
        "decisiontime",
        "decisionurl",
        "annexurl",
        "eparurl",
    )


admin.site.register(Authorisation, AuthorisationAdmin)
