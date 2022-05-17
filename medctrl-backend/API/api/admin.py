# from django.contrib import admin

# Register your models here.

from django.contrib import admin
from import_export import fields, resources, widgets, admin as import_admin
from api.models.medicine_models import (
    Medicine,
    Authorisation,
    Procedure,
    Lookupatccode,
    Lookuplegalbasis,
    Lookuplegalscope,
    Lookupmedicinetype,
    Lookupstatus,
    Lookupactivesubstance,
    Lookuprapporteur,
    Lookupproceduretype,
    Historyauthorisation,
    Historybrandname,
    Historyindication,
    Historymah,
    Historyorphan,
    Historyprime,
)
from api.update_cache import update_cache


def import_foreign_key(field, model):
    """
    Create a ForeignKey field for a given field and model.
    Can be used to automatically create foreign key fields for import if they don't exist already.

    :param field: The field to create a ForeignKey for
    :param model: The model to create a ForeignKey for
    """
    return fields.Field(
        column_name=field, attribute=field, widget=CustomForeignKeyWidget(model, field)
    )


class CustomForeignKeyWidget(widgets.ForeignKeyWidget):
    """
    Custom ForeignKeyWidget that creates a new object if it doesn't exist already.
    """

    def clean(self, value, row, *args, **kwargs):
        if value is not None:
            value, _ = self.model.objects.get_or_create(**{self.field: value})

        return value


class CacheModelAdmin(admin.ModelAdmin):
    """
    Admin View class.
    Every class that will inherit from this will automatically update the cache after data modifications.
    """

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        update_cache()
    
    def delete_queryset(self, request, queryset):
        super().delete_queryset(request, queryset)
        update_cache()
    
    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        update_cache()


class MedicineResource(resources.ModelResource):
    """
    Resource for the Medicine model.
    Has explicit foreign keys so Django import/export can automatically create the values if needed.
    """

    atccode = import_foreign_key("atccode", Lookupatccode)
    legalbasis = import_foreign_key("legalbasis", Lookuplegalbasis)
    legalscope = import_foreign_key("legalscope", Lookuplegalscope)
    medicinetype = import_foreign_key("medicinetype", Lookupmedicinetype)
    status = import_foreign_key("status", Lookupstatus)
    activesubstance = import_foreign_key("activesubstance", Lookupactivesubstance)

    class Meta:
        """
        Meta class for MedicineResource
        """

        model = Medicine
        import_id_fields = ("eunumber",)


class MedicineAdmin(import_admin.ImportExportModelAdmin, CacheModelAdmin):
    """
    Admin View for Medicine
    """

    resource_class = MedicineResource
    list = (
        "eunumber",
        "emanumber",
        "atccode",
        "activesubstance",
        "newactivesubstance",
        "legalbasis",
        "legalscope",
        "atmp",
        "status",
        "referral",
        "suspension",
        "emaurl",
        "ecurl",
    )


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


class ProcedureResource(resources.ModelResource):
    """
    Resource for the Procedure model.
    Has explicit foreign keys so Django import/export can automatically create the values if needed.
    """

    eunumber = import_foreign_key("eunumber", Medicine)
    proceduretype = import_foreign_key("proceduretype", Lookupproceduretype)

    class Meta:
        """
        Meta class for ProcedureResource
        """

        model = Procedure
        import_id_fields = ("commisionnumber",)


class ProcedureAdmin(import_admin.ImportExportModelAdmin, CacheModelAdmin):
    """
    Admin View for Procedure
    """

    resource_class = ProcedureResource
    list = (
        "eunumber",
        "procedurecount",
        "commisionnumber",
        "emanumber",
        "proceduredate",
        "proceduretype",
        "decisiondate",
        "decisionnumber",
        "decisionurl",
        "annexurl",
    )


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


class HistoryorphanResource(resources.ModelResource):
    """
    Resource for the Historyorphan model.
    Has explicit foreign keys so Django import/export can automatically create the values if needed.
    """

    eunumber = import_foreign_key("eunumber", Medicine)

    class Meta:
        """
        Meta class for HistoryorphanResource
        """

        model = Historyorphan
        import_id_fields = (
            "eunumber",
            "orphandate",
        )


class HistoryorphanAdmin(import_admin.ImportExportModelAdmin, CacheModelAdmin):
    """
    Admin View for Historyorphan
    """

    resource_class = HistoryorphanResource
    list = (
        "eunumber",
        "orphan",
        "orphandate",
    )


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


admin.site.register(Medicine, MedicineAdmin)
admin.site.register(Authorisation, AuthorisationAdmin)
admin.site.register(Procedure, ProcedureAdmin)
admin.site.register(Historyauthorisation, HistoryauthorisationAdmin)
admin.site.register(Historybrandname, HistorybrandnameAdmin)
admin.site.register(Historyindication, HistoryindicationAdmin)
admin.site.register(Historymah, HistorymahAdmin)
admin.site.register(Historyorphan, HistoryorphanAdmin)
admin.site.register(Historyprime, HistoryprimeAdmin)
