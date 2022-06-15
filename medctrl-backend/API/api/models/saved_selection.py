# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
import uuid
from django.db import models
from django.contrib.auth.models import User
from api.models.medicine_models import Medicine


class SavedSelection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    eunumbers = models.ManyToManyField(Medicine)
    name = models.CharField(max_length=256, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "saved_selection"
