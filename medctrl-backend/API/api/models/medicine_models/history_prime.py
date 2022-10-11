# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models


class HistoryPrime(models.Model):
    """
    Model class for the prime designation history table.
    """
    eu_prime_id = create_dashboard_column(
        models.IntegerField(db_column="eu_prime_id", primary_key=True, null=False),
        Category.General_Information,
        "number",
        "EU Priority Medicine ID"
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

    eu_prime = create_dashboard_column(
        models.BooleanField(db_column="eu_prime", null=True),
        Category.General_Information,
        "bool",
        "EU Priority Medicine"
    )

    class Meta:
        db_table = "history_prime"

