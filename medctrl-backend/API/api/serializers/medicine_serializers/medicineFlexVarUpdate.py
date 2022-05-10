from rest_framework import serializers

from api.models.medicine_models import Medicine


class MedicineFlexVarUpdateSerializer(serializers.ModelSerializer):
    """Medicineflex serializer"""

    class Meta:
        """Metadata"""

        model = Medicine
        fields = ["atccode", "status", "referral", "suspension", "emaurl", "ecurl"]
