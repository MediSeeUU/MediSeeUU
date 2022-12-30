# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.contrib import admin
from import_export import resources, admin as import_admin
from api.models.human_models import (
    MedicinalProduct,
)
from api.models.orphan_models import (
    OrphanProduct,
)
from api.admin.common import import_foreign_key
from api.admin.cachemodeladmin import CacheModelAdmin


class OrphanProductResource(resources.ModelResource):
    """
    Necessary resource class for the OrphanProduct admin view.
    Has explicit foreign keys so Django import/export can automatically create the values if needed.
    ModelResource is Resource subclass for handling Django models.
    """
    eu_od_pnumber = import_foreign_key("eu_pnumber", MedicinalProduct)

    class Meta:
        """
        Meta class for OrphanProductResource
        """
        model = OrphanProduct
        import_id_fields = (
            "eu_od_pnumber",
        )


class OrphanProductAdmin(import_admin.ImportExportModelAdmin, CacheModelAdmin):
    """
    Admin View for OrphanProduct
    """
    resource_class = OrphanProductResource
    list_display = [
        "eu_od_number",
        "eu_od_pnumber",
        "ema_od_number",
    ]


admin.site.register(OrphanProduct, OrphanProductAdmin)
