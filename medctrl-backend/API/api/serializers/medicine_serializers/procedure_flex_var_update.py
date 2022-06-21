# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from rest_framework import serializers
from api.models.medicine_models import Procedure

# serializer for the flexible variables of procedure
class ProcedureFlexVarUpdateSerializer(serializers.ModelSerializer):
    """Endpoint procedure serializer"""

    class Meta:
        """Metadata"""

        model = Procedure
        fields = ["decisionurl", "annexurl"]
