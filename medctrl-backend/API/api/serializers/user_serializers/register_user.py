from rest_framework import serializers
from django.contrib.auth.models import User

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    """Register user Serializer"""

    class Meta:
        """Metadata"""

        model = User
        fields = (
            "id",
            "username",
            "password",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"],
            validated_data["password"],
        )

        return user
