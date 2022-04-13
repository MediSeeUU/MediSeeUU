from django.db import models

class Lookuplegalbasis(models.Model):
    legalbasis = models.CharField(db_column='LegalBasis', primary_key=True, max_length=45)

    class Meta:
        db_table = 'lookuplegalbasis'