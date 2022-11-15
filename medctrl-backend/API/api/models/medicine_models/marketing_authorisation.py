# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .medicinal_product import MedicinalProduct
from .accelerated_assessment import AcceleratedAssessment
from .duration import Duration
from .common import create_dashboard_column, Category


class MarketingAuthorisation(models.Model):
    eu_pnumber = models.OneToOneField(
        MedicinalProduct,
        models.CASCADE,
        primary_key=True,
        null=False,
        blank=False,
        related_name="marketing_authorisation",
    )

    ema_procedure_start_initial = create_dashboard_column(
        models.DateField(
            null=False,
        ),
        Category.General_Information,
        "date",
        "Initial EMA Procedure Start Date",
    )

    chmp_opinion_date = create_dashboard_column(
        models.DateField(
            null=False,
        ),
        Category.General_Information,
        "date",
        "Initial EMA (CHMP) Opinion Date",
    )

    eu_aut_date = create_dashboard_column(
        models.DateField(
            null=False,
        ),
        Category.General_Information,
        "date",
        "Initial EU Authorisation Date",
    )

    aut_url = create_dashboard_column(
        models.URLField(
            null=False,
        ),
        Category.General_Information,
        "link",
        "Authorisation Decision Link",
    )

    smpc_url = create_dashboard_column(
        models.URLField(
            null=False,
        ),
        Category.General_Information,
        "link",
        "Authorisation Annex Link",
    )

    epar_url = create_dashboard_column(
        models.URLField(
            null=False,
        ),
        Category.General_Information,
        "link",
        "Initial Authorisation EPAR Link",
    )

    ema_rapp = create_dashboard_column(
        models.TextField(
            null=False,
        ),
        Category.General_Information,
        "string",
        "EMA rapporteur for initial authorisation",
    )

    ema_corapp = create_dashboard_column(
        models.TextField(
            null=False,
        ),
        Category.General_Information,
        "string",
        "EMA co-rapporteur for initial authorisation",
    )

    ema_accelerated_assessment = models.OneToOneField(
        AcceleratedAssessment,
        models.CASCADE,
    )

    duration = models.OneToOneField(
        Duration,
        models.CASCADE,
    )

    ema_reexamination = create_dashboard_column(
        models.BooleanField(
            null=False,
        ),
        Category.General_Information,
        "bool",
        "EMA re-examination performed",
    )

    class Meta:
        db_table = "marketing_authorisation"
