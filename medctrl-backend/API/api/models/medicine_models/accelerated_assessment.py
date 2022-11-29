# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from api.models.dashboard_columns import create_dashboard_column, Category


class AcceleratedAssessment(models.Model):
    """
    This is the model class for the EMA Accelerated Assessment table. New attributes can be added here.
    This model is derived from a base model from the Django library.

    Attributes:
        eu_accel_assess_g (models.BooleanField):
            BooleanField indicating if accelerated assessment has been granted. Shown on the dashboard.
        eu_accel_assess_m (models.BooleanField):
            BooleanField indicating if accelerated assessment has been maintained. Shown on the dashboard.
    """
    eu_accel_assess_g = create_dashboard_column(
        models.BooleanField(
            null=True,
        ),
        Category.General_Information,
        "bool",
        "EU accelerated assessment granted",
    )

    eu_accel_assess_m = create_dashboard_column(
        models.BooleanField(
            null=True,
        ),
        Category.General_Information,
        "bool",
        "EU accelerated assessment maintained",
    )

    class Meta:
        db_table = "accelerated_assessment"
