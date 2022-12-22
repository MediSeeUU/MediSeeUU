# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from api.models.create_dashboard_columns import (
    create_dashboard_column,
    create_dashboard_history_initial_column,
    Category,
    ExtraDashBoardColumn,
)
from .ingredients_and_substances import IngredientsAndSubstances
from api.models.common import DataFormats
from api.models.na_fields import BooleanWithNAField, URLWithNAField


class MedicinalProduct(models.Model):
    """
    This is the model class for the Medicinal Product table. New attributes can be added here.
    This model is derived from a base model from the Django library.

    Attributes:
        eu_pnumber (models.CharField):
            CharField containing the EU Number. Used as the primary key and shown on the dashboard.
        ema_url (URLWithNAField):
            URLField containing an url to the ema website. Shown on the dashboard.
        ec_url (URLWithNAField):
            URLField containing an url to the ec website. Shown on the dashboard.
        ema_number (models.CharField):
            CharField containing the EMA Number. Shown on the dashboard.
        eu_med_type (models.CharField):
            CharField containing the medicine type. Shown on the dashboard.
        eu_atmp (BooleanWithNAField):
            BooleanWithNAField which indicates if this medicine is an ATMP. Shown on the dashboard.
        ema_number_check (BooleanWithNAField):
            BooleanWithNAField containing the EMA Number Check. Not shown on the dashboard.
        ingredients_and_substances (models.ForeignKey):
            ForeignKey to the :py:class:`.IngredientsAndSubstances` model
        eu_brand_name_initial (models.OneToOneField):
            Unique Foreign Key to the initial item in the :py:class:`.HistoryBrandName` model. Shown on the dashboard.
        eu_od_initial (models.OneToOneField):
            Unique Foreign Key to the initial item in the :py:class:`.HistoryOD` model. Shown on the dashboard.
        eu_prime_initial (models.OneToOneField):
            Unique Foreign Key to the initial item in the :py:class:`.HistoryPrime` model. Shown on the dashboard.
    """
    eu_pnumber = create_dashboard_column(
        models.CharField(
            max_length=255,
            primary_key=True,
            null=False,
            blank=False,
        ),
        Category.Marketing_authorisation,
        DataFormats.String,
        "EU Product Number",
        [
            ExtraDashBoardColumn(
                Category.Marketing_authorisation,
                "eu_pnumber_id",
                DataFormats.Number,
                "EU product number ID",
                lambda x: int(x[-3:]),
            )
        ]
    )

    ema_url = create_dashboard_column(
        URLWithNAField(),
        Category.Medicinal_product,
        DataFormats.Link,
        "EMA Product Page Link",
    )

    ec_url = create_dashboard_column(
        URLWithNAField(),
        Category.Medicinal_product,
        DataFormats.Link,
        "EC Product Page Link",
    )

    ema_number = create_dashboard_column(
        models.CharField(
            max_length=255,
        ),
        Category.Medicinal_product,
        DataFormats.String,
        "EMA Application Number",
    )

    eu_med_type = create_dashboard_column(
        models.TextField(),
        Category.Medicinal_product,
        DataFormats.String,
        "EU Medicine Type",
    )

    eu_atmp = create_dashboard_column(
        BooleanWithNAField(
            null=True,
        ),
        Category.Medicinal_product,
        DataFormats.Bool,
        "EU ATMP",
    )

    ema_number_check = BooleanWithNAField(
        null=True,
    )

    ingredients_and_substances = models.ForeignKey(
        IngredientsAndSubstances,
        models.PROTECT,
        null=True,
    )

    eu_brand_name_initial = create_dashboard_history_initial_column(
        models.OneToOneField(
            "HistoryBrandName",
            models.SET_NULL,
            null=True,
        ),
        Category.Medicinal_product,
        DataFormats.String,
        "Initial EU brand name",
    )

    eu_od_initial = create_dashboard_history_initial_column(
        models.OneToOneField(
            "HistoryOD",
            models.SET_NULL,
            null=True,
        ),
        Category.Medicinal_product,
        DataFormats.Bool,
        "EU orphan designation at authorisation",
    )

    eu_prime_initial = create_dashboard_history_initial_column(
        models.OneToOneField(
            "HistoryPrime",
            models.SET_NULL,
            null=True,
        ),
        Category.Medicinal_product,
        DataFormats.Bool,
        "EU Priority Medicine at authorisation",
    )

    class Meta:
        db_table = "medicinal_product"
