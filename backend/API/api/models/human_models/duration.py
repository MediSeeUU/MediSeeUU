# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from api.models.create_dashboard_columns import create_dashboard_column, Category
from api.models.common import DataFormats
from api.models.na_fields import IntegerWithNAField


class Duration(models.Model):
    """
    This is the model class for the Duration table. New attributes can be added here.
    This model is derived from a base model from the Django library.

    Attributes:
        assess_time_days_total (models.IntegerField):
            IntegerField containing the total days of the duration of the
            initial EU authorisation assessment procedure. Shown on the dashboard.
        assess_time_days_active (models.IntegerField):
            IntegerField containing the active days of the duration of the
            initial EU authorisation assessment procedure. Shown on the dashboard.
        assess_time_days_cstop (models.IntegerField):
            IntegerField containing the clock-stop days of the duration of the
            initial EU authorisation assessment procedure. Shown on the dashboard.
        ec_decision_time_days (models.IntegerField):
            IntegerField containing the EC decision time in days. Shown on the dashboard.
    """
    assess_time_days_total = create_dashboard_column(
        IntegerWithNAField(
            null=False,
        ),
        Category.Marketing_authorisation,
        DataFormats.Number,
        "Duration of initial EU authorisation assessment procedure (total days)",
    )

    assess_time_days_active = create_dashboard_column(
        IntegerWithNAField(
            null=False,
        ),
        Category.Marketing_authorisation,
        DataFormats.Number,
        "Duration of initial EU authorisation assessment procedure (active days)",
    )

    assess_time_days_cstop = create_dashboard_column(
        IntegerWithNAField(
            null=False,
        ),
        Category.Marketing_authorisation,
        DataFormats.Number,
        "Duration of initial EU authorisation assessment procedure (clock-stop days)",
    )

    ec_decision_time_days = create_dashboard_column(
        IntegerWithNAField(
            null=False,
        ),
        Category.Marketing_authorisation,
        DataFormats.Number,
        "EC decision time (days)",
    )

    class Meta:
        db_table = "duration"
        verbose_name = "Duration"
        verbose_name_plural = "Durations"
