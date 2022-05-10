from django.db import models


class Lookupproceduretype(models.Model):
    proceduretype = models.CharField(
        db_column="ProcedureType", primary_key=True, max_length=128
    )

    class Meta:
        db_table = "lookupproceduretype"
