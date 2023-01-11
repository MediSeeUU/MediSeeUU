# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .medicinal_product import MedicinalProduct
from api.models.create_dashboard_columns import (
    Category,
)
from api.models.common import DataFormats, AutTypes


class HistoryAuthorisationType(models.Model):
    """
    This is the model class for the Authorisation Type history table. New attributes can be added here.
    This model is derived from a base model from the Django library.

    Attributes:
        eu_pnumber (models.ForeignKey):
            Foreign Key to the :py:class:`.MedicinalProduct` model
        change_date (models.DateField):
            DateField containing the date of the entry.
        eu_aut_type (models.CharField):
            CharField containing the authorisation type. Restricted by the options from :py:class:`.AutTypes`
            Initial and current shown on the dashboard.
    """
    eu_pnumber = models.ForeignKey(
        MedicinalProduct,
        models.CASCADE, 
        null=False,
        related_name="eu_aut_type",
    )

    change_date = models.DateField(
        null=False,
    )

    eu_aut_type = models.CharField(
        max_length=45,
        choices=AutTypes.choices,
        null=False,
        blank=False,
    )

    class Meta:
        db_table = "history_authorisation_type"
        verbose_name = "History Authorisation Type"
        verbose_name_plural = "Histories Authorisation Type"

    class HistoryInfo:
        dashboard_columns = [
            {
                "category": Category.Marketing_authorisation,
                "data-key": "eu_aut_type_current",
                "data-format": DataFormats.String,
                "data-value": "Current type of EU authorisation",
            }
        ]
        timeline_items = [
            {
                "category": Category.Marketing_authorisation,
                "data-key": "eu_aut_type",
                "data-format": DataFormats.String,
                "data-value": "EU Authorisation Type",
            }
        ]
