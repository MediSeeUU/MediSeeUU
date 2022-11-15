# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

from rest_framework import serializers
from api.models.medicine_models import AcceleratedAssessment, MarketingAuthorisation


class AcceleratedAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Meta information
        """
        model = AcceleratedAssessment
        exclude = ["id", ]


class MarketingAuthorisationSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Meta information
        """
        model = MarketingAuthorisation
        fields = "__all__"

