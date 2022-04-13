from django.db import models

class Lookupactivesubstance(models.Model):
    activesubstance = models.CharField(db_column='ActiveSubstance', primary_key=True, max_length=255)

    class Meta:
        db_table = 'lookupactivesubstance'