# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from hashlib import md5
from django.db import models
from api.models.create_dashboard_columns import create_dashboard_column, Category, ExtraDashBoardColumn
from api.models.na_fields import BooleanWithNAField
from api.models.common import DataFormats


class IngredientsAndSubstances(models.Model):
    """
    This is the model class for the Ingredients and Substances table. New attributes can be added here.
    This model is derived from a base model from the Django library.

    Attributes:
        active_substance (models.TextField):
            TextField containing the active_substance. Shown on the dashboard.
        atc_code (models.CharField):
            CharField containing the atc_code. Shown on the dashboard.
        eu_nas (BooleanWithNAField):
            BooleanWithNAField containing eu_nas. Shown on the dashboard.
    """

    active_substance = create_dashboard_column(
        models.TextField(
            null=False,
            blank=False,
        ),
        Category.Ingredients_and_substances,
        DataFormats.String,
        "Active Substance",
    )

    atc_code = create_dashboard_column(
        models.CharField(
            max_length=45,
            null=False,
            blank=False,
        ),
        Category.Medicinal_product,
        DataFormats.String,
        "ATC Code",
        [
            ExtraDashBoardColumn(
                Category.Medicinal_product,
                "atc_name_l1",
                DataFormats.String,
                "ATC name (level 1)",
                lambda x: x[0],
            ),
            ExtraDashBoardColumn(
                Category.Medicinal_product,
                "atc_name_l2",
                DataFormats.String,
                "ATC name (level 2)",
                lambda x: x[0: 3],
            ),
            ExtraDashBoardColumn(
                Category.Medicinal_product,
                "atc_name_l3",
                DataFormats.String,
                "ATC name (level 3)",
                lambda x: x[0: 4],
            ),
            ExtraDashBoardColumn(
                Category.Medicinal_product,
                "atc_name_l4",
                DataFormats.String,
                "ATC name (level 4)",
                lambda x: x[0: 5],
            ),
        ]
    )

    eu_nas = create_dashboard_column(
        BooleanWithNAField(
            null=True,
            blank=True,
        ),
        Category.Ingredients_and_substances,
        DataFormats.Bool,
        "EU New Active Substance",
    )

    def __str__(self):
        return self.active_substance

    class Meta:
        db_table = "ingredients_and_substances"
        verbose_name = "Ingredients And Substances"
        verbose_name_plural = "Ingredients And Substances"
