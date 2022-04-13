from rest_framework import serializers
from api.models.medicine_models import LegalBasis


class LegalBasisSerializer(serializers.ModelSerializer):
    """Legal basis serializer"""

    class Meta:
        """Metadata"""

        model = LegalBasis
        fields = ["description"]
