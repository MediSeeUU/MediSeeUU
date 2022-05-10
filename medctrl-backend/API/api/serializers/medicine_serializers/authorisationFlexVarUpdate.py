from rest_framework import serializers

from api.models.medicine_models import Authorisation


class AuthorisationFlexVarUpdateSerializer(serializers.ModelSerializer):
    """AuthorisationFlex serializer"""

    class Meta:
        """Metadata"""

        model = Authorisation
        fields = ["decisionurl", "annexurl", "eparurl"]
