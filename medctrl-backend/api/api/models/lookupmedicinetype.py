from django.db import models

class Lookupmedicinetype(models.Model):
    medicinetype = models.CharField(db_column='MedicineType', primary_key=True, max_length=45)

    class Meta:
        db_table = 'lookupmedicinetype'