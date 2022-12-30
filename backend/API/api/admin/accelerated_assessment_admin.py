# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.contrib import admin
from import_export import resources, admin as import_admin
from api.models.human_models import (
    AcceleratedAssessment,
)
from api.admin.cachemodeladmin import CacheModelAdmin


class AcceleratedAssessmentResource(resources.ModelResource):
    """
    Necessary resource class for the AcceleratedAssessment admin view.
    Has explicit foreign keys so Django import/export can automatically create the values if needed.
    ModelResource is Resource subclass for handling Django models.
    """

    class Meta:
        """
        Meta class for AcceleratedAssessmentResource
        """
        model = AcceleratedAssessment
        import_id_fields = (
            "id",
        )


class AcceleratedAssessmentAdmin(import_admin.ImportExportModelAdmin, CacheModelAdmin):
    """
    Admin View for AcceleratedAssessment
    """
    resource_class = AcceleratedAssessmentResource
    list_display = [
        "id",
        "eu_accel_assess_g",
        "eu_accel_assess_m",
    ]


admin.site.register(AcceleratedAssessment, AcceleratedAssessmentAdmin)
