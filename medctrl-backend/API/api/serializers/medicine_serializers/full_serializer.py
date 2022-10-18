# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from rest_framework import serializers
from api.models.medicine_models import Medicine
from api.models.medicine_models import (
    HistoryATCCode,
    HistoryAuthorisationStatus,
    HistoryAuthorisationType,
    HistoryBrandName,
    HistoryMAH,
    HistoryEMANumberCheck,
    HistoryOD,
    HistoryPrime,
    HistoryEUOrphanCon
)

# serializer for all the fields of medicine


class MedicineSerializer(serializers.ModelSerializer):
    """
    Medicine table serializer for the scraper endpoints
    """

    class Meta:
        """
        Meta information
        """

        model = Medicine
        fields = "__all__"

# serializers for all the history tables


class ATCCodeSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = HistoryATCCode
        fields = "__all__"


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


class NumberCheckSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = HistoryEMANumberCheck
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


class EUOrphanConSerializer (serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = HistoryEUOrphanCon
        fields = ("eu_orphan_con",)
        ordering = ("change_date",)
