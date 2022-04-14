from rest_framework import serializers
from api.models.medicine_models import AtcCode


class AtcCodeSerializer(serializers.ModelSerializer):
    """Atc code serializer"""

    class Meta:
        """Metadata"""

        model = AtcCode
        fields = ["atc_code", "description"]
