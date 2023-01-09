# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.contrib import admin
from import_export import resources, admin as import_admin
from api.models.human_models import (
    IngredientsAndSubstances,
)
from api.admin.cachemodeladmin import CacheModelAdmin


class IngredientsAndSubstancesResource(resources.ModelResource):
    """
    Necessary resource class for the IngredientsAndSubstances admin view.
    Has explicit foreign keys so Django import/export can automatically create the values if needed.
    ModelResource is Resource subclass for handling Django models.
    """

    class Meta:
        """
        Meta class for IngredientsAndSubstancesResource
        """
        model = IngredientsAndSubstances
        import_id_fields = (
            "id",
        )


class IngredientsAndSubstancesAdmin(import_admin.ImportExportModelAdmin, CacheModelAdmin):
    """
    Admin View for IngredientsAndSubstances
    """
    resource_class = IngredientsAndSubstancesResource
    list_display = [
        "active_substance",
        "atc_code",
        "eu_nas",
    ]


admin.site.register(IngredientsAndSubstances, IngredientsAndSubstancesAdmin)
