# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .common import create_dashboard_column, Category


class HistoryMAH(models.Model):
    """
    Model class for the MAH history table.
    """
    eu_mah_id = models.IntegerField(db_column="eu_mah_id", primary_key=True, null=False)

    eu_pnumber = models.ForeignKey("Medicine", models.CASCADE, db_column="eu_pnumber", null=False)

    change_date = models.DateField(db_column="change_date", null=True)

    eu_mah = create_dashboard_column(
        models.CharField(db_column="eu_mah", max_length=255),
        Category.General_Information,
        "string",
        "EU Marketing Authorisation Holder"
    )

    class Meta:
        db_table = "eu_mah_history"
