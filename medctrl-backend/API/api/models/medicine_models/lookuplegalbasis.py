# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models


class Lookuplegalbasis(models.Model):
    """
    Model class for the legal basis lookup table. As the abstract functionality for all model classes is nearly identical, information about them has been moved to an external readme.
    """

    legalbasis = models.CharField(
        db_column="LegalBasis", primary_key=True, max_length=45
    )

    class Meta:
        db_table = "lookuplegalbasis"
