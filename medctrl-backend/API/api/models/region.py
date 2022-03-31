from django.db import models


class Region(models.Model):
    region_id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=320)

    class Meta:
        managed = False
        db_table = "region"
