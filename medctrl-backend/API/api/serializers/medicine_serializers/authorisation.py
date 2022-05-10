from rest_framework import serializers
from api.models.medicine_models import Authorisation

class AuthorisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authorisation
        fields = "__all__"