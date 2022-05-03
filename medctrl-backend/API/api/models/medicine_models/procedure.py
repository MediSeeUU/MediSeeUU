from django.db import models
from .medicine import Medicine
from .lookupproceduretype import Lookupproceduretype


class Procedure(models.Model):
    eunumber = models.ForeignKey(
        Medicine, models.CASCADE, db_column="EUNumber"
    )
    procedurecount = models.IntegerField(db_column="ProcedureCount")
    commisionnumber = models.IntegerField(
        db_column="CommisionNumber", blank=True, primary_key=True
    )
    emanumber = models.CharField(db_column="EMANumber", max_length=128, blank=True, null=True)
    proceduredate = models.DateField(db_column="ProcedureDate", blank=True, null=True)
    proceduretype = models.ForeignKey(
        Lookupproceduretype,
        models.CASCADE,
        db_column="ProcedureType",
        blank=True,
        null=True,
    )
    decisiondate = models.DateField(db_column="DecisionDate", blank=True, null=True)
    decisionnumber = models.CharField(
        db_column="DecisionNumber", max_length=45, blank=True, null=True
    )
    decisionurl = models.CharField(
        db_column="DecisionURL", max_length=255, blank=True, null=True
    )
    annexurl = models.CharField(
        db_column="AnnexURL", max_length=255, blank=True, null=True
    )

    class Meta:
        db_table = "procedure"
        unique_together = (("eunumber", "procedurecount"),)
