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
    HistoryEUOrphanCon,
)


class AuthorisationStatusSerializer(serializers.ModelSerializer):
    """
    Authorisation Status serializer for the post endpoint.
    """

    class Meta:
        """
        Meta information
        """

        model = HistoryAuthorisationStatus
        exclude = ["id", ]


class AuthorisationTypeSerializer(serializers.ModelSerializer):
    """
    Authorisation type serializer for the post endpoint.
    """

    class Meta:
        """
        Meta information
        """

        model = HistoryAuthorisationType
        exclude = ["id", ]


class BrandNameSerializer(serializers.ModelSerializer):
    """
    Brand name serializer for the post endpoint
    """

    class Meta:
        """
        Meta information
        """

        model = HistoryBrandName
        exclude = ["id", ]


class MAHSerializer(serializers.ModelSerializer):
    """
    Marketing Authorisation Holder serializer for the post endpoint
    """

    class Meta:
        """
        Meta information
        """

        model = HistoryMAH
        exclude = ["id", ]


class OrphanDesignationSerializer(serializers.ModelSerializer):
    """
    Orphan Designation table serializer for the post endpoint
    """
    class Meta:
        """
        Meta information
        """
        model = HistoryOD
        exclude = ["id", ]


class PrimeSerializer(serializers.ModelSerializer):
    """
    Priority Medicine Designation table serializer for the post endpoint
    """
    
    class Meta:
        """
        Meta information
        """

        model = HistoryPrime
        exclude = ["id", ]


class EUOrphanConSerializer(serializers.ModelSerializer):
    """
    Orphan Condition table serializer for the post endpoint
    """

    class Meta:
        """
        Meta information
        """

        model = HistoryEUOrphanCon
        exclude = ["id", ]
