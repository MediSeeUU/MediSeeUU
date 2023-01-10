# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from api.models.human_models import MedicinalProduct
from api.models.create_dashboard_columns import (
    Category,
)
from api.models.common import (
    DataFormats,
)
from api.models.other import LockModel


class HistoryBrandName(LockModel):
    """
    This is the model class for the Brand Name history table. New attributes can be added here.
    This model is derived from a base model from the Django library.

    Attributes:
        eu_pnumber (models.ForeignKey):
            Foreign Key to the :py:class:`.MedicinalProduct` model
        change_date (models.DateField):
            DateField containing the date of the entry.
        eu_brand_name (models.TextField):
            TextField containing the EU brand name. Initial and current shown on the dashboard.
    """
    eu_pnumber = models.ForeignKey(
        MedicinalProduct,
        models.CASCADE,
        null=False,
        blank=False,
        related_name="eu_brand_name",
    )

    change_date = models.DateField(
        null=False,
        blank=False,
    )

    eu_brand_name = models.TextField(
        null=False,
        blank=False,
    )

    class Meta:
        db_table = "history_brand_name"
        verbose_name = "History Brand Name"
        verbose_name_plural = "Histories Brand Name"

    class HistoryInfo:
        dashboard_columns = [
            {
                "category": Category.Medicinal_product,
                "data-key": "eu_brand_name_current",
                "data-format": DataFormats.String,
                "data-value": "Current EU brand name",
            }
        ]
        timeline_items = [
            {
                "category": Category.Medicinal_product,
                "data-key": "eu_brand_name",
                "data-format": DataFormats.String,
                "data-value": "EU Brand Name",
            }
        ]
