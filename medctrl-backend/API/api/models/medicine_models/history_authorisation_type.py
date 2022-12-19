# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .common import create_dashboard_history_columns, Category, AutTypes


class HistoryAuthorisationType(models.Model):
    """
    This is the model class for the Authorisation Type history table. New attributes can be added here.
    This model is derived from a base model from the Django library.
    """
    eu_pnumber = models.ForeignKey(
        "Medicine", 
        models.CASCADE, 
        db_column="eu_pnumber", 
        null=False
    )

    change_date = models.DateField(
        db_column="change_date", 
        null=True
    )

    eu_aut_type = create_dashboard_history_columns(
        models.CharField(db_column="eu_aut_type", max_length=11, choices=AutTypes.choices),
        Category.Marketing_Authorisation,
        "string",
        "EU Authorisation Type"
    )

    class Meta:
        db_table = "history_authorisation_type"
