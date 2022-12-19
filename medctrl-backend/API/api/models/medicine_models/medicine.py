# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .common import create_dashboard_column, Category


class Medicine(models.Model):
    """
    This is the model class for the Medicine table. New attributes can be added here.
    This model is derived from a base model from the Django library.
    """    
    eu_pnumber = create_dashboard_column(
        models.CharField(db_column="eu_pnumber", max_length=255, primary_key=True, null=False),
        Category.Marketing_Authorisation,
        "string",
        "EU Product Number"
    )

    atc_code = create_dashboard_column(
        models.CharField(db_column="atc_code", max_length=7),
        Category.Medicinal_Product,
        "string",
        "ATC Code"
    )

    active_substance = create_dashboard_column(
        models.TextField(db_column="active_substance", null=False),
        Category.Ingredients_and_Substances,
        "string",
        "Active Substance"
    )

    eu_nas = create_dashboard_column(
        models.BooleanField(db_column="eu_nas", null=True),
        Category.Ingredients_and_Substances,
        "bool",
        "EU New Active Substance"
    )

    ema_procedure_start_initial = create_dashboard_column(
        models.DateField(db_column="ema_procedure_start_initial", null=False),
        Category.Marketing_Authorisation,
        "date",
        "Initial EMA Procedure Start Date"
    )

    chmp_opinion_date = create_dashboard_column(
        models.DateField(db_column="chmp_opinion_date", null=False),
        Category.Marketing_Authorisation,
        "date",
        "Initial EMA (CHMP) Opinion Date"
    )

    eu_aut_date = create_dashboard_column(
        models.DateField(db_column="eu_aut_date", null=False),
        Category.Marketing_Authorisation,
        "date",
        "Initial EU Authorisation Date"
    )

    ema_url = create_dashboard_column(
        models.URLField(db_column="ema_url", null=False),
        Category.Medicinal_Product,
        "link",
        "EMA Product Page Link"
    )

    ec_url = create_dashboard_column(
        models.URLField(db_column="ec_url", null=False),
        Category.Medicinal_Product,
        "link",
        "EC Product Page Link"
    )

    ema_number = create_dashboard_column(
        models.CharField(db_column="ema_number", max_length=255, null=False),
        Category.Medicinal_Product,
        "string",
        "EMA Application Number"
    )

    eu_med_type = create_dashboard_column(
        models.TextField(db_column="eu_med_type", null=False),
        Category.Medicinal_Product,
        "string",
        "EU Medicine Type"
    )

    eu_atmp = create_dashboard_column(
        models.BooleanField(db_column="eu_atmp", null=True),
        Category.Medicinal_Product,
        "bool",
        "EU ATMP"
    )

    aut_url = create_dashboard_column(
        models.URLField(db_column="aut_url", null=False),
        Category.Marketing_Authorisation,
        "link",
        "Authorisation Decision Link"
    )

    smpc_url = create_dashboard_column(
        models.URLField(db_column="smpc_url", null=False),
        Category.Marketing_Authorisation,
        "link",
        "Authorisation Annex Link"
    )

    epar_url = create_dashboard_column(
        models.URLField(db_column="epar_url", null=False),
        Category.Marketing_Authorisation,
        "link",
        "Initial Authorisation EPAR Link"
    )

    ema_number_check = create_dashboard_column(
        models.BooleanField(db_column="ema_number_check", null=True),
        Category.Marketing_Authorisation,
        "bool",
        "EMA Number Check"
    )

    ema_rapp = create_dashboard_column(
        models.TextField(db_column="ema_rapp", null=False),
        Category.Marketing_Authorisation,
        "string",
        "EMA rapporteur for initial authorisation"
    )

    ema_corapp = create_dashboard_column(
        models.TextField(db_column="ema_corapp", null=False),
        Category.Marketing_Authorisation,
        "string",
        "EMA co-rapporteur for initial authorisation"
    )

    eu_accel_assess_g = create_dashboard_column(
        models.BooleanField(db_column="eu_accel_assess_g", null=True),
        Category.Marketing_Authorisation,
        "bool",
        "EU accelerated assessment granted"
    )

    eu_accel_assess_m = create_dashboard_column(
        models.BooleanField(db_column="eu_accel_assess_m", null=True),
        Category.Marketing_Authorisation,
        "bool",
        "EU accelerated assessment maintained"
    )

    assess_time_days_total = create_dashboard_column(
        models.IntegerField(db_column="assess_time_days_total", null=False),
        Category.Marketing_Authorisation,
        "number",
        "Duration of initial EU authorisation assessment procedure (total days)"
    )

    assess_time_days_active = create_dashboard_column(
        models.IntegerField(db_column="assess_time_days_active", null=False),
        Category.Marketing_Authorisation,
        "number",
        "Duration of initial EU authorisation assessment procedure (active days)"
    )

    assess_time_days_cstop = create_dashboard_column(
        models.IntegerField(db_column="assess_time_days_cstop", null=False),
        Category.Marketing_Authorisation,
        "number",
        "Duration of initial EU authorisation assessment procedure (clock-stop days)"
    )

    ec_decision_time_days = create_dashboard_column(
        models.IntegerField(db_column="ec_decision_time_days", null=False),
        Category.Marketing_Authorisation,
        "number",
        "EC decision time (days)"
    )


    ema_reexamination = create_dashboard_column(
        models.BooleanField(db_column="ema_reexamination", null=False),
        Category.Marketing_Authorisation,
        "bool",
        "EMA re-examination performed"
    )

    eu_referral = create_dashboard_column(
        models.BooleanField(db_column="eu_referral", null=False),
        Category.Procedures,
        "bool",
        "EU referral"
    )

    eu_suspension = create_dashboard_column(
        models.BooleanField(db_column="eu_suspension", null=False),
        Category.Procedures,
        "bool",
        "EU suspension"
    )

    omar_url = create_dashboard_column(
        models.URLField(db_column="omar_url", null=False),
        Category.Orphan_Product,
        "link",
        "URL to orphan maintanance assessment report"
    )

    odwar_url = create_dashboard_column(
        models.URLField(db_column="odwar_url", null=False),
        Category.Orphan_Product,
        "link",
        "URL to orphan designation withdrawal assessment report"
    )

    eu_od_number = create_dashboard_column(
        models.CharField(db_column="eu_od_number", max_length=255, null=False),
        Category.Orphan_Product,
        "string",
        "EU orphan designation number"
    )

    ema_od_number = create_dashboard_column(
        models.CharField(db_column="ema_od_number", max_length=255, null=False),
        Category.Orphan_Product,
        "string",
        "EMA orphan designation number"
    )

    eu_od_con = create_dashboard_column(
        models.TextField(db_column="eu_od_con", null=False),
        Category.Orphan_Product,
        "string",
        "EU orphan designation condition"
    )

    eu_od_date = create_dashboard_column(
        models.DateField(db_column="eu_od_date", null=False),
        Category.Orphan_Product,
        "date",
        "EU orphan designation date"
    )

    eu_od_pnumber = create_dashboard_column(
        models.CharField(db_column="eu_od_pnumber", max_length=255, null=False),
        Category.Orphan_Product,
        "string",
        "EU product number for orphan designation"
    )

    eu_od_sponsor = create_dashboard_column(
        models.TextField(db_column="eu_od_sponsor", null=False),
        Category.Orphan_Product,
        "string",
        "Sponsor for EU orphan designation"
    )

    eu_od_comp_date = create_dashboard_column(
        models.DateField(db_column="eu_od_comp_date", null=False),
        Category.Orphan_Product,
        "date",
        "COMP decision date (for EU orphan designation)"
    )

    class Meta:
        db_table = "medicine"
