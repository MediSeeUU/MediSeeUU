# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .common import create_dashboard_column, Category


class AcceleratedAssessment(models.Model):
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
