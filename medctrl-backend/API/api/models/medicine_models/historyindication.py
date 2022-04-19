from django.db import models


class Historyindication(models.Model):
    eunumber = models.OneToOneField(
        "Medicine", models.CASCADE, db_column="EUNumber", primary_key=True
    )
    indication = models.CharField(db_column="Indication", max_length=45)
    indicationdate = models.DateField(db_column="IndicationDate", blank=True, null=True)

    class Meta:
        db_table = "historyindication"
        unique_together = (("eunumber", "indication"),)
