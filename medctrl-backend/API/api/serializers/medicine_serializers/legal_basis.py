from rest_framework import serializers
from api.models.medicine_models import Lookuplegalbasis


class LegalBasisSerializer(serializers.ModelSerializer):
    """Legal basis serializer"""

    class Meta:
        """Metadata"""

        model = Lookuplegalbasis
        fields = ["legalbasis"]
