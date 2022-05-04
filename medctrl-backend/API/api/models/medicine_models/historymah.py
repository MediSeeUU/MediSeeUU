from django.db import models


class Historymah(models.Model):
    eunumber = models.ForeignKey(
        "Medicine", models.CASCADE, db_column="EUNumber"
    )
    mah = models.CharField(db_column="MAH", max_length=45)
    mahdate = models.DateField(db_column="MAHDate", blank=True, null=True)

    class Meta:
        db_table = "historymah"
