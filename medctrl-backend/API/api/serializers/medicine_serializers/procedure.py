from rest_framework import serializers
from api.models.medicine_models import Procedure


class ProcedureSerializer(serializers.ModelSerializer):
    """Endpoint procedure serializer"""

    class Meta:
        """Metadata"""

        model = Procedure
        fields = "__all__"
