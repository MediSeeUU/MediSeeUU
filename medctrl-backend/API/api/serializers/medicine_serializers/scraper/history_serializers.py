# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

# This file contains all serializers concerning
# the history of the medicine data of the database.
# ---------------------------------------------

from rest_framework import serializers
from api.models.medicine_models import (
    HistoryAuthorisationStatus,
    HistoryAuthorisationType,
    HistoryBrandName,
    HistoryMAH,
    HistoryOD,
    HistoryPrime,
    HistoryEUOrphanCon
)


class AuthorisationStatusSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = HistoryAuthorisationStatus
        fields = "__all__"


class AuthorisationTypeSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = HistoryAuthorisationType
        fields = "__all__"


class BrandNameSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = HistoryBrandName
        fields = "__all__"


class MAHSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = HistoryMAH
        fields = "__all__"


class OrphanDesignationSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = HistoryOD
        fields = "__all__"


class PrimeSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = HistoryPrime
        fields = "__all__"

class EUOrphanConSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = HistoryEUOrphanCon
        fields = "__all__"