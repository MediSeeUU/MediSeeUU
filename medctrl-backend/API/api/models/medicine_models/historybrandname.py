# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .common import create_dashboard_column, Category


class Historybrandname(models.Model):
    """
    Model class for the brand name history table.
    """

    eunumber = models.ForeignKey("Medicine", models.CASCADE, db_column="EUNumber")
    brandname = create_dashboard_column(
        models.CharField(db_column="BrandName", max_length=255),
        Category.General_Information,
        "string",
        "Brand Name"
    )
    brandnamedate = models.DateField(db_column="BrandNameDate", blank=True, null=True)

    class Meta:
        db_table = "historybrandname"
        unique_together = (("eunumber", "brandnamedate"),)
