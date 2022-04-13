from django.db import models

class Historyorphan(models.Model):
    eunumber = models.OneToOneField('Medicine', models.CASCADE, db_column='EUNumber', primary_key=True)
    orphan = models.IntegerField(db_column='Orphan')
    orphandate = models.DateField(db_column='OrphanDate', blank=True, null=True)

    class Meta:
        db_table = 'historyorphan'
        unique_together = (('eunumber', 'orphan'),)