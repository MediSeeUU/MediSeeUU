from api.models.medicine_models import MedicinalProduct
from django.db import models


class MedicineLocks(models.Model):
    """
    This is the model class for the Medicine Locks table.
    It is used to store locked attributes for a :py:class:`.MedicinalProduct` object.
    This model is derived from a base model from the Django library.

    Attributes:
        eu_pnumber (models.ForeignKey):
            Foreign Key to the :py:class:`.MedicinalProduct` object the lock is for.
        column_name (models.CharField):
            CharField containing the name of the column that needs to be locked.
    """
    eu_pnumber = models.ForeignKey(
        MedicinalProduct,
        models.CASCADE,
        null=False,
    )

    column_name = models.CharField(
        max_length=255,
        null=False
    )

    class Meta:
        db_table = "medicine_locks"
        constraints = [
            models.UniqueConstraint(
                fields=['eu_pnumber', 'column_name'],
                name="eu_pnumber column_name composite key"
            )
        ]
