# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .common import create_dashboard_column, Category


class HistoryBrandName(models.Model):
    """
    Model class for the brand name history table.
    """
    eu_brand_name_id = create_dashboard_column(
        models.IntegerField(db_column="eu_brand_name_id", primary_key=True, null=False),
        Category.General_Information,
        "number",
        "EU Brand Number ID"
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

    eu_brand_name = create_dashboard_column(
        models.TextField(db_column="eu_brand_name"),
        Category.General_Information,
        "string",
        "EU Brand Name"
    )

    class Meta:
        db_table = "history_brand_name"
