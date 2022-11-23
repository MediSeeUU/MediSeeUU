# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .orphan_product import OrphanProduct
from .common import create_dashboard_history_columns, Category


class HistoryEUOrphanCon(models.Model):
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
        related_name="eu_orphan_con",
    )

    change_date = models.DateField(
        null=False,
        blank=False,
    )

    eu_orphan_con = create_dashboard_history_columns(
        models.TextField(
            null=False,
            blank=False,
        ),
        Category.General_Information,
        "string",
        "History EU orphan conditions",
    )

    class Meta:
        db_table = "history_eu_orphan_con"
