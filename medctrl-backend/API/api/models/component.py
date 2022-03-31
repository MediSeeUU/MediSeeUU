from django.db import models


class Component(models.Model):
    eu_nr = models.OneToOneField(
        "Medicine", models.DO_NOTHING, db_column="eu_nr", primary_key=True
    )
    substance = models.ForeignKey("Substance", models.DO_NOTHING)
    substance_new = models.TextField(
        blank=True, null=True
    ) 

    class Meta:
        db_table = "component"
        unique_together = (("eu_nr", "substance"),)
