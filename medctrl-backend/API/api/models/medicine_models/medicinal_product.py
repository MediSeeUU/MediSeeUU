# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .common import create_dashboard_column, Category
from .ingredients_and_substances import IngredientsAndSubstances


class MedicinalProduct(models.Model):
    """
    This is the model class for the Medicinal Product table. New attributes can be added here.
    This model is derived from a base model from the Django library.

    Attributes:
        eu_pnumber (models.CharField):
            CharField containing the EU Number. Used as the primary key and shown on the dashboard.
        ema_url (models.URLField):
            URLField containing an url to the ema website. Shown on the dashboard.
        ec_url (models.URLField):
            URLField containing an url to the ec website. Shown on the dashboard.
        ema_number (models.CharField):
            CharField containing the EMA Number. Shown on the dashboard.
        eu_med_type (models.CharField):
            CharField containing the medicine type. Shown on the dashboard.
        eu_atmp (models.BooleanField):
            BooleanField which indicates if this medicine is an ATMP. Shown on the dashboard.
        ema_number_check (models.BooleanField):
            BooleanField containing the EMA Number Check. Not shown on the dashboard.
        ingredients_and_substances (models.ForeignKey):
            ForeignKey to the :py:class:`.IngredientsAndSubstances` model

    """    
    eu_pnumber = create_dashboard_column(
        models.CharField(
            max_length=255,
            primary_key=True,
            null=False,
            blank=False,
        ),
        Category.General_Information,
        "string",
        "EU Product Number",
    )

    ema_url = create_dashboard_column(
        models.URLField(),
        Category.General_Information,
        "link",
        "EMA Product Page Link",
    )

    ec_url = create_dashboard_column(
        models.URLField(),
        Category.General_Information,
        "link",
        "EC Product Page Link",
    )

    ema_number = create_dashboard_column(
        models.CharField(
            max_length=255,
        ),
        Category.General_Information,
        "string",
        "EMA Application Number",
    )

    eu_med_type = create_dashboard_column(
        models.TextField(),
        Category.General_Information,
        "string",
        "EU Medicine Type",
    )

    eu_atmp = create_dashboard_column(
        models.BooleanField(
            null=True,
        ),
        Category.General_Information,
        "bool",
        "EU ATMP",
    )

    ema_number_check = models.BooleanField(
        null=True,
    )

    ingredients_and_substances = models.ForeignKey(
        IngredientsAndSubstances,
        models.CASCADE,
    )

    class Meta:
        db_table = "medicinal_product"
