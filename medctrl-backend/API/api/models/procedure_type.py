from django.db import models


class ProcedureType(models.Model):
    procedure_type_id = models.UUIDField(primary_key=True)
    description = models.CharField(max_length=320)

    class Meta:
        db_table = "procedure_type"
