# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models


class HistoryAuthorisationStatus(models.Model):
    """
    Model class for the authorisation history table.
    """
    eu_aut_status_id = create_dashboard_column(
        models.IntegerField(db_column="eu_aut_status_id", primary_key=True, null=False),
        Category.General_Information,
        "number",
        "EU Authorisation Status ID"
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

    eu_aut_status = create_dashboard_column(
        models.CharField(db_column="eu_aut_status", max_length=10, choices=AutStatus.choices),
        Category.General_Information,
        "string",
        "EU Authorisation Status"
    )

    class Meta:
        db_table = "history_authorisation_status"
