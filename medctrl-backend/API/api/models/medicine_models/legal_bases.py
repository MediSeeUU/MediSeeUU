# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .common import create_dashboard_column, Category, LegalBasesTypes


class LegalBases(models.Model):
    """
    This is the model class for the Legal Base table. New attributes can be added here.
    This model is derived from a base model from the Django library.
    """
    eu_pnumber = models.ForeignKey(
        "Medicine",
        models.CASCADE,
        db_column="eu_pnumber",
        null=False
    )

    eu_legal_basis = create_dashboard_column(
        models.CharField(db_column="eu_legal_basis", max_length=14, choices=LegalBasesTypes.choices),
        Category.Marketing_Authorisation,
        "[string]",
        "EU Legal Basis"
    )

    class Meta:
        db_table = "legal_bases"
        constraints = [
            models.UniqueConstraint(fields=['eu_pnumber', 'eu_legal_basis'],
                                    name="eu_pnumber eu_legal_basis composite key")
        ]
