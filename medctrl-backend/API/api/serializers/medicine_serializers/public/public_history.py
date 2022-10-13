from rest_framework import serializers
from api.models.medicine_models import (
    HistoryATCCode,
    HistoryAuthorisationStatus,
    HistoryAuthorisationType,
    HistoryBrandName,
    HistoryMAH,
    HistoryEMANumberCheck,
    HistoryOD,
    HistoryPrime,
)


class ATCCodeSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = HistoryATCCode
        fields = ("atc_code",)
        ordering = ("change_date",)


class AuthorisationStatusSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
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
    Authorisation table serializer for the view endpoint medicine
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
    Authorisation table serializer for the view endpoint medicine
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
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = HistoryMAH
        fields = ("eu_mah",)
        ordering = ("change_date",)


class NumberCheckSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = HistoryEMANumberCheck
        fields = ("ema_number_check",)
        ordering = ("change_date",)


class OrphanDesignationSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
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
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = HistoryPrime
        fields = ("eu_prime",)
        ordering = ("change_date",)
