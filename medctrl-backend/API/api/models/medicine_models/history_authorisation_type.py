# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .medicinal_product import MedicinalProduct
from .common import create_dashboard_history_columns, Category, AutTypes


class HistoryAuthorisationType(models.Model):
    """
    This is the model class for the Authorisation Type history table. New attributes can be added here.
    This model is derived from a base model from the Django library.

    Attributes:
        eu_pnumber (models.ForeignKey):
            Foreign Key to the :py:class:`.MedicinalProduct` model
        change_date (models.DateField):
            DateField containing the date of the entry.
        eu_aut_type (models.CharField):
            CharField containing the authorisation type. Restricted by the options from :py:class:`.AutTypes`
            Initial and current shown on the dashboard.
    """
    eu_pnumber = models.ForeignKey(
        MedicinalProduct,
        models.CASCADE, 
        null=False,
        related_name="eu_aut_type",
    )

    change_date = models.DateField(
        null=False,
    )

    eu_aut_type = create_dashboard_history_columns(
        models.CharField(
            max_length=11,
            choices=AutTypes.choices,
            null=False,
            blank=False,
        ),
        Category.General_Information,
        "string",
        "EU Authorisation Type",
    )

    class Meta:
        db_table = "history_authorisation_type"
