from django.db import models


class MarketingAuthorisationHolder(models.Model):
    mah_id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=320)

    class Meta:
        managed = False
        db_table = "marketing_authorisation_holder"
