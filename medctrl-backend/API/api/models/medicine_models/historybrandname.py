from django.db import models


class Historybrandname(models.Model):
    eunumber = models.ForeignKey(
        "Medicine", models.CASCADE, db_column="EUNumber"
    )
    brandname = models.CharField(db_column="BrandName", max_length=45)
    brandnamedate = models.DateField(db_column="BrandNameDate", blank=True, null=True)

    class Meta:
        db_table = "historybrandname"
        unique_together = (("eunumber", "brandnamedate"),)
