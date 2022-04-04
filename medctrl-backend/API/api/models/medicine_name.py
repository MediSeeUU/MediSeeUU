from django.db import models
from api.models.medicine import Medicine
from api.models.marketing_authorisation_holder import MarketingAuthorisationHolder


class MedicineName(models.Model):
    eu_nr = models.OneToOneField(
        Medicine, models.DO_NOTHING, db_column="eu_nr", primary_key=True
    )
    region = models.ForeignKey("Region", models.DO_NOTHING)
    start_date = models.DateField()
    mah = models.ForeignKey(MarketingAuthorisationHolder, models.DO_NOTHING)
    name = models.CharField(max_length=320)
    end_date = models.DateField(blank=True, null=True)
    brand = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "medicine_name"
        unique_together = (("eu_nr", "region", "start_date", "mah"),)
