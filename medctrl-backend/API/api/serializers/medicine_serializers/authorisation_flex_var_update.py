# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from rest_framework import serializers

from api.models.medicine_models import Authorisation

# serializer for the flexible fields of authorisation
class AuthorisationFlexVarUpdateSerializer(serializers.ModelSerializer):
    """AuthorisationFlex serializer"""

    class Meta:
        """Metadata"""

        model = Authorisation
        fields = ["decisionurl", "annexurl", "eparurl"]
