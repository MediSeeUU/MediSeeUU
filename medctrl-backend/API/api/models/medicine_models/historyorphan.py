from django.db import models


class Historyorphan(models.Model):
    eunumber = models.ForeignKey("Medicine", models.CASCADE, db_column="EUNumber")
    orphan = models.IntegerField(db_column="Orphan")
    orphandate = models.DateField(db_column="OrphanDate", blank=True, null=True)

    class Meta:
        db_table = "historyorphan"
        unique_together = (("eunumber", "orphandate"),)
