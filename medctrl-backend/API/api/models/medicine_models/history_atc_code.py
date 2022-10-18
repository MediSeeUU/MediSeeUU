# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .common import create_dashboard_column, Category


class HistoryATCCode(models.Model):
    """
    Model class for the MAH history table.
    """
    eu_pnumber = models.ForeignKey("Medicine", models.CASCADE, db_column="eu_pnumber", null=False)

    change_date = models.DateField(db_column="change_date", null=True)

    atc_code = create_dashboard_column(
        models.CharField(db_column="atc_code", max_length=7),
        Category.General_Information,
        "string",
        "ATC Code"
    )

    class Meta:
        db_table = "history_atc_code"
