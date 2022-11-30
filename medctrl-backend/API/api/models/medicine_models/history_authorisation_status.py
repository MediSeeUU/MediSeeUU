# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .medicinal_product import MedicinalProduct
from api.models.create_dashboard_columns import create_dashboard_history_current_column, Category
from api.models.common import AutStatus


class HistoryAuthorisationStatus(models.Model):
    """
    This is the model class for the Authorisation Status history table. New attributes can be added here.
    This model is derived from a base model from the Django library.

    Attributes:
        eu_pnumber (models.ForeignKey):
            Foreign Key to the :py:class:`.MedicinalProduct` model
        change_date (models.DateField):
            DateField containing the date of the entry.
        eu_aut_status (models.CharField):
            CharField containing the authorisation status. Restricted by the options from :py:class:`.AutStatus`
            Current shown on the dashboard.
    """
    eu_pnumber = models.ForeignKey(
        MedicinalProduct,
        models.CASCADE,
        null=False,
        blank=False,
        related_name="eu_aut_status",
    )

    change_date = models.DateField(
        null=False,
        blank=False,
    )

    eu_aut_status = create_dashboard_history_current_column(
        models.CharField(
            max_length=10,
            choices=AutStatus.choices,
            null=False,
            blank=False,
        ),
        Category.General_Information,
        "string",
        "EU Authorisation Status",
        None,
        None,
    )

    class Meta:
        db_table = "history_authorisation_status"
