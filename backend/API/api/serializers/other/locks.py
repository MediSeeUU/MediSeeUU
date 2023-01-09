# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

# This file contains the serializer for the locks model
# ------------------------------------------------------
from rest_framework import serializers
from api.models.other import (
    MedicineLocks,
    OrphanLocks,
)


class MedicineLocksSerializer(serializers.ModelSerializer):
    """
    Serializer for the :py:class:`.MedicineLocks` model
    """

    class Meta:
        """
        Meta class, return all fields by default
        """

        model = MedicineLocks
        fields = "__all__"


class OrphanLocksSerializer(serializers.ModelSerializer):
    """
    Serializer for the :py:class:`.OrphanLocks` model
    """

    class Meta:
        """
        Meta class, return all fields by default
        """

        model = OrphanLocks
        fields = "__all__"
