# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.contrib import admin
from import_export import resources, admin as import_admin
from api.models.human_models import MedicinalProduct
from api.admin.cachemodeladmin import CacheModelAdmin


class MedicinalProductResource(resources.ModelResource):
    """
    Necessary resource class for the MedicinalProduct admin view.
    ModelResource is Resource subclass for handling Django models.
    """    
    class Meta:
        """
        Meta class for MedicinalProductResource
        """
        model = MedicinalProduct
        import_id_fields = ("eu_pnumber",)


class MedicinalProductAdmin(import_admin.ImportExportModelAdmin, CacheModelAdmin):
    """
    Admin View for Medicine, contains a list of all the shown attributes.
    """
    resource_class = MedicinalProductResource

    list_display = [
        "eu_pnumber",
        "ema_number",
    ]


admin.site.register(MedicinalProduct, MedicinalProductAdmin)
