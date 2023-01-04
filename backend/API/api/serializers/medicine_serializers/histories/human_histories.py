# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

from rest_framework import serializers
from api.models.human_models import (
    HistoryAuthorisationStatus,
    HistoryAuthorisationType,
    HistoryBrandName,
    HistoryMAH,
    HistoryOD,
    HistoryPrime,
)


class AuthorisationStatusSerializer(serializers.ModelSerializer):
    """
    This serializer serializes the :py:class:`.HistoryAuthorisationStatus` model.
    """
    class Meta:
        """
        Meta information
        """
        model = HistoryAuthorisationStatus
        exclude = ("id", )


class AuthorisationTypeSerializer(serializers.ModelSerializer):
    """
    This serializer serializes the :py:class:`.HistoryAuthorisationType` model.
    """
    class Meta:
        """
        Meta information
        """
        model = HistoryAuthorisationType
        exclude = ("id", )


class BrandNameSerializer(serializers.ModelSerializer):
    """
    This serializer serializes the :py:class:`.HistoryBrandName` model.
    """
    class Meta:
        """
        Meta information
        """
        model = HistoryBrandName
        exclude = ("id", )


class MAHSerializer(serializers.ModelSerializer):
    """
    This serializer serializes the :py:class:`.HistoryMAH` model.
    """
    class Meta:
        """
        Meta information
        """
        model = HistoryMAH
        exclude = ("id", )


class OrphanDesignationSerializer(serializers.ModelSerializer):
    """
    This serializer serializes the :py:class:`.HistoryOD` model.
    """
    class Meta:
        """
        Meta information
        """
        model = HistoryOD
        exclude = ("id", )


class PrimeSerializer(serializers.ModelSerializer):
    """
    This serializer serializes the :py:class:`.HistoryPrime` model.
    """
    class Meta:
        """
        Meta information
        """
        model = HistoryPrime
        exclude = ("id", )
