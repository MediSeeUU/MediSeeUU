# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .common import create_dashboard_column, Category


class Historymah(models.Model):
    """
    Model class for the MAH history table.
    """

    eunumber = models.ForeignKey("Medicine", models.CASCADE, db_column="EUNumber")
    mah = create_dashboard_column(
        models.CharField(db_column="MAH", max_length=255),
        Category.General_Information,
        "string",
        "Marketing Authorisation Holder"
    )
    mahdate = models.DateField(db_column="MAHDate", blank=True, null=True)

    class Meta:
        db_table = "historymah"
        unique_together = (("eunumber", "mahdate"),)
