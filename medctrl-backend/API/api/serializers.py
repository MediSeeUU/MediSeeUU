from rest_framework import serializers

from api.models import Dummy


class DummySerializer(serializers.ModelSerializer):
    """
    Serializer that can serialize a Dummy object from given data
    """

    text = serializers.CharField(max_length=1000, required=True)

    def create(self, validated_data):
        # Once the request data has been validated
        # we can create a todo item instance in the database
        return Dummy.objects.create(text=validated_data.get("text"))

    def update(self, instance, validated_data):
        # Once the request data has been validated
        # we can update the todo item instance in the database
        instance.text = validated_data.get("text", instance.text)
        instance.save()
        return instance

    class Meta:
        """
        Metadata for serializer
        """

        model = Dummy
        fields = ("id", "text")
