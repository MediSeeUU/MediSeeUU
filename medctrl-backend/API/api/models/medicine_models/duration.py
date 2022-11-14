# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .common import create_dashboard_column, Category


class Duration(models.Model):
    assess_time_days_total = create_dashboard_column(
        models.IntegerField(
            db_column="assess_time_days_total",
            null=False,
        ),
        Category.General_Information,
        "number",
        "Duration of initial EU authorisation assessment procedure (total days)",
    )

    assess_time_days_active = create_dashboard_column(
        models.IntegerField(
            db_column="assess_time_days_active",
            null=False,
        ),
        Category.General_Information,
        "number",
        "Duration of initial EU authorisation assessment procedure (active days)",
    )

    assess_time_days_cstop = create_dashboard_column(
        models.IntegerField(
            db_column="assess_time_days_cstop",
            null=False,
        ),
        Category.General_Information,
        "number",
        "Duration of initial EU authorisation assessment procedure (clock-stop days)",
    )

    ec_decision_time_days = create_dashboard_column(
        models.IntegerField(
            db_column="ec_decision_time_days",
            null=False,
        ),
        Category.General_Information,
        "number",
        "EC decision time (days)",
    )

    class Meta:
        db_table = "duration"
