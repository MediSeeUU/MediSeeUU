# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .medicinal_product import MedicinalProduct
from api.models.create_dashboard_columns import create_dashboard_column, Category
from api.models.common import LegalBasesTypes
from api.models.common import DataFormats


class LegalBases(models.Model):
    """
    This is the model class for the Legal Base table. New attributes can be added here.
    This model is derived from a base model from the Django library.

    Attributes:
        eu_pnumber (models.ForeignKey):
            Foreign Key to the :py:class:`.MedicinalProduct` model
        eu_legal_basis (models.CharField):
            CharField containing one of the EU legal bases for a medicine.
            Restricted by the options from :py:class:`.LegalBasesTypes`. Shown on the dashboard.
    """
    eu_pnumber = models.ForeignKey(
        MedicinalProduct,
        models.CASCADE,
        null=False,
        blank=False,
        related_name="eu_legal_basis",
    )

    eu_legal_basis = create_dashboard_column(
        models.CharField(
            max_length=45,
            choices=LegalBasesTypes.choices,
            null=False,
            blank=False,
        ),
        Category.Marketing_authorisation,
        DataFormats.String_List,
        "EU Legal Basis",
    )

    class Meta:
        db_table = "legal_bases"
        constraints = [
            models.UniqueConstraint(fields=['eu_pnumber', 'eu_legal_basis'],
                                    name="eu_pnumber eu_legal_basis composite key")
        ]
