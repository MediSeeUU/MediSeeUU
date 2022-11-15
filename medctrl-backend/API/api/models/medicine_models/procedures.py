# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .medicinal_product import MedicinalProduct
from .common import create_dashboard_column, Category


class Procedures(models.Model):
    eu_pnumber = models.ForeignKey(
        MedicinalProduct,
        models.CASCADE,
        null=False,
    )

    eu_suspension = create_dashboard_column(
        models.BooleanField(
            null=False
        ),
        Category.General_Information,
        "bool",
        "EU suspension",
    )

    eu_referral = create_dashboard_column(
        models.BooleanField(
            null=False
        ),
        Category.General_Information,
        "bool",
        "EU referral",
    )

    class Meta:
        db_table = "procedures"
