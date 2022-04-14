from django.db import models
from .medicine import Medicine
from .lookupproceduretype import Lookupproceduretype

class Procedure(models.Model):
    eunumber = models.OneToOneField(Medicine, models.CASCADE, db_column='EUNumber', primary_key=True)
    procedurecount = models.IntegerField(db_column='ProcedureCount')
    commisionnumber = models.IntegerField(db_column='CommisionNumber', blank=True, null=True)
    emanumber = models.IntegerField(db_column='EMANumber', blank=True, null=True)
    proceduredate = models.DateField(db_column='ProcedureDate', blank=True, null=True)
    proceduretype = models.ForeignKey(Lookupproceduretype, models.CASCADE, db_column='ProcedureType', blank=True, null=True)
    decisiondate = models.DateField(db_column='DecisionDate', blank=True, null=True)
    decisionnumber = models.IntegerField(db_column='DecisionNumber', blank=True, null=True)
    decisionurl = models.CharField(db_column='DecisionURL', max_length=255, blank=True, null=True)
    annexurl = models.CharField(db_column='AnnexURL', max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'procedure'
        unique_together = (('eunumber', 'procedurecount'),)