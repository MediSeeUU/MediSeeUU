from api.models.orphan_models import OrphanProduct
from django.db import models


class OrphanLocks(models.Model):
    """
    This is the model class for the Orphan Locks table.
    It is used to store locked attributes for a :py:class:`.OrphanProduct` object.
    This model is derived from a base model from the Django library.

    Attributes:
        eu_od_number (models.ForeignKey):
            Foreign Key to the :py:class:`.OrphanProduct` object the lock is for.
        column_name (models.CharField):
            CharField containing the name of the column that needs to be locked.
    """
    eu_od_number = models.ForeignKey(
        OrphanProduct,
        models.CASCADE,
        null=False,
    )

    column_name = models.CharField(
        max_length=255,
        null=False
    )

    class Meta:
        db_table = "orphan_locks"
        constraints = [
            models.UniqueConstraint(
                fields=['eu_od_number', 'column_name'],
                name="eu_od_number column_name composite key"
            )
        ]
