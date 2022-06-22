# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models


class Historybrandname(models.Model):
    """
    Model class for the brand name history table.
    As the abstract functionality for all model classes is nearly identical,
    information about them has been moved to an external readme.
    """

    eunumber = models.ForeignKey("Medicine", models.CASCADE, db_column="EUNumber")
    brandname = models.CharField(db_column="BrandName", max_length=255)
    brandnamedate = models.DateField(db_column="BrandNameDate", blank=True, null=True)

    class Meta:
        db_table = "historybrandname"
        unique_together = (("eunumber", "brandnamedate"),)
