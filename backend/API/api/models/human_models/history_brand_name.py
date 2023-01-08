# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from api.models.human_models import MedicinalProduct
from api.models.create_dashboard_columns import (
    Category,
)
from api.models.common import DataFormats


class HistoryBrandName(models.Model):
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

    class HistoryInfo:
        category = Category.Medicinal_product
        data_format = DataFormats.String
        current_name = "eu_brand_name_current"
        current_title = "Current EU brand name"
        timeline_title = "EU Brand Name"
        timeline_name = "eu_brand_name"
