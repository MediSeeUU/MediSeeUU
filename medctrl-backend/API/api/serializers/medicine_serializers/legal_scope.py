from rest_framework import serializers
from api.models.medicine_models import LegalScope


class LegalScopeSerializer(serializers.ModelSerializer):
    """Legal scope serializer"""

    class Meta:
        """Metadata"""

        model = LegalScope
        fields = ["description"]
