# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

# This file contains all serializers concerning
# the history of the medicine data of the database.
# ---------------------------------------------

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
        fields = "__all__"


class AuthorisationStatusSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = history_authorisation_status
        fields = "__all__"


class AuthorisationTypeSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = history_authorisation_type
        fields = "__all__"


class BrandNameSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = history_brand_name
        fields = "__all__"


class MAHSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = history_mah
        fields = "__all__"


class NumberCheckSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = history_number_check
        fields = "__all__"


class OrphanDesignationSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = history_od
        fields = "__all__"


class PrimeSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = history_prime
        fields = "__all__"
