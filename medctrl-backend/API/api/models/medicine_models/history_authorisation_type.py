# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models


class HistoryAuthorisationType(models.Model):
    """
    Model class for the authorisation history table.
    """
    eu_aut_type_id = create_dashboard_column(
        models.IntegerField(db_column="eu_aut_type_id", primary_key=True, null=False),
        Category.General_Information,
        "number",
        "EU Authorisation Type ID"
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

    eu_aut_type = create_dashboard_column(
        models.CharField(db_column="eu_aut_type", max_length=11, choices=AutTypes.choices),
        Category.General_Information,
        "string",
        "EU Authorisation Type"
    )

    class Meta:
        db_table = "history_authorisation_type"
