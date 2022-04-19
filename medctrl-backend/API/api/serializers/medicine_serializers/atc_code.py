from rest_framework import serializers
from api.models.medicine_models import Lookupatccode


class AtcCodeSerializer(serializers.ModelSerializer):
    """Atc code serializer"""

    class Meta:
        """Metadata"""

        model = Lookupatccode
        fields = ["atccode"]
