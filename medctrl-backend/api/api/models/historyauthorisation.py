from django.db import models

class Historyauthorisation(models.Model):
    eunumber = models.OneToOneField('Medicine', models.DO_NOTHING, db_column='EUNumber', primary_key=True)
    authorisationdate = models.DateField(db_column='AuthorisationDate')
    opiniondate = models.DateField(db_column='OpinionDate', blank=True, null=True)
    decisionauthorisationtype = models.CharField(db_column='DecisionAuthorisationType', max_length=45, blank=True, null=True)
    annexauthorisationtype = models.CharField(db_column='AnnexAuthorisationType', max_length=45, blank=True, null=True)
    registerauthorisationtype = models.CharField(db_column='RegisterAuthorisationType', max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'historyauthorisation'
        unique_together = (('eunumber', 'authorisationdate'),)