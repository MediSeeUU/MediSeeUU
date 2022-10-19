# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .common import create_dashboard_history_columns, Category


class HistoryBrandName(models.Model):
    """
    Model class for the brand name history table.
    """
    eu_pnumber = models.ForeignKey("Medicine", models.CASCADE, db_column="eu_pnumber", null=False)

    change_date = models.DateField(db_column="change_date", null=True)

    eu_brand_name = create_dashboard_history_columns(
        models.TextField(db_column="eu_brand_name"),
        Category.General_Information,
        "string",
        "EU Brand Name"
    )

    class Meta:
        db_table = "history_brand_name"
