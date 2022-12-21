# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from api.models.human_models import MedicinalProduct
from api.models.create_dashboard_columns import create_dashboard_history_current_column, Category
from api.models.common import DataFormats


class HistoryEUOrphanCon(models.Model):
    """
    This is the model class for the Orphan Condition history table. New attributes can be added here.
    This model is derived from a base model from the Django library.

    Attributes:
        eu_pnumber (models.ForeignKey):
            Foreign Key to the :py:class:`.MedicinalProduct` model
        change_date (models.DateField):
            DateField containing the date of the entry.
        eu_orphan_con (models.TextField):
            TextField containing the EU orphan condition. Initial and current shown on the dashboard.
    """
    eu_pnumber = models.ForeignKey(
        MedicinalProduct,
        models.CASCADE,
        null=False,
        blank=False,
        related_name="eu_orphan_con",
    )

    change_date = models.DateField(
        null=False,
        blank=False,
    )

    eu_orphan_con = create_dashboard_history_current_column(
        models.TextField(
            null=False,
            blank=False,
        ),
        Category.Medicinal_product,
        DataFormats.String,
        "History EU orphan conditions",
    )

    class Meta:
        db_table = "history_eu_orphan_con"
