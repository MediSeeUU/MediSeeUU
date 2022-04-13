from django.db import models

class Medicine(models.Model):
    eunumber = models.IntegerField(db_column='EUNumber', primary_key=True)
    emanumber = models.CharField(db_column='EMANumber', max_length=45, blank=True, null=True)
    atccode = models.ForeignKey(Lookupatccode, models.DO_NOTHING, db_column='ATCCode', blank=True, null=True)
    activesubstance = models.ForeignKey(Lookupactivesubstance, models.DO_NOTHING, db_column='ActiveSubstance', blank=True, null=True)
    newactivesubstance = models.IntegerField(db_column='NewActiveSubstance', blank=True, null=True)
    legalbasis = models.ForeignKey(Lookuplegalbasis, models.DO_NOTHING, db_column='LegalBasis', blank=True, null=True)
    legalscope = models.ForeignKey(Lookuplegalscope, models.DO_NOTHING, db_column='LegalScope', blank=True, null=True)
    atmp = models.IntegerField(db_column='ATMP', blank=True, null=True)
    medicinetype = models.ForeignKey(Lookupmedicinetype, models.DO_NOTHING, db_column='MedicineType', blank=True, null=True)
    status = models.ForeignKey(Lookupstatus, models.DO_NOTHING, db_column='Status', blank=True, null=True)
    referral = models.IntegerField(db_column='Referral', blank=True, null=True)
    suspension = models.IntegerField(db_column='Suspension', blank=True, null=True)
    emaurl = models.CharField(db_column='EMAURL', max_length=320, blank=True, null=True)
    ecurl = models.CharField(db_column='ECURL', max_length=320, blank=True, null=True)

    class Meta:
        db_table = 'medicine'