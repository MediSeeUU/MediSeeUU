# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .medicinal_product import MedicinalProduct
from api.models.dashboard_columns import create_dashboard_column, Category


class Procedures(models.Model):
    """
    This is the model class for the Procedures table. New attributes can be added here.
    This model is derived from a base model from the Django library.

     Attributes:
        eu_pnumber (models.ForeignKey):
            Foreign Key to the :py:class:`.MedicinalProduct` model
        eu_suspension (models.BooleanField):
            BooleanField indicating if this procedure is a suspension procedure.
            On the dashboard, it is shown as True if there is any suspension procedure.
        eu_referral (models.BooleanField):
            BooleanField indicating if this procedure is a referral procedure.
            On the dashboard, it is shown as True if there is any referral procedure.
    """
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
