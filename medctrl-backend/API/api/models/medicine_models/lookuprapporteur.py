# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models


class Lookuprapporteur(models.Model):
    rapporteur = models.CharField(
        db_column="Rapporteur", primary_key=True, max_length=45
    )

    class Meta:
        db_table = "lookuprapporteur"
