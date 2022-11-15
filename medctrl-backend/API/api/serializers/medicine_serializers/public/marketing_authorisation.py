# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

from rest_framework import serializers
from api.models.medicine_models import AcceleratedAssessment, Duration, MarketingAuthorisation


class AcceleratedAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Meta information
        """
        model = AcceleratedAssessment
        exclude = ["id", ]


class DurationSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Meta information
        """
        model = Duration
        exclude = ["id", ]


class MarketingAuthorisationSerializer(serializers.ModelSerializer):
    ema_accelerated_assessment = AcceleratedAssessmentSerializer(read_only=True)
    duration = DurationSerializer(read_only=True)

    class Meta:
        """
        Meta information
        """
        model = MarketingAuthorisation
        fields = "__all__"

    def to_representation(self, obj) -> dict:
        """
        This function creates a one-dimensional object from multiple fields.

        Args:
            obj (Any): Takes an object to be transformed.

        Returns:
            dict: Returns a single dict representation of the object.
        """
        representation = super().to_representation(obj)

        # Change the representation for all foreign key fields
        for field in [
            "ema_accelerated_assessment",
            "duration",
        ]:
            field_representation = representation.pop(field)
            if field_representation:
                for key in field_representation:
                    representation[key] = field_representation[key]

        return representation
