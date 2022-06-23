# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models


class Lookupproceduretype(models.Model):
    """
    Model class for the procedure type lookup table.
    """

    proceduretype = models.CharField(
        db_column="ProcedureType", primary_key=True, max_length=128
    )

    class Meta:
        db_table = "lookupproceduretype"
