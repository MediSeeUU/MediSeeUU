from django.db import models

class AtcCode(models.Model):
    atc_code = models.CharField(primary_key=True, max_length=7)
    description = models.CharField(max_length=320)
    parent_code = models.ForeignKey('self', models.DO_NOTHING, db_column='parent_code', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'atc_code'