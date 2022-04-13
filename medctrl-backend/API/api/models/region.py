from django.db import models


class Region(models.Model):
    region_id = models.UUIDField(primary_key=True)
    description = models.CharField(max_length=320)

    class Meta:
        db_table = "region"
