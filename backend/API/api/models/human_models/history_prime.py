# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .medicinal_product import MedicinalProduct
from api.models.common import BooleanWithNAField


class HistoryPrime(models.Model):
    """
    This is the model class for the Priority Medicine Designation History table. New attributes can be added here.
    This model is derived from a base model from the Django library.

    Attributes:
        eu_pnumber (models.ForeignKey):
            Foreign Key to the :py:class:`.MedicinalProduct` model
        change_date (models.DateField):
            DateField containing the date of the entry.
        eu_prime (BooleanWithNAField):
            BooleanWithNAField indicating if the medicine is an EU priority medicine. Initial shown on the dashboard.
    """
    eu_pnumber = models.ForeignKey(
        MedicinalProduct,
        models.CASCADE, 
        null=False,
        blank=False,
        related_name="eu_prime",
    )

    change_date = models.DateField(
        null=False,
        blank=False,
    )

    eu_prime = BooleanWithNAField(
        null=False,
        blank=False,
    )

    class Meta:
        db_table = "history_prime"
