from django.db import models


class MarketingAuthorisationHolder(models.Model):
    mah_id = models.UUIDField(primary_key=True)
    description = models.CharField(max_length=320)

    class Meta:
        db_table = "marketing_authorisation_holder"
