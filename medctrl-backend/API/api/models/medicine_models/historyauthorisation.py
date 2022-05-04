from django.db import models


class Historyauthorisation(models.Model):
    
    eunumber = models.ForeignKey(
        "Medicine", models.CASCADE, db_column="EUNumber"
    )
    authorisationdate = models.DateField(db_column="AuthorisationDate")
    opiniondate = models.DateField(db_column="OpinionDate", blank=True, null=True)
    decisionauthorisationtype = models.CharField(
        db_column="DecisionAuthorisationType", max_length=45, blank=True, null=True
    )
    annexauthorisationtype = models.CharField(
        db_column="AnnexAuthorisationType", max_length=45, blank=True, null=True
    )
    registerauthorisationtype = models.CharField(
        db_column="RegisterAuthorisationType", max_length=45, blank=True, null=True
    )

    class Meta:
        db_table = "historyauthorisation"
