# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

# This file contains the serializer for the locks model
# ------------------------------------------------------
from rest_framework import serializers
from api.models.other import Locks


class LocksSerializer(serializers.ModelSerializer):
    """
    Serializer for the Locks model
    """

    class Meta:
        """
        Meta class, return all fields by default
        """

        model = Locks
        fields = "__all__"
