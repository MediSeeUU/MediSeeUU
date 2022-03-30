from django.db import models
from api.models.medicine import Medicine

class Procedure(models.Model):
    eu_nr = models.OneToOneField(Medicine, models.DO_NOTHING, db_column='eu_nr', primary_key=True)
    procedure_count = models.IntegerField()
    comission_procedure_nr = models.IntegerField(blank=True, null=True)
    ema_procedure_nr = models.IntegerField(blank=True, null=True)
    procedure_date = models.DateField(blank=True, null=True)
    procedure_type = models.ForeignKey('ProcedureType', models.DO_NOTHING, db_column='procedure_type', blank=True, null=True)
    decision_date = models.DateField(blank=True, null=True)
    decision_nr = models.IntegerField(blank=True, null=True)
    descision_url = models.CharField(max_length=320, blank=True, null=True)
    annex_url = models.CharField(max_length=320, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'procedure'
        unique_together = (('eu_nr', 'procedure_count'),)