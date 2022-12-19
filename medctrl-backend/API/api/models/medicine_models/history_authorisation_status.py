# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .common import create_dashboard_column, Category, AutStatus


class HistoryAuthorisationStatus(models.Model):
    """
    This is the model class for the Authorisation Status history table. New attributes can be added here.
    This model is derived from a base model from the Django library.
    """
    eu_pnumber = models.ForeignKey(
        "Medicine", 
        models.CASCADE, 
        null=False
    )

    change_date = models.DateField(
        db_column="change_date", 
        null=True
    )

    eu_aut_status = create_dashboard_column(
        models.CharField(db_column="eu_aut_status", max_length=10, choices=AutStatus.choices),
        Category.Marketing_Authorisation,
        "string",
        "EU Authorisation Status"
    )

    class Meta:
        db_table = "history_authorisation_status"
