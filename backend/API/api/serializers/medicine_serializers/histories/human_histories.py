# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

from rest_framework import serializers
from api.models.human_models import (
    HistoryAuthorisationStatus,
    HistoryAuthorisationType,
    HistoryBrandName,
    HistoryEUOrphanCon,
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
        fields = ("eu_aut_status", "change_date", )


class AuthorisationTypeSerializer(serializers.ModelSerializer):
    """
    This serializer serializes the :py:class:`.HistoryAuthorisationType` model.
    """
    class Meta:
        """
        Meta information
        """
        model = HistoryAuthorisationType
        fields = ("eu_aut_type", "change_date", )


class BrandNameSerializer(serializers.ModelSerializer):
    """
    This serializer serializes the :py:class:`.HistoryBrandName` model.
    """
    class Meta:
        """
        Meta information
        """
        model = HistoryBrandName
        fields = ("eu_brand_name", "change_date", )


class MAHSerializer(serializers.ModelSerializer):
    """
    This serializer serializes the :py:class:`.HistoryMAH` model.
    """
    class Meta:
        """
        Meta information
        """
        model = HistoryMAH
        fields = ("eu_mah", "change_date", )


class OrphanDesignationSerializer(serializers.ModelSerializer):
    """
    This serializer serializes the :py:class:`.HistoryOD` model.
    """
    class Meta:
        """
        Meta information
        """
        model = HistoryOD
        fields = ("eu_od", "change_date", )


class PrimeSerializer(serializers.ModelSerializer):
    """
    This serializer serializes the :py:class:`.HistoryPrime` model.
    """
    class Meta:
        """
        Meta information
        """
        model = HistoryPrime
        fields = ("eu_prime", "change_date", )


class EUOrphanConSerializer (serializers.ModelSerializer):
    """
    This serializer serializes the :py:class:`.HistoryEUOrphanCon` model.
    """
    class Meta:
        """
        Meta information
        """
        model = HistoryEUOrphanCon
        fields = ("eu_orphan_con", "change_date", )
