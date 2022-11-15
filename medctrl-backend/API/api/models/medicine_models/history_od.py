# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .medicinal_product import MedicinalProduct
from .common import create_dashboard_history_column_initial, Category


class HistoryOD(models.Model):
    """
    This is the model class for the Orphan Designation history table. New attributes can be added here.
    This model is derived from a base model from the Django library.
    """
    eu_pnumber = models.ForeignKey(
        MedicinalProduct,
        models.CASCADE, 
        null=False,
        blank=False,
    )

    change_date = models.DateField(
        null=False,
        blank=False,
    )

    eu_od = create_dashboard_history_column_initial(
        models.BooleanField(
            null=False,
            blank=False,
        ),
        Category.General_Information,
        "bool",
        "EU Orphan Designation",
    )

    class Meta:
        db_table = "history_od"
