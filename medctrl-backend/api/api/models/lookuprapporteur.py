from django.db import models

class Lookuprapporteur(models.Model):
    rapporteur = models.CharField(db_column='Rapporteur', primary_key=True, max_length=45)

    class Meta:
        db_table = 'lookuprapporteur'