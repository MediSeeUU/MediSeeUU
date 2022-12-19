# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .common import create_dashboard_history_column_initial, Category


class HistoryOD(models.Model):
    """
    This is the model class for the Orphan Designation history table. New attributes can be added here.
    This model is derived from a base model from the Django library.
    """
    eu_pnumber = models.ForeignKey(
        "Medicine", 
        models.CASCADE, 
        db_column="eu_pnumber", 
        null=False)

    change_date = models.DateField(db_column="change_date", null=True)

    eu_od = create_dashboard_history_column_initial(
        models.BooleanField(db_column="eu_od", null=True),
        Category.Marketing_Authorisation,
        "bool",
        "EU Orphan Designation"
    )

    class Meta:
        db_table = "history_od"
