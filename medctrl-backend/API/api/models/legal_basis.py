from django.db import models


class LegalBasis(models.Model):
    legal_basis_id = models.UUIDField(primary_key=True)
    description = models.CharField(max_length=45)

    class Meta:
        db_table = "legal_basis"