from django.db import models


class Lookupstatus(models.Model):
    status = models.CharField(db_column="Status", primary_key=True, max_length=45)

    class Meta:
        db_table = "lookupstatus"
