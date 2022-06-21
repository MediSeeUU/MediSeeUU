# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models


class Lookupstatus(models.Model):
    status = models.CharField(db_column="Status", primary_key=True, max_length=45)

    class Meta:
        db_table = "lookupstatus"
