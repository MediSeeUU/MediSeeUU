# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .common import create_dashboard_column, Category


class HistoryEUOrphanCon(models.Model):
    """
    Model class for the eu orphan conditions history table.
    """
    eu_pnumber = models.ForeignKey("Medicine", models.CASCADE, db_column="eu_pnumber", null=False)

    change_date = models.DateField(db_column="change_date", null=True)

    eu_orphan_con = create_dashboard_column(
        models.TextField(db_column="eu_orphan_con", null=False),
        Category.General_Information,
        "string",
        "History EU orphan conditions"
    )

    class Meta:
        db_table = "history_eu_orphan_con"
