# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .medicinal_product import MedicinalProduct
from .common import create_dashboard_column, Category, AutStatus


class HistoryAuthorisationStatus(models.Model):
    """
    This is the model class for the Authorisation Status history table. New attributes can be added here.
    This model is derived from a base model from the Django library.
    """
    eu_pnumber = models.ForeignKey(
        MedicinalProduct,
        models.CASCADE,
        null=False,
        blank=False,
    )

    change_date = models.DateField(
        db_column="change_date", 
        null=False,
        blank=False,
    )

    eu_aut_status = create_dashboard_column(
        models.CharField(
            db_column="eu_aut_status",
            max_length=10,
            choices=AutStatus.choices,
            null=False,
            blank=False,
        ),
        Category.General_Information,
        "string",
        "EU Authorisation Status",
    )

    class Meta:
        db_table = "history_authorisation_status"
