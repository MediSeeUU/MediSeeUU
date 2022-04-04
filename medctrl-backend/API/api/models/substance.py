from django.db import models


class Substance(models.Model):
    substance_id = models.UUIDField(primary_key=True)
    description = models.CharField(max_length=320)

    class Meta:
        db_table = "substance"
