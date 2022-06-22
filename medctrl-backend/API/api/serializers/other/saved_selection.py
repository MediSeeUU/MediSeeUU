# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

# This file contains the serializer for the 'saved data'
# of an user.
# ------------------------------------------------------
from rest_framework import serializers
from api.models.other import SavedSelection

# Gets all data selections that a user saved
class SavedSelectionSerializer(serializers.ModelSerializer):
    """
    Serializer for the SavedSelection model
    """

    class Meta:
        """
        Meta class, return all fields by default
        """

        model = SavedSelection
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Instead of returning the user_id, return the username
        data["created_by"] = instance.created_by.username

        return data
