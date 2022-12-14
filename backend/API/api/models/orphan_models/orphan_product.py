# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from api.models.human_models.medicinal_product import MedicinalProduct
from api.models.create_dashboard_columns import (
    create_dashboard_column,
    create_dashboard_history_foreign_key_column,
    Category,
)
from api.models.common import DataFormats
from api.models.na_fields import DateWithNAField, URLWithNAField


class OrphanProduct(models.Model):
    """
    This is the model class for the Orphan Product table. New attributes can be added here.
    This model is derived from a base model from the Django library.

    Attributes:
        eu_od_number (models.CharField):
            CharField containing the EU orphan designation number. Shown on the dashboard.
        omar_url (URLWithNAField):
            URLField containing an url to the orphan maintenance assessment report. Shown on the dashboard.
        odwar_url (URLWithNAField):
            URLField containing an url to the orphan designation withdrawal assessment report. Shown on the dashboard.
        eu_pnumber (models.ForeignKey):
            Foreign Key to the :py:class:`.MedicinalProduct` model. Optional. Shown on the dashboard.
        ema_od_number (models.CharField):
            CharField containing the EMA orphan designation number. Shown on the dashboard.
        eu_od_con (models.TextField):
            TextField containing the EU orphan designation condition. Shown on the dashboard.
        eu_od_date (models.DateField):
            DateField containing the EU orphan designation date. Shown on the dashboard.
        eu_od_comp_date (models.DateField):
            DateField containing the EU orphan designation COMP decision date. Shown on the dashboard.
        eu_od_sponsor (models.TextField):
            TextField containing the EU orphan designation sponsor. Shown on the dashboard.
        eu_orphan_con_initial (models.OneToOneField):
            Unique Foreign Key to the initial item in the :py:class:`.HistoryEUOrphanCon` model. Shown on the dashboard.
    """
    eu_od_number = create_dashboard_column(
        models.CharField(
            max_length=255,
            primary_key=True,
            null=False,
            blank=False,
        ),
        Category.Orphan_product,
        DataFormats.String,
        "EU orphan designation number",
    )

    omar_url = create_dashboard_column(
        URLWithNAField(),
        Category.Orphan_product,
        DataFormats.Link,
        "URL to orphan maintenance assessment report",
    )

    odwar_url = create_dashboard_column(
        URLWithNAField(),
        Category.Orphan_product,
        DataFormats.Link,
        "URL to orphan designation withdrawal assessment report",
    )

    eu_od_pnumber = models.ForeignKey(
        MedicinalProduct,
        models.CASCADE,
        null=True,
        related_name="eu_od_pnumber",
    )

    ema_od_number = create_dashboard_column(
        models.CharField(
            max_length=255,
            null=False
        ),
        Category.Orphan_product,
        DataFormats.String,
        "EMA orphan designation number",
    )

    eu_od_con = create_dashboard_column(
        models.TextField(
            null=False
        ),
        Category.Orphan_product,
        DataFormats.String,
        "EU orphan designation condition",
    )

    eu_od_date = create_dashboard_column(
        DateWithNAField(),
        Category.Orphan_product,
        DataFormats.Date,
        "EU orphan designation date",
    )

    eu_od_comp_date = create_dashboard_column(
        DateWithNAField(),
        Category.Orphan_product,
        DataFormats.Date,
        "COMP decision date (for EU orphan designation)",
    )

    eu_orphan_con_initial = create_dashboard_history_foreign_key_column(
        models.ForeignKey(
            "HistoryEUOrphanCon",
            models.SET_NULL,
            null=True,
            blank=True,
            related_name="eu_orphan_con_initial"
        ),
        Category.Medicinal_product,
        DataFormats.Dictionary_List,
        "Initial EU orphan conditions",
    )

    class Meta:
        db_table = "orphan_product"
        verbose_name = "Orphan Product"
        verbose_name_plural = "Orphan Products"
