# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .common import create_dashboard_column, Category


class HistoryATCCode(models.Model):
    """
    Model class for the MAH history table.
    """
    atc_code_id = create_dashboard_column(
        models.IntegerField(db_column="atc_code_id", primary_key=True, null=False),
        Category.General_Information,
        "number",
        "ATC Code ID"
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

    atc_code = create_dashboard_column(
        models.CharField(db_column="atc_code", max_length=7),
        Category.General_Information,
        "string",
        "ATC Code"
    )

    class Meta:
        db_table = "history_atc_code"
