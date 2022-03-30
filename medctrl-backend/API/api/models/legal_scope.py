from django.db import models


class LegalScope(models.Model):
    legal_scope_id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = "legal_scope"
