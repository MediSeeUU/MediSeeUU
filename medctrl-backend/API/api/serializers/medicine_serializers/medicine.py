from rest_framework import serializers
from api.models.medicine_models import Medicine

# serializer for all the fields of medicine
class MedicineSerializer(serializers.ModelSerializer):
    """
    Medicine table serializer for the scraper endpoints
    """
    class Meta:
        """
        Meta information
        """
        model = Medicine
        fields = "__all__"
