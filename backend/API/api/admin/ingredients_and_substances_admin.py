# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.contrib import admin
from import_export import resources, admin as import_admin
from api.models.human_models import (
    MedicinalProduct,
    IngredientsAndSubstances,
)
from api.admin.common import import_foreign_key
from api.admin.cachemodeladmin import CacheModelAdmin


class IngredientsAndSubstancesResource(resources.ModelResource):
    """
    Necessary resource class for the IngredientsAndSubstances admin view.
    Has explicit foreign keys so Django import/export can automatically create the values if needed.
    ModelResource is Resource subclass for handling Django models.
    """
    eu_pnumber = import_foreign_key("eu_pnumber", MedicinalProduct)

    class Meta:
        """
        Meta class for IngredientsAndSubstancesResource
        """
        model = IngredientsAndSubstances
        import_id_fields = (
            "active_substance_hash",
        )


# TODO: Find out how to automatically generate hash when active substance is entered
class IngredientsAndSubstancesAdmin(import_admin.ImportExportModelAdmin, CacheModelAdmin):
    """
    Admin View for IngredientsAndSubstances
    """
    resource_class = IngredientsAndSubstancesResource
    list = (
        "active_substance",
        "atc_code",
        "eu_nas"
    )


admin.site.register(IngredientsAndSubstances, IngredientsAndSubstancesAdmin)
