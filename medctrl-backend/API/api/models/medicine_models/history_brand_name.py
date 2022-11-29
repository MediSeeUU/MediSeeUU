# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .medicinal_product import MedicinalProduct
from api.models.dashboard_columns import create_dashboard_history_current_column, Category


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

    eu_brand_name = create_dashboard_history_current_column(
        models.TextField(
            null=False,
            blank=False,
        ),
        Category.General_Information,
        "string",
        "EU Brand Name",
    )

    class Meta:
        db_table = "history_brand_name"
