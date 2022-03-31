from django.db import models


class Substance(models.Model):
    substance_id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=320)

    class Meta:
        managed = False
        db_table = "substance"
