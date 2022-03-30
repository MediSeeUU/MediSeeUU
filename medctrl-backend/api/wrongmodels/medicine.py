from django.db import models

class Medicine(models.Model):
    eu_nr = models.IntegerField(primary_key=True)
    ema_nr = models.CharField(max_length=45, blank=True, null=True)
    legal_basis = models.ForeignKey(models.LegalBasis, models.DO_NOTHING, blank=True, null=True)
    legal_scope = models.ForeignKey(models.LegalScope, models.DO_NOTHING, blank=True, null=True)
    atc_code = models.ForeignKey(models.AtcCode, models.DO_NOTHING, db_column='atc_code', blank=True, null=True)
    prime = models.TextField(blank=True, null=True)  # This field type is a guess.
    orphan = models.TextField(blank=True, null=True)  # This field type is a guess.
    atmp = models.TextField(blank=True, null=True)  # This field type is a guess.
    ema_url = models.CharField(max_length=320, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'medicine'