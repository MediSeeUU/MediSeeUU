from rest_framework import serializers

from api.models.medicine_models import Medicine

# serializer for the flexible fields of medicine
class MedicineFlexVarUpdateSerializer(serializers.ModelSerializer):
    """Medicineflex serializer"""

    class Meta:
        """Metadata"""

        model = Medicine
        fields = ["atccode", "status", "referral", "suspension", "emaurl", "ecurl"]
