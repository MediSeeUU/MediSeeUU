from rest_framework import serializers
from api.models.medicine_models import Lookuplegalscope


class LegalScopeSerializer(serializers.ModelSerializer):
    """Legal scope serializer"""

    class Meta:
        """Metadata"""

        model = Lookuplegalscope
        fields = ["legalscope"]
