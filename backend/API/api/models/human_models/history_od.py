# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .medicinal_product import MedicinalProduct
from api.models.create_dashboard_columns import (
    Category,
)
from api.models.common import DataFormats
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

    eu_od = BooleanWithNAField(
        null=False,
        blank=False,
    )

    class Meta:
        db_table = "history_od"

    class HistoryInfo:
        category = Category.Marketing_authorisation
        data_format = DataFormats.Bool
        timeline_title = "EU orphan designation"
        timeline_name = "eu_od"
