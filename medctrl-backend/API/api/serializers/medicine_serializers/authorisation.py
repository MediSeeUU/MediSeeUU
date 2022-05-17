from rest_framework import serializers
from api.models.medicine_models import Authorisation

# serializer for all the fields of authorisation
class AuthorisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authorisation
        fields = "__all__"
