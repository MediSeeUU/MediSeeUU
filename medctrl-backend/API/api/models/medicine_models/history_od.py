# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .common import create_dashboard_column, Category


class HistoryOD(models.Model):
    """
    Model class for the orphan designation history table.
    """
    eu_od_id = models.IntegerField(db_column="eu_od_id", primary_key=True, null=False)

    eu_pnumber = models.ForeignKey("Medicine", models.CASCADE, db_column="eu_pnumber", null=False)

    change_date = models.DateField(db_column="change_date", null=True)

    eu_od = create_dashboard_column(
        models.BooleanField(db_column="eu_od", null=True),
        Category.General_Information,
        "bool",
        "EU Orphan Designation"
    )

    class Meta:
        db_table = "history_od"
