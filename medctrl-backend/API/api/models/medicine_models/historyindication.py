# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models


class Historyindication(models.Model):
    """
    Model class for the identication history table. As the abstract functionality for all model classes is nearly identical, information about them has been moved to an external readme. 
    """
    eunumber = models.ForeignKey("Medicine", models.CASCADE, db_column="EUNumber")
    indication = models.CharField(db_column="Indication", max_length=45)
    indicationdate = models.DateField(db_column="IndicationDate", blank=True, null=True)

    class Meta:
        db_table = "historyindication"
        unique_together = (("eunumber", "indicationdate"),)
