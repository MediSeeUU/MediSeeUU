# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models


class Medicine(models.Model):
    """
    Model class for the medicine table.
    """
    
    test = models.CharField(
        db_column="test",
        max_length=45,
        blank=True,
        null=True
    )
    eunumber = models.IntegerField(
        db_column="EUNumber",
        primary_key=True
    )
    emanumber = models.CharField(
        db_column="EMANumber",
        max_length=45,
        blank=True,
        null=True
    )
    atccode = models.CharField(
        db_column="ATCCode",
        max_length=7,
        null=True
    )
    activesubstance = models.CharField(
        db_column="ActiveSubstance",
        max_length=255,
        null=True
    )
    newactivesubstance = models.IntegerField(
        db_column="NewActiveSubstance",
        blank=True,
        null=True
    )
    legalbasis = models.CharField(
        db_column="LegalBasis",
        max_length=45,
        null=True
    )
    legalscope = models.CharField(
        db_column="LegalScope",
        max_length=45,
        null=True
    )
    atmp = models.IntegerField(
        db_column="ATMP",
        blank=True,
        null=True
    )
    medicinetype = models.CharField(
        db_column="MedicineType",
        max_length=45,
        null=True
    )
    status = models.CharField(
        db_column="Status",
        max_length=45,
        null=True
    )
    referral = models.IntegerField(
        db_column="Referral",
        blank=True,
        null=True
    )
    suspension = models.IntegerField(
        db_column="Suspension",
        blank=True,
        null=True
    )
    emaurl = models.CharField(
        db_column="EMAURL",
        max_length=320,
        blank=True,
        null=True
    )
    ecurl = models.CharField(
        db_column="ECURL",
        max_length=320,
        blank=True,
        null=True
    )

    manually_updated = models.BooleanField(default=False)

    class Meta:
        db_table = "medicine"
