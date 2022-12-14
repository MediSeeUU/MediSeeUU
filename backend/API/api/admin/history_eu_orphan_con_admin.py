# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.contrib import admin
from import_export import resources, admin as import_admin
from api.models.orphan_models import OrphanProduct
from api.models.orphan_models import HistoryEUOrphanCon
from api.admin.common import import_foreign_key
from api.admin.cachemodeladmin import CacheModelAdmin


class HistoryEUOrphanConResource(resources.ModelResource):
    """
    Necessary resource class for the HistoryEUOrphonCon admin view.
    Has explicit foreign keys so Django import/export can automatically create the values if needed.
    ModelResource is Resource subclass for handling Django models.
    """
    eu_od_number = import_foreign_key("eu_od_number", OrphanProduct)

    class Meta:
        """
        Meta class for HistoryEUOrphanConResource
        """
        model = HistoryEUOrphanCon
        import_id_fields = (
            "eu_od_number",
        )


class HistoryEUOrphanConAdmin(import_admin.ImportExportModelAdmin, CacheModelAdmin):
    """
    Admin View for HistoryEUOrphanCon
    """
    resource_class = HistoryEUOrphanConResource
    list_display = [
        "eu_od_number",
        "change_date",
        "indication",
    ]


admin.site.register(HistoryEUOrphanCon, HistoryEUOrphanConAdmin)
