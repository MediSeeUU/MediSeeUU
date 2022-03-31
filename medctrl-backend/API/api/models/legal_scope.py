from django.db import models


class LegalScope(models.Model):
    legal_scope_id = models.UUIDField(primary_key=True)
    description = models.CharField(max_length=45)

    class Meta:
        db_table = "legal_scope"
