# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from api.models.orphan_models import OrphanProduct
from api.models.create_dashboard_columns import (
    Category,
)
from api.models.common import DataFormats


class HistoryEUODSponsor(models.Model):
    """
    This is the model class for the Orphan Condition history table. New attributes can be added here.
    This model is derived from a base model from the Django library.

    Attributes:
        eu_od_number (models.ForeignKey):
            Foreign Key to the :py:class:`.OrphanProduct` model
        change_date (models.DateField):
            DateField containing the date of the entry.
        eu_orphan_con (models.TextField):
            TextField containing the EU orphan condition. Initial and current shown on the dashboard.
    """
    eu_od_number = models.ForeignKey(
        OrphanProduct,
        models.CASCADE,
        null=False,
        blank=False,
        related_name="eu_od_sponsor",
    )

    change_date = models.DateField(
        null=False,
        blank=False,
    )

    eu_od_sponsor = models.TextField(
        null=False,
        blank=False,
    )

    class Meta:
        db_table = "history_eu_od_sponsor"
        verbose_name = "History EU OD Sponsor"
        verbose_name_plural = "Histories EU OD Sponsor"

    class HistoryInfo:
        dashboard_columns = [
            {
                "category": Category.Orphan_product,
                "data-key": "eu_od_sponsor",
                "data-format": DataFormats.String,
                "data-value": "Sponsor for EU orphan designation",
            }
        ]
        timeline_items = [
            {
                "category": Category.Orphan_product,
                "data-key": "eu_od_sponsor",
                "data-format": DataFormats.String,
                "data-value": "EU orphan designation sponsor",
            }
        ]
