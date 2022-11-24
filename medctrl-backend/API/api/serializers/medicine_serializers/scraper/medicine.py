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
    OrphanProduct,
    Procedures,
    LegalBases,
)


class MedicinalProductSerializer(serializers.ModelSerializer):
    """
    Medicine table serializer for the scraper endpoints
    """

    class Meta:
        """
        Meta information
        """

        model = MedicinalProduct
        fields = "__all__"


class IngredientsAndSubstancesSerializer(serializers.ModelSerializer):
    """
    IngredientsAndSubstances table serializer for the scraper endpoints
    """

    class Meta:
        """
        Meta information
        """

        model = IngredientsAndSubstances
        fields = "__all__"


class MarketingAuthorisationSerializer(serializers.ModelSerializer):
    """
    MarketingAuthorisation table serializer for the scraper endpoints
    """

    class Meta:
        """
        Meta information
        """

        model = MarketingAuthorisation
        fields = "__all__"


class AcceleratedAssessmentSerializer(serializers.ModelSerializer):
    """
    AcceleratedAssessment table serializer for the scraper endpoints
    """

    class Meta:
        """
        Meta information
        """

        model = AcceleratedAssessment
        exclude = ["id", ]


class DurationSerializer(serializers.ModelSerializer):
    """
    Duration table serializer for the scraper endpoints
    """

    class Meta:
        """
        Meta information
        """

        model = Duration
        exclude = ["id", ]


class OrphanProductSerializer(serializers.ModelSerializer):
    """
    OrphanProduct table serializer for the scraper endpoints
    """

    class Meta:
        """
        Meta information
        """

        model = OrphanProduct
        fields = "__all__"


class ProceduresSerializer(serializers.ModelSerializer):
    """
    Procedures table serializer for the scraper endpoints
    """

    class Meta:
        """
        Meta information
        """

        model = Procedures
        exclude = ["id", ]


class LegalBasesSerializer(serializers.ModelSerializer):
    """
    LegalBases table serializer for the scraper endpoints
    """

    class Meta:
        """
        Meta information
        """

        model = LegalBases
        exclude = ["id", ]

