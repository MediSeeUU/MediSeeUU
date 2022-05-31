from rest_framework import serializers
from api.models.other import SavedSelection

#Gets all data slections that a user saved
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
