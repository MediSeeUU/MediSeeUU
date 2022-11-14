# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from api.models.medicine_models import MedicinalProduct
from .common import create_dashboard_column, Category


class OrphanProduct(models.Model):
    eu_od_number = create_dashboard_column(
        models.CharField(db_column="eu_od_number", max_length=255, primary_key=True, null=False),
        Category.General_Information,
        "string",
        "EU orphan designation number",
    )

    omar_url = create_dashboard_column(
        models.URLField(db_column="omar_url", null=False),
        Category.General_Information,
        "link",
        "URL to orphan maintenance assessment report",
    )

    odwar_url = create_dashboard_column(
        models.URLField(db_column="odwar_url", null=False),
        Category.General_Information,
        "link",
        "URL to orphan designation withdrawal assessment report",
    )

    eu_pnumber = models.ForeignKey(
        MedicinalProduct,
        models.CASCADE,
        db_column="eu_pnumber",
    )

    ema_od_number = create_dashboard_column(
        models.CharField(db_column="ema_od_number", max_length=255, null=False),
        Category.General_Information,
        "string",
        "EMA orphan designation number",
    )

    eu_od_con = create_dashboard_column(
        models.TextField(db_column="eu_od_con", null=False),
        Category.General_Information,
        "string",
        "EU orphan designation condition",
    )

    eu_od_date = create_dashboard_column(
        models.DateField(db_column="eu_od_date", null=False),
        Category.General_Information,
        "date",
        "EU orphan designation date",
    )

    eu_od_comp_date = create_dashboard_column(
        models.DateField(db_column="eu_od_comp_date", null=False),
        Category.General_Information,
        "date",
        "COMP decision date (for EU orphan designation)",
    )

    eu_od_pnumber = create_dashboard_column(
        models.CharField(db_column="eu_od_pnumber", max_length=255, null=False),
        Category.General_Information,
        "string",
        "EU product number for orphan designation",
    )

    eu_od_sponsor = create_dashboard_column(
        models.TextField(db_column="eu_od_sponsor", null=False),
        Category.General_Information,
        "string",
        "Sponsor for EU orphan designation",
    )

    class Meta:
        db_table = "orphan_product"
