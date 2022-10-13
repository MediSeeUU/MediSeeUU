# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
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
