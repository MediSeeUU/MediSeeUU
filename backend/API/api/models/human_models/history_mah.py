# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .medicinal_product import MedicinalProduct
from api.models.create_dashboard_columns import (
    Category
)
from api.models.common import (
    DataFormats,
)
from api.models.other import LockModel


class HistoryMAH(LockModel):
    """
    This is the model class for the Marketing Authorisation Holder history table. New attributes can be added here.
    This model is derived from a base model from the Django library.

    Attributes:
        eu_pnumber (models.ForeignKey):
            Foreign Key to the :py:class:`.MedicinalProduct` model
        change_date (models.DateField):
            DateField containing the date of the entry.
        eu_mah (models.CharField):
            CharField containing the EU marketing authorisation holder. Initial and current shown on the dashboard.
    """
    eu_pnumber = models.ForeignKey(
        MedicinalProduct,
        models.CASCADE, 
        null=False,
        blank=False,
        related_name="eu_mah",
    )

    change_date = models.DateField(
        null=False,
        blank=False,
    )

    eu_mah = models.CharField(
        max_length=255,
        null=False,
        blank=False,
    )

    class Meta:
        db_table = "eu_mah_history"
        verbose_name = "History MAH"
        verbose_name_plural = "Histories MAH"

    class HistoryInfo:
        dashboard_columns = [
            {
                "category": Category.Marketing_authorisation,
                "data-key": "eu_mah_current",
                "data-format": DataFormats.String,
                "data-value": "Current EU marketing authorisation holder",
            }
        ]
        timeline_items = [
            {
                "category": Category.Marketing_authorisation,
                "data-key": "eu_mah",
                "data-format": DataFormats.String,
                "data-value": "EU Marketing Authorisation Holder",
            }
        ]

    def __str__(self):
        return f"MAH<{self.eu_mah}> History Item"
