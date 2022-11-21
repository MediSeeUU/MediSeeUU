# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from hashlib import md5
from django.db import models
from .common import create_dashboard_column, Category


class IngredientsAndSubstances(models.Model):
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
        Category.General_Information,
        "string",
        "Active Substance",
    )

    atc_code = create_dashboard_column(
        models.CharField(
            max_length=7,
            null=False,
            blank=False,
        ),
        Category.General_Information,
        "string",
        "ATC Code",
    )

    eu_nas = create_dashboard_column(
        models.BooleanField(
            null=True,
            blank=False,
        ),
        Category.General_Information,
        "bool",
        "EU New Active Substance",
    )

    def save(self, *args, **kwargs):
        self.active_substance_hash = md5(self.active_substance.encode()).hexdigest()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "ingredients_and_substances"
