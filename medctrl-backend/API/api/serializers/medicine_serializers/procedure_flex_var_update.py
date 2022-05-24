from rest_framework import serializers
from api.models.medicine_models import Procedure

# serializer for the flexible variables of procedure
class ProcedureFlexVarUpdateSerializer(serializers.ModelSerializer):
    """Endpoint procedure serializer"""

    class Meta:
        """Metadata"""

        model = Procedure
        fields = ["decisionurl", "annexurl"]
