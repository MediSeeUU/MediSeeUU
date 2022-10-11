# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .common import create_dashboard_column, Category, NotVarCharField, AutTypes, LegalBases


# Tijdelijk alles in de general_information category gestopt

class Medisee(models.Model):
    atc_code = create_dashboard_column(
        models.CharField(db_column="atc_code", max_length=7, null=False),
        Category.General_Information,
        "string",
        "ATC code"
    )

    active_substance = create_dashboard_column(
        models.TextField(db_column="active_substance", null=False),
        Category.General_Information,
        "string",
        "Active substance"
    )

    eu_nas = create_dashboard_column(
        models.BooleanField(db_column="eu_nas", null=True),
        Category.General_Information,
        "bool",
        "EU new active substance"
    )

    ema_procedure_start_initial = create_dashboard_column(
        models.DateField(db_column="ema_procedure_start_initial", null=False),
        Category.General_Information,
        "date",
        "Initial EMA procedure start date"
    )

    chmp_opinion_date = create_dashboard_column(
        models.DateField(db_column="chmp_opinion_date", null=False),
        Category.General_Information,
        "date",
        "Initial EMA (CHMP) opinion date"
    )

    eu_aut_date = create_dashboard_column(
        models.DateField(db_column="eu_aut_date", null=False),
        Category.General_Information,
        "date",
        "Initial EU authorisation date"
    )

    eu_aut_type_initial = create_dashboard_column(
        NotVarCharField(db_column="eu_aut_type_initial", max_length=1, choices=AutTypes.choices),
        Category.General_Information,
        "string",
        "Initial type of EU authorisation"
    )

    eu_brand_name_initial = create_dashboard_column(
        models.TextField(db_column="eu_brand_name_initial", null=False),
        Category.General_Information,
        "string",
        "Initial EU brand name"
    )

    eu_pnumber = create_dashboard_column(
        models.CharField(db_column="eu_pnumber", max_length=255, primary_key=True, null=False),
        Category.General_Information,
        "string",
        "EU product number"
    )

    eu_pnumber_id = create_dashboard_column(
        models.PositiveSmallIntegerField(db_column="eu_pnumber_id", null=False),
        Category.General_Information,
        "number",
        "EU product number ID"
    )

    eu_legal_basis = create_dashboard_column(
        models.CharField(db_column="eu_legal_basis", max_length=14, choices=LegalBases.choices),
        Category.General_Information,
        "string",
        "EU legal basis"
    )

    aut_url = create_dashboard_column(
        models.URLField(db_column="aut_url", null=False),
        Category.General_Information,
        "link",
        "URL to EU authorisation decision"
    )

    smpc_url = create_dashboard_column(
        models.URLField(db_column="smpc_url", null=False),
        Category.General_Information,
        "link",
        "URL to EU authorisation annex"
    )

    epar_url = create_dashboard_column(
        models.URLField(db_column="epar_url", null=False),
        Category.General_Information,
        "link",
        "URL to EMA initial authorisation EPAR"
    )

    eu_atmp = create_dashboard_column(
        models.BooleanField(db_column="eu_atmp", null=True),
        Category.General_Information,
        "bool",
        "EU ATMP"
    )

    eu_med_type = create_dashboard_column(
        models.TextField(db_column="eu_med_type", null=False),
        Category.General_Information,
        "string",
        "EU type of medicine"
    )

    # R23 EU AUT STATUS NOG missing

    eu_brand_name = create_dashboard_column(
        models.TextField(db_column="eu_brand_name", null=False),
        Category.General_Information,
        "string",
        "EU brand name"
    )

    eu_brand_name_history = create_dashboard_column(
        models.TextField(db_column="eu_brand_name_history", null=False),
        Category.General_Information,
        "string",
        "History of EU brand names"
    )

    ema_number = create_dashboard_column(
        models.CharField(db_column="ema_number", max_length=255, null=False),
        Category.General_Information,
        "string",
        "EMA application number"
    )

    ema_number_id = create_dashboard_column(
        models.PositiveSmallIntegerField(db_column="ema_number_id", null=False),
        Category.General_Information,
        "number",
        "EMA application number ID"
    )

    ema_number_certainty = create_dashboard_column(
        models.FloatField(db_column="ema_number_certainty", null=False),
        Category.General_Information,
        "number",
        "EMA application number certainty"
    )

    # ema_number_check nog doen R30

    eu_mah = create_dashboard_column(
        models.CharField(db_column="eu_mah", max_length=255, null=False),
        Category.General_Information,
        "string",
        "EU marketing authorisation holder"
    )

    eu_mah_initial = create_dashboard_column(
        models.CharField(db_column="eu_mah_initial", max_length=255, null=False),
        Category.General_Information,
        "string",
        "Initial EU marketing authorisation holder"
    )

    eu_prime_initial = create_dashboard_column(
        models.BooleanField(db_column="eu_prime_initial", null=True),
        Category.General_Information,
        "bool",
        "EU Priority Medicine at authorisation"
    )

    eu_od_initial = create_dashboard_column(
        models.BooleanField(db_column="eu_od_initial", null=True),
        Category.General_Information,
        "bool",
        "EU orphan designation at authorisation"
    )

    ema_url = create_dashboard_column(
        models.URLField(db_column="ema_url", null=False),
        Category.General_Information,
        "link",
        "URL to EMA medicinal product page"
    )

    ec_url = create_dashboard_column(
        models.URLField(db_column="ec_url", null=False),
        Category.General_Information,
        "link",
        "URL to EC medicinal product page"
    )
    class Meta:
        db_table = "medisee"
