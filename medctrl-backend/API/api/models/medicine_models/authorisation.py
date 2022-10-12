# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.db import models
from .common import create_dashboard_column, Category


class Authorisation(models.Model):
    """
    Model class for the authorisation table.
    """

    eunumber = models.OneToOneField(
        "Medicine", models.CASCADE, db_column="EUNumber", primary_key=True
    )

    rapporteur = create_dashboard_column(
         models.CharField(db_column="Rapporteur", max_length=45, blank=True, null=True),
        Category.Co_Rapporteur,
        "string",
        "Rapporteur"
    )

    corapporteur = create_dashboard_column(
        models.CharField(db_column="CoRapporteur", max_length=45, blank=True, null=True),
        Category.Co_Rapporteur,
        "string",
        "Co-Rapporteur"
    )

    acceleratedgranted = models.IntegerField(
        db_column="AcceleratedGranted", blank=True, null=True
    )
    acceleratedmaintained = models.IntegerField(
        db_column="AcceleratedMaintained", blank=True, null=True
    )
    authorisationactivetime = models.IntegerField(
        db_column="AuthorisationActiveTime", blank=True, null=True
    )
    authorisationstoppedtime = models.IntegerField(
        db_column="AuthorisationStoppedTime", blank=True, null=True
    )
    authorisationtotaltime = models.IntegerField(
        db_column="AuthorisationTotalTime", blank=True, null=True
    )
    decisiontime = models.IntegerField(db_column="DecisionTime", blank=True, null=True)
    decisionurl = models.CharField(
        db_column="DecisionURL", max_length=255, blank=True, null=True
    )
    annexurl = models.CharField(
        db_column="AnnexURL", max_length=255, blank=True, null=True
    )
    eparurl = models.CharField(
        db_column="EPARURL", max_length=255, blank=True, null=True
    )

    class Meta:
        db_table = "authorisation"