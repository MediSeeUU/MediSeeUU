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
    """    
    eu_pnumber = create_dashboard_column(
        models.CharField(
            db_column="eu_pnumber",
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
        models.URLField(
            db_column="ema_url",
        ),
        Category.General_Information,
        "link",
        "EMA Product Page Link",
    )

    ec_url = create_dashboard_column(
        models.URLField(
            db_column="ec_url",
        ),
        Category.General_Information,
        "link",
        "EC Product Page Link",
    )

    ema_number = create_dashboard_column(
        models.CharField(
            db_column="ema_number",
            max_length=255,
        ),
        Category.General_Information,
        "string",
        "EMA Application Number",
    )

    eu_med_type = create_dashboard_column(
        models.TextField(
            db_column="eu_med_type",
        ),
        Category.General_Information,
        "string",
        "EU Medicine Type",
    )

    eu_atmp = create_dashboard_column(
        models.BooleanField(
            db_column="eu_atmp",
            null=True,
        ),
        Category.General_Information,
        "bool",
        "EU ATMP",
    )

    ema_number_check = create_dashboard_column(
        models.BooleanField(
            db_column="ema_number_check",
            null=True,
        ),
        Category.General_Information,
        "bool",
        "EMA Number Check",
    )

    ingredients_substance = models.ForeignKey(
        IngredientsAndSubstances,
        models.CASCADE,
        db_column="ingredients_substance",
    )

    class Meta:
        db_table = "medicinal_product"
