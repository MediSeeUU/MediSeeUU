# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .medicinal_product import MedicinalProduct
from api.models.create_dashboard_columns import (
    Category,
)
from api.models.common import (
    DataFormats,
    ODChoices,
)
from api.models.na_fields import BooleanWithNAField


class HistoryOD(models.Model):
    """
    This is the model class for the Orphan Designation history table. New attributes can be added here.
    This model is derived from a base model from the Django library.

    Attributes:
        eu_pnumber (models.ForeignKey):
            Foreign Key to the :py:class:`.MedicinalProduct` model
        change_date (models.DateField):
            DateField containing the date of the entry.
        eu_od (BooleanWithNAField):
            BooleanWithNAField indicating if the medicine has an EU orphan designation. Initial shown on the dashboard.
    """
    eu_pnumber = models.ForeignKey(
        MedicinalProduct,
        models.CASCADE, 
        null=False,
        blank=False,
        related_name="eu_od",
    )

    change_date = models.DateField(
        null=False,
        blank=False,
    )

    eu_od = models.CharField(
        max_length=40,
        choices=ODChoices.choices,
        null=False,
        blank=False,
    )

    class Meta:
        db_table = "history_od"

    class HistoryInfo:
        timeline_items = [
            {
                "category": Category.Marketing_authorisation,
                "data-key": "eu_od",
                "data-format": DataFormats.Bool,
                "data-value": "EU orphan designation",
            }
        ]
