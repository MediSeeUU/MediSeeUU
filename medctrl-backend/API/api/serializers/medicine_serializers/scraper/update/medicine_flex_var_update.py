# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from rest_framework import serializers
from api.models.medicine_models import (
    MedicinalProduct,
    IngredientsAndSubstances,
    MarketingAuthorisation,
    AcceleratedAssessment,
    Duration,
)
from api.models.orphan_models import (
    OrphanProduct,
)


# serializer for the flexible fields of medicine
class MedicinalProductFlexVarUpdateSerializer(serializers.ModelSerializer):
    """
    Medicinal Product serializer for the flexible variables for the post endpoint
    """
    class Meta:
        """
        Metadata
        """
        model = MedicinalProduct
        fields = [
            "ema_number_check",
            "ema_url",
            "ec_url",
        ]


class IngredientsAndSubstancesFlexVarUpdateSerializer(serializers.ModelSerializer):
    """
    IngredientsAndSubstances table serializer for the flexible variables for the scraper endpoints
    """

    class Meta:
        """
        Meta information
        """

        model = IngredientsAndSubstances
        fields = [
            "atc_code",
        ]


class MarketingAuthorisationFlexVarUpdateSerializer(serializers.ModelSerializer):
    """
    MarketingAuthorisation table serializer for the flexible variables for the scraper endpoints
    """

    class Meta:
        """
        Meta information
        """

        model = MarketingAuthorisation
        fields = [
            "aut_url",
            "smpc_url",
            "epar_url",
        ]


class AcceleratedAssessmentFlexVarUpdateSerializer(serializers.ModelSerializer):
    """
    AcceleratedAssessment table serializer for the flexible variables for the scraper endpoints
    """

    class Meta:
        """
        Meta information
        """

        model = AcceleratedAssessment
        fields = []


class DurationFlexVarUpdateSerializer(serializers.ModelSerializer):
    """
    Duration table serializer for the flexible variables for the scraper endpoints
    """

    class Meta:
        """
        Meta information
        """

        model = Duration
        fields = []


class OrphanProductFlexVarUpdateSerializer(serializers.ModelSerializer):
    """
    OrphanProduct table serializer for the flexible variables for the scraper endpoints
    """

    class Meta:
        """
        Meta information
        """

        model = OrphanProduct
        fields = [
            "omar_url",
            "odwar_url",
        ]
