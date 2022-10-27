# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from rest_framework import serializers
from api.models.medicine_models import Medicine


# serializer for the flexible fields of medicine
class MedicineFlexVarUpdateSerializer(serializers.ModelSerializer):
    """
    Medicineflex serializer for the post endpoint
    """
    class Meta:
        """
        Metadata
        """
        model = Medicine
        fields = [
            "atc_code",
            "ema_number_check",
            "ema_url",
            "ec_url",
            "aut_url",
            "smpc_url",
            "epar_url",
            "eu_referral",
            "eu_suspension",
            "omar_url",
            "odwar_url"
        ]
