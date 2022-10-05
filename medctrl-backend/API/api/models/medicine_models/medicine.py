# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .common import create_dashboard_column, Category

class Medicine(models.Model):
    """
    Model class for the medicine table.
    """
    
    test = create_dashboard_column(
        models.CharField(db_column="test", max_length=45, blank=True, null=True), 
        Category.General_Information,
        "string",
        "test"
    )

    activesubstance = create_dashboard_column(
        models.CharField(db_column="ActiveSubstance", max_length=255, null=True),
        Category.General_Information,
        "string",
        "Active Substance"
    )

    atccode = create_dashboard_column(
        models.CharField(db_column="ATCCode", max_length=7, null=True),
        Category.General_Information,
        "string",
        "ATC Code"
    )

    status = create_dashboard_column(
        models.CharField(db_column="Status", max_length=45, null=True),
        Category.General_Information,
        "string",
        "Status"
    )


    eunumber = create_dashboard_column(
        models.IntegerField(db_column="EUNumber", primary_key=True),
        Category.Identifying_Information,
        "number",
        "Short EU Number"
    )

    emanumber = create_dashboard_column(
        models.CharField(db_column="EMANumber", max_length=45, blank=True, null=True),
        Category.Identifying_Information,
        "number",
        "Application Number"
    )

    atmp = create_dashboard_column(
        models.IntegerField(db_column="ATMP", blank=True, null=True),
        Category.Medicine_Designations,
        "bool",
        "ATMP"
    )

    newactivesubstance = create_dashboard_column(
        models.IntegerField(db_column="NewActiveSubstance", blank=True, null=True),
        Category.Medicine_Designations,
        "bool",
        "NAS Qualified"
    )

    legalscope = create_dashboard_column(
        models.CharField(db_column="LegalScope", max_length=45, null=True),
        Category.Legal_Information,
        "string",
        "Legal Scope"
    )

    legalbasis = create_dashboard_column(
        models.CharField(db_column="LegalBasis", max_length=45, null=True),
        Category.Legal_Information,
        "string",
        "Legal Type"
    )

    emaurl = create_dashboard_column(
        models.CharField(db_column="EMAURL", max_length=320, blank=True, null=True),
        Category.Additional_Resources,
        "link",
        "EMA url"
    )

    ecurl = create_dashboard_column(
        models.CharField(db_column="ECURL", max_length=320, blank=True, null=True),
        Category.Additional_Resources,
        "link",
        "EC url"
    )

    medicinetype = models.CharField(
        db_column="MedicineType", max_length=45, null=True
    )

    referral = models.IntegerField(db_column="Referral", blank=True, null=True)
    suspension = models.IntegerField(db_column="Suspension", blank=True, null=True)

    manually_updated = models.BooleanField(default=False)

    class Meta:
        db_table = "medicine"
