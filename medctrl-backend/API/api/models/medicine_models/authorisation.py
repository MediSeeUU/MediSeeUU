from django.db import models


class Authorisation(models.Model):
    eunumber = models.OneToOneField(
        "Medicine", models.CASCADE, db_column="EUNumber", primary_key=True
    )
    rapporteur = models.ForeignKey(
        "Lookuprapporteur",
        models.CASCADE,
        db_column="Rapporteur",
        blank=True,
        null=True,
        related_name="rapporteur_related",
    )
    corapporteur = models.ForeignKey(
        "Lookuprapporteur",
        models.CASCADE,
        db_column="CoRapporteur",
        blank=True,
        null=True,
        related_name="corapporteur_related",
    )
    acceleratedgranted = models.IntegerField(
        db_column="AcceleratedGranted", blank=True, null=True
    )
    acceleratedmaintained = models.IntegerField(
        db_column="AcceleratedMaintained", blank=True, null=True
    )
    authorisationtotaltime = models.IntegerField(
        db_column="AuthorisationTotalTime", blank=True, null=True
    )
    authorisationactivetime = models.IntegerField(
        db_column="AuthorisationActiveTime", blank=True, null=True
    )
    authorisationstoppedtime = models.IntegerField(
        db_column="AuthorisationStoppedTime", blank=True, null=True
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
