from django.db import models


class Lookuplegalscope(models.Model):
    legalscope = models.CharField(
        db_column="LegalScope", primary_key=True, max_length=45
    )

    class Meta:
        db_table = "lookuplegalscope"
