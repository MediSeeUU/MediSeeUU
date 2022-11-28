# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

from rest_framework import serializers
from api.serializers.medicine_serializers.public.common import RelatedMixin
from api.models.medicine_models import AcceleratedAssessment, Duration, MarketingAuthorisation


class AcceleratedAssessmentSerializer(serializers.ModelSerializer):
    """
    This serializer serializes the :py:class:`.AcceleratedAssessment` model.
    """
    class Meta:
        """
        Meta information
        """
        model = AcceleratedAssessment
        exclude = ["id", ]


class DurationSerializer(serializers.ModelSerializer):
    """
    This serializer serializes the :py:class:`.Duration` model.
    """
    class Meta:
        """
        Meta information
        """
        model = Duration
        exclude = ["id", ]


class MarketingAuthorisationSerializer(RelatedMixin, serializers.ModelSerializer):
    """
    This serializer serializes the :py:class:`.MarketingAuthorisation` model.
    """
    class Meta:
        """
        Meta information
        """
        model = MarketingAuthorisation
        related = [
            ("ema_accelerated_assessment", AcceleratedAssessmentSerializer),
            ("duration", DurationSerializer),
        ]
        fields = "__all__"
