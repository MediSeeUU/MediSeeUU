# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from hashlib import md5
from django.db import models
from api.models.create_dashboard_columns import create_dashboard_column, Category


class IngredientsAndSubstances(models.Model):
    """
    This is the model class for the Ingredients and Substances table. New attributes can be added here.
    This model is derived from a base model from the Django library.

    Attributes:
        active_substance_hash (models.CharField):
            The active_substance is the primary key. However, a models.TextField cannot be used as the primary key.
            That's why we create a hash from the active_substance and use that as the primary key.
            Not shown on the dashboard.
        active_substance (models.TextField):
            TextField containing the active_substance. Shown on the dashboard.
        atc_code (models.CharField):
            CharField containing the atc_code. Shown on the dashboard.
        eu_nas (models.BooleanField):
            BooleanField containing eu_nas. Shown on the dashboard.
    """
    active_substance_hash = models.CharField(
        max_length=32,
        primary_key=True,
        null=False,
        blank=False,
    )

    active_substance = create_dashboard_column(
        models.TextField(
            null=False,
            blank=False,
        ),
        Category.Ingredients_and_substances,
        "string",
        "Active Substance",
    )

    atc_code = create_dashboard_column(
        models.CharField(
            max_length=7,
            null=False,
            blank=False,
        ),
        Category.Medicinal_product,
        "string",
        "ATC Code",
    )

    eu_nas = create_dashboard_column(
        models.BooleanField(
            null=True,
            blank=False,
        ),
        Category.Ingredients_and_substances,
        "bool",
        "EU New Active Substance",
    )

    def save(self, *args, **kwargs):
        """
        Overrides the default save function to add the active_substance_hash field

        Args:
            *args: all function parameters
            **kwargs: all keyword arguments
        """
        self.active_substance_hash = md5(self.active_substance.encode()).hexdigest()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "ingredients_and_substances"
