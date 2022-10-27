# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

# This serializer file is responsible for serializing all
# data concerning an user. Because the permissions we use
# are partly determined by the group(s) an user belongs to,
# the group serializer is included in this file.
# --------------------------------------------------------

from rest_framework import serializers
from django.contrib.auth.models import User, Group
from api.models.other import SavedSelection
from api.serializers import SavedSelectionSerializer


# Serializes all groups provided by the Userserializer
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


# serializes all information concerning a authenticated user
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class for the User model
    """
    groups = GroupSerializer(many=True)  # adds all groups a user belongs to
    selections = serializers.SerializerMethodField()

    class Meta:
        """
        Meta class for the UserSerializer
        """
        model = User
        fields = (
            "id",
            "username",
            "groups",
            "selections",
        )  # all fields that will be serialized and returned

    # gets all data selections that a user has saved
    def get_selections(self, user):
        """
        Get all the selections that this user has created
        """
        selections = SavedSelection.objects.filter(created_by=user.id)
        return SavedSelectionSerializer(selections, many=True).data
