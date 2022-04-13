from django.db import models

class Lookupatccode(models.Model):
    atccode = models.CharField(db_column='ATCCode', primary_key=True, max_length=7)

    class Meta:
        db_table = 'lookupatccode'