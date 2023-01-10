# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from django.dispatch import receiver
from .medicinal_product import MedicinalProduct
from .accelerated_assessment import AcceleratedAssessment
from .duration import Duration
from .history_authorisation_type import HistoryAuthorisationType
from .history_mah import HistoryMAH
from api.models.create_dashboard_columns import (
    create_dashboard_column,
    create_dashboard_history_foreign_key_column,
    Category,
)
from api.models.common import (
    DataFormats,
)
from api.models.na_fields import BooleanWithNAField, DateWithNAField, URLWithNAField
from api.models.other import LockModel


class MarketingAuthorisation(LockModel):
    """
    This is the model class for the Marketing Authorisation table. New attributes can be added here.
    This model is derived from a base model from the Django library.

    Attributes:
        eu_pnumber (models.OneToOneField):
            Unique Foreign Key to the :py:class:`.MedicinalProduct` model
        ema_procedure_start_initial (models.DateField):
            DateField containing the date the EMA procedure started. Shown on the dashboard.
        chmp_opinion_date (models.DateField):
            DateField containing the date of the CHMP opinion. Shown on the dashboard.
        eu_aut_date (models.DateField):
            DateField containing the date of the EU authorisation. Shown on the dashboard.
        aut_url (URLWithNAField):
            URLField containing an url to the authorisation decision. Shown on the dashboard.
        smpc_url (URLWithNAField):
            URLField containing an url to the SMPC. Shown on the dashboard.
        epar_url (URLWithNAField):
            URLField containing an url to EPAR. Shown on the dashboard.
        ema_rapp (models.TextField):
            TextField containing the EMA rapporteur. Shown on the dashboard.
        ema_corapp (models.TextField):
            TextField containing the EMA co-rapporteur. Shown on the dashboard.
        ema_accelerated_assessment (models.OneToOneField):
            Unique Foreign Key to the :py:class:`.AcceleratedAssessment` model
        duration (models.OneToOneField):
            Unique Foreign Key to the :py:class:`.Duration` model
        ema_reexamination (BooleanWithNAField):
            BooleanWithNAField indicating if the EMA re-examination has been performed. Shown on the dashboard.
        eu_aut_type_initial (models.OneToOneField):
            Unique Foreign Key to the initial item in the :py:class:`.HistoryAuthorisationType` model.
            Shown on the dashboard.
        eu_mah_initial (models.OneToOneField):
            Unique Foreign Key to the initial item in the :py:class:`.HistoryMAH` model.
            Shown on the dashboard.
    """
    eu_pnumber = models.OneToOneField(
        MedicinalProduct,
        models.CASCADE,
        primary_key=True,
        null=False,
        blank=False,
        related_name="marketing_authorisation",
    )

    ema_procedure_start_initial = create_dashboard_column(
        DateWithNAField(),
        Category.Marketing_authorisation,
        DataFormats.Date,
        "Initial EMA Procedure Start Date",
    )

    chmp_opinion_date = create_dashboard_column(
        DateWithNAField(),
        Category.Marketing_authorisation,
        DataFormats.Date,
        "Initial EMA (CHMP) Opinion Date",
    )

    eu_aut_date = create_dashboard_column(
        DateWithNAField(),
        Category.Marketing_authorisation,
        DataFormats.Date,
        "Initial EU Authorisation Date",
    )

    aut_url = create_dashboard_column(
        URLWithNAField(),
        Category.Marketing_authorisation,
        DataFormats.Link,
        "Authorisation Decision Link",
    )

    smpc_url = create_dashboard_column(
        URLWithNAField(),
        Category.Marketing_authorisation,
        DataFormats.Link,
        "Authorisation Annex Link",
    )

    epar_url = create_dashboard_column(
        URLWithNAField(),
        Category.Marketing_authorisation,
        DataFormats.Link,
        "Initial Authorisation EPAR Link",
    )

    ema_rapp = create_dashboard_column(
        models.TextField(
            null=True,
            blank=True,
        ),
        Category.Marketing_authorisation,
        DataFormats.String,
        "EMA rapporteur for initial authorisation",
    )

    ema_corapp = create_dashboard_column(
        models.TextField(
            null=True,
            blank=True,
        ),
        Category.Marketing_authorisation,
        DataFormats.String,
        "EMA co-rapporteur for initial authorisation",
    )

    ema_accelerated_assessment = models.OneToOneField(
        AcceleratedAssessment,
        models.PROTECT,
    )

    duration = models.OneToOneField(
        Duration,
        models.PROTECT,
    )

    ema_reexamination = create_dashboard_column(
        BooleanWithNAField(),
        Category.Marketing_authorisation,
        DataFormats.Bool,
        "EMA re-examination performed",
    )

    eu_aut_type_initial = create_dashboard_history_foreign_key_column(
        models.OneToOneField(
            HistoryAuthorisationType,
            models.SET_NULL,
            null=True,
            blank=True,
        ),
        Category.Marketing_authorisation,
        DataFormats.String,
        "Initial type of EU authorisation",
    )

    eu_mah_initial = create_dashboard_history_foreign_key_column(
        models.OneToOneField(
            HistoryMAH,
            models.SET_NULL,
            null=True,
            blank=True,
        ),
        Category.Marketing_authorisation,
        DataFormats.String,
        "Initial EU marketing authorisation holder",
    )

    class Meta:
        db_table = "marketing_authorisation"
        verbose_name = "Marketing Authorisation"
        verbose_name_plural = "Marketing Authorisations"

    def __str__(self):
        return self.eu_pnumber.__str__()

    def delete(self, *args, **kwargs):
        if self.duration:
            self.duration.delete()
        if self.ema_accelerated_assessment:
            self.ema_accelerated_assessment.delete()
        super().delete(*args, **kwargs)


@receiver(models.signals.post_delete, sender=MarketingAuthorisation)
def handle_deleted_marketing__authorisation(sender, instance, **kwargs):
    if instance.duration:
        instance.duration.delete()
    if instance.ema_accelerated_assessment:
        instance.ema_accelerated_assessment.delete()
