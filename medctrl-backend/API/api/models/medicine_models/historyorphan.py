# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models


class Historyorphan(models.Model):
    """
    Model class for the orphan designation history table. As the abstract functionality for all model classes is nearly identical, information about them has been moved to an external readme.
    """

    eunumber = models.ForeignKey("Medicine", models.CASCADE, db_column="EUNumber")
    orphan = models.IntegerField(db_column="Orphan")
    orphandate = models.DateField(db_column="OrphanDate", blank=True, null=True)

    class Meta:
        db_table = "historyorphan"
        unique_together = (("eunumber", "orphandate"),)
