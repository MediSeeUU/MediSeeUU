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
    Authorisation Status table serializer for the view endpoint medicine
    """
    class Meta:
        """
        Meta information
        """
        model = HistoryAuthorisationStatus
        fields = ("eu_aut_status",)
        ordering = ("change_date",)


class AuthorisationTypeSerializer(serializers.ModelSerializer):
    """
    Authorisation Type table serializer for the view endpoint medicine
    """
    class Meta:
        """
        Meta information
        """
        model = HistoryAuthorisationType
        fields = ("eu_aut_type",)
        ordering = ("change_date",)


class BrandNameSerializer(serializers.ModelSerializer):
    """
    Brand Name table serializer for the view endpoint medicine
    """
    class Meta:
        """
        Meta information
        """
        model = HistoryBrandName
        fields = ("eu_brand_name",)
        ordering = ("change_date",)


class MAHSerializer(serializers.ModelSerializer):
    """
    Marketing Authorisation Holder table serializer for the view endpoint medicine
    """
    class Meta:
        """
        Meta information
        """
        model = HistoryMAH
        fields = ("eu_mah",)
        ordering = ("change_date",)


class OrphanDesignationSerializer(serializers.ModelSerializer):
    """
    Orphan Designation table serializer for the view endpoint medicine
    """
    class Meta:
        """
        Meta information
        """
        model = HistoryOD
        fields = ("eu_od",)
        ordering = ("change_date",)


class PrimeSerializer(serializers.ModelSerializer):
    """
    Priority Medicine Designation table serializer for the view endpoint medicine
    """
    class Meta:
        """
        Meta information
        """
        model = HistoryPrime
        fields = ("eu_prime",)
        ordering = ("change_date",)


class EUOrphanConSerializer (serializers.ModelSerializer):
    """
    Orphan Condition table serializer for the view endpoint medicine
    """
    class Meta:
        """
        Meta information
        """
        model = HistoryEUOrphanCon
        fields = ("eu_orphan_con",)
        ordering = ("change_date",)
