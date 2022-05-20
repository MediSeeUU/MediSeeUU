from rest_framework import serializers
from django.contrib.auth.models import User, Group

from api.models import SavedSelection
from api.serializers import SavedSelectionSerializer


class GroupSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Group model
    """

    class Meta:
        """
        Meta class for the GroupSerializer
        """

        model = Group
        fields = ("name", "id")


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class for the User model
    """

    groups = GroupSerializer(many=True)
    selections = serializers.SerializerMethodField()

    class Meta:
        """
        Meta class for the UserSerializer
        """

        model = User
        fields = ("id", "username", "groups", "selections")

    def get_selections(self, user):
        """
        Get all the selections that this user has created
        """
        selections = SavedSelection.objects.filter(created_by=user.id)
        return SavedSelectionSerializer(selections, many=True).data
