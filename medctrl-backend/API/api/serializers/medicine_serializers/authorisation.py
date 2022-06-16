# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from rest_framework import serializers
from api.models.medicine_models import Authorisation

# serializer for all the fields of authorisation
class AuthorisationSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the scraper endpoints
    """

    class Meta:
        model = Authorisation
        fields = "__all__"
