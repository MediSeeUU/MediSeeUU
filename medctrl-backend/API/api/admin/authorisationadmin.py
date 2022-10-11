# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.contrib import admin
from import_export import fields, resources, admin as import_admin
from api.models.medicine_models import (
    Medicine,
    Authorisation
)
from api.admin.common import import_foreign_key
from api.admin.cachemodeladmin import CacheModelAdmin


class AuthorisationResource(resources.ModelResource):
    """
    Resource for the Authorisation model.
    Has explicit foreign keys so Django import/export can automatically create the values if needed.
    """

    eunumber = import_foreign_key("eunumber", Medicine)

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
