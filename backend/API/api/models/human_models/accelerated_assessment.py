# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from api.models.create_dashboard_columns import create_dashboard_column, Category
from api.models.common import (
    DataFormats,
)
from api.models.na_fields import BooleanWithNAField
from api.models.other import LockModel


class AcceleratedAssessment(LockModel):
    """
    This is the model class for the EMA Accelerated Assessment table. New attributes can be added here.
    This model is derived from a base model from the Django library.

    Attributes:
        eu_accel_assess_g (BooleanWithNAField):
            BooleanWithNAField indicating if accelerated assessment has been granted. Shown on the dashboard.
        eu_accel_assess_m (BooleanWithNAField):
            BooleanWithNAField indicating if accelerated assessment has been maintained. Shown on the dashboard.
    """
    eu_accel_assess_g = create_dashboard_column(
        BooleanWithNAField(
            null=True,
        ),
        Category.Marketing_authorisation,
        DataFormats.Bool,
        "EU accelerated assessment granted",
    )

    eu_accel_assess_m = create_dashboard_column(
        BooleanWithNAField(
            null=True,
        ),
        Category.Marketing_authorisation,
        DataFormats.Bool,
        "EU accelerated assessment maintained",
    )

    class Meta:
        db_table = "accelerated_assessment"
        verbose_name = "Accelerated Assessment"
        verbose_name_plural = "Accelerated Assessments"
