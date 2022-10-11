# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .common import create_dashboard_column, Category

class HistoryEMANumberCheck(models.Model):
    """
    Model class for the identication history table.
    """
    ema_number_check_id = create_dashboard_column(
        models.IntegerField(db_column="ema_number_check_id", primary_key=True, null=False),
        Category.General_Information,
        "number",
        "EMA Number Check ID"
    )

    eu_pnumber = create_dashboard_column(
        models.ForeignKey("Medicine", models.CASCADE, db_column="eu_pnumber", null=False),
        Category.General_Information,
        "number",
        "EU Product Number"
    )

    change_date = create_dashboard_column(
        models.DateField(db_column="change_date", null=True),
        Category.General_Information,
        "date",
        "Change Date"
    )

    ema_number_check = create_dashboard_column(
        models.BooleanField(db_column="eu_number_check", null=True),
        Category.General_Information,
        "bool",
        "EMA Number Check"
    )

    class Meta:
        db_table = "history_number_check"