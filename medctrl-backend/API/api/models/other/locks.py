from django.db import models


class Locks(models.Model):
    """
    This is the model class for the Locks table. It is used to store locked attributes for a medicine object.
    This model is derived from a base model from the Django library.
    """
    eu_pnumber = models.ForeignKey(
        "Medicine",
        models.CASCADE,
        db_column="eu_pnumber",
        null=False,
    )

    column_name = models.CharField(
        db_column="column_name",
        max_length=255,
        null=False
    )

    class Meta:
        db_table = "locks"
        constraints = [
            models.UniqueConstraint(
                fields=['eu_pnumber', 'column_name'],
                name="eu_pnumber column_name composite key"
            )
        ]
