# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from api.models.orphan_models import OrphanProduct
from api.models.create_dashboard_columns import (
    Category,
)
from api.models.common import (
    DataFormats,
)
from api.models.na_fields import DateWithNAField
from api.models.other import LockModel


class HistoryEUOrphanCon(LockModel):
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

    link_date = DateWithNAField()

    end_date = DateWithNAField()

    indication = models.TextField(
        null=False,
        blank=False,
    )

    class Meta:
        db_table = "history_eu_orphan_con"
        verbose_name = "History EU Orphan Con"
        verbose_name_plural = "Histories EU Orphan Con"

    class HistoryInfo:
        dashboard_columns = [
            {
                "category": Category.Medicinal_product,
                "data-key": "eu_orphan_con_current",
                "data-format": DataFormats.Dictionary_List,
                "data-value": "Status of EU orphan designations",
            }
        ]
        timeline_items = [
            {
                "category": Category.Medicinal_product,
                "data-key": "eu_orphan_con",
                "data-format": DataFormats.Dictionary_List,
                "data-value": "EU orphan conditions",
            },
            {
                "category": Category.Orphan_product,
                "data-key": "eu_orphan_con",
                "data-format": DataFormats.Dictionary,
                "data-value": "EU orphan conditions",
            }
        ]

    def __str__(self):
        return f"EUOrphanCon<{self.indication}> History Item"
