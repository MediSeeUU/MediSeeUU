# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models


class Historymah(models.Model):
    """
    Model class for the MAH history table.
    """

    eunumber = models.ForeignKey("Medicine", models.CASCADE, db_column="EUNumber")
    mah = models.CharField(db_column="MAH", max_length=255)
    mahdate = models.DateField(db_column="MAHDate", blank=True, null=True)

    class Meta:
        db_table = "historymah"
        unique_together = (("eunumber", "mahdate"),)
