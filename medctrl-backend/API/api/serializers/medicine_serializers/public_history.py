from rest_framework import serializers
from api.models.medicine_models import (
    history_atc_code,
    history_authorisation_status,
    history_authorisation_type,
    history_brand_name,
    history_mah,
    history_number_check,
    history_od,
    history_prime,
)


class ATCCodeSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = history_atc_code
        fields = "atc_code"


class AuthorisationStatusSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = history_authorisation_status
        fields = "eu_aut_type"


class AuthorisationTypeSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = history_authorisation_type
        fields = "eu_aut_status"


class BrandNameSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = history_brand_name
        fields = "eu_brand_name"


class MAHSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = history_mah
        fields = "eu_mah"


class NumberCheckSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = history_number_check
        fields = "ema_number_check"


class OrphanDesignationSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = history_od
        fields = "eu_od"


class PrimeSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = history_prime
        fields = "eu_prime"
