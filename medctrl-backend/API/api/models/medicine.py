from django.db import models
from api.models.atc_code import AtcCode
from api.models.legal_basis import LegalBasis
from api.models.legal_scope import LegalScope


class Medicine(models.Model):
    eu_nr = models.IntegerField(primary_key=True)
    ema_nr = models.CharField(max_length=45, blank=True, null=True)
    legal_basis = models.ForeignKey(
        LegalBasis, models.DO_NOTHING, blank=True, null=True, related_name='legalbasis_description'
    )
    legal_scope = models.ForeignKey(
        LegalScope, models.DO_NOTHING, blank=True, null=True
    )
    atc_code = models.ForeignKey(
        AtcCode, models.DO_NOTHING, db_column="atc_code", blank=True, null=True
    )
    prime = models.TextField(blank=True, null=True)
    orphan = models.TextField(blank=True, null=True)
    atmp = models.TextField(blank=True, null=True)
    ema_url = models.CharField(max_length=320, blank=True, null=True)

    class Meta:
        db_table = "medicine"
