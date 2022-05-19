from rest_framework import serializers

from api.models.medicine_models import Authorisation

# serializer for the flexible fields of authorisation
class AuthorisationFlexVarUpdateSerializer(serializers.ModelSerializer):
    """AuthorisationFlex serializer"""

    class Meta:
        """Metadata"""

        model = Authorisation
        fields = ["decisionurl", "annexurl", "eparurl"]
