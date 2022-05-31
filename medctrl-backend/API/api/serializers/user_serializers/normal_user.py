from rest_framework import serializers
from django.contrib.auth.models import User, Group

from api.models import SavedSelection
from api.serializers import SavedSelectionSerializer

#Serialises all groups provided by the Userserializer
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

#serializes all informations concerning a authenticated user
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class for the User model
    """

    groups = GroupSerializer(many=True) #adds all groups a user belongs to
    selections = serializers.SerializerMethodField()

    class Meta:
        """
        Meta class for the UserSerializer
        """

        model = User
        fields = ("id", "username", "groups", "selections") #all fields that will be serialized and returned

    #gets all data selections that a user has saved
    def get_selections(self, user):
        """
        Get all the selections that this user has created
        """
        selections = SavedSelection.objects.filter(created_by=user.id)
        return SavedSelectionSerializer(selections, many=True).data
