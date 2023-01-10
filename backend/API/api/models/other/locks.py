# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

from django.db import models


class Locks(models.Model):
    """
    This is the model class for the Medicine Locks table.
    It is used to store locked attributes for a :py:class:`.MedicinalProduct` object.
    This model is derived from a base model from the Django library.

    Attributes:
        eu_pnumber (models.ForeignKey):
            Foreign Key to the :py:class:`.MedicinalProduct` object the lock is for.
        column_name (models.CharField):
            CharField containing the name of the column that needs to be locked.
    """
    model_name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
    )

    model_pk = models.CharField(
        max_length=255,
        null=False,
        blank=False,
    )

    column_name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
    )

    class Meta:
        db_table = "locks"
        constraints = [
            models.UniqueConstraint(
                fields=["model_name", "model_pk", "column_name"],
                name="locks composite key"
            )
        ]
        verbose_name = "Lock"
        verbose_name_plural = "Locks"



class LockModel(models.Model):
    def save(self, *args, **kwargs):
        if self.pk:
            locks = Locks.objects.filter(model_name=type(self).__name__, model_pk=self.pk).all()
            for lock in locks:
                if hasattr(self, lock.column_name):
                    setattr(self, lock.column_name, None)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
