from rest_framework import serializers
from django.contrib.auth.models import User

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    """User Serializer"""

    class Meta:
        """Metadata"""

        model = User
        fields = ("id", "username", "email")
