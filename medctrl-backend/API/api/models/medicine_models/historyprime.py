from django.db import models


class Historyprime(models.Model):
    eunumber = models.ForeignKey(
        "Medicine", models.CASCADE, db_column="EUNumber"
    )
    prime = models.IntegerField(db_column="PRIME")
    primedate = models.DateField(db_column="PRIMEDate", blank=True, null=True)

    class Meta:
        db_table = "historyprime"
