# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .common import create_dashboard_column, Category

class Medicine(models.Model):
    """
    Model class for the medicine table.
    """
    eu_pnumber = create_dashboard_column(
        models.CharField(db_column="eu_pnumber", max_length=255, primary_key=True, null=False),
        Category.General_Information,
        "string",
        "EU Product Number"
    )

    active_substance = create_dashboard_column(
        models.TextField(db_column="active_substance", null=False),
        Category.General_Information,
        "string",
        "Active Substance"
    )

    eu_nas = create_dashboard_column(
        models.BooleanField(db_column="eu_nas", null=True),
        Category.General_Information,
        "bool",
        "EU New Active Substance"
    )

    ema_procedure_start_initial = create_dashboard_column(
        models.DateField(db_column="ema_procedure_start_initial", null=False),
        Category.General_Information,
        "date",
        "Initial EMA Procedure Start Date"
    )

    chmp_opinion_date = create_dashboard_column(
        models.DateField(db_column="chmp_opinion_date", null=False),
        Category.General_Information,
        "date",
        "Initial EMA (CHMP) Opinion Date"
    )

    eu_aut_date = create_dashboard_column(
        models.DateField(db_column="eu_aut_date", null=False),
        Category.General_Information,
        "date",
        "Initial EU Authorisation Date"
    )

    eu_legal_basis = create_dashboard_column(
        models.CharField(db_column="eu_legal_basis", max_length=14, choices=LegalBases.choices),
        Category.General_Information,
        "string",
        "EU Legal Basis"
    )

    ema_url = create_dashboard_column(
        models.URLField(db_column="ema_url", null=False),
        Category.General_Information,
        "link",
        "EMA Product Page Link"
    )

    ec_url = create_dashboard_column(
        models.URLField(db_column="ec_url", null=False),
        Category.General_Information,
        "link",
        "EC Product Page Link"
    )

    ema_number = create_dashboard_column(
        models.CharField(db_column="ema_number", max_length=255, null=False),
        Category.General_Information,
        "string",
        "EMA Application Number"
    )

    eu_med_type = create_dashboard_column(
        models.TextField(db_column="eu_med_type", null=False),
        Category.General_Information,
        "string",
        "EU Medicine Type"
    )

    eu_atmp = create_dashboard_column(
        models.BooleanField(db_column="eu_atmp", null=True),
        Category.General_Information,
        "bool",
        "EU ATMP"
    )

    class Meta:
        db_table = "medicine"
