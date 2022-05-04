from rest_framework import serializers
from api.models.medicine_models import Medicine
from api.models.medicine_models import Authorisation
from api.models.medicine_models import Procedure

class AuthorisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authorisation
        exclude = ('eunumber', )

class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = ('decisiondate', )

class MedicineSerializer(serializers.ModelSerializer):
    authorisation = AuthorisationSerializer(read_only=True)
    #procedure = ProcedureSerializer(read_only=True)

    class Meta:
        model = Medicine
        fields = "__all__"
    
    def to_representation(self, obj):
        """Move fields from authorisation to user representation."""
        representation = super().to_representation(obj)

        authorisation_representation = representation.pop('authorisation')
        for key in authorisation_representation:
            representation[key] = authorisation_representation[key]

        return representation

    def to_internal_value(self, data):
        """Move fields related to authorisation to their own authorisation dictionary."""
        authorisation_internal = {}
        for key in AuthorisationSerializer.Meta.fields:
            if key in data:
                authorisation_internal[key] = data.pop(key)

        internal = super().to_internal_value(data)
        internal['authorisation'] = authorisation_internal
        internal['procedure'] = procedure_internal
        return internal

    def update(self, instance, validated_data):
        """Update user and authorisation. Assumes there is a authorisation for every user."""
        authorisation_data = validated_data.pop('authorisation')
        procedure_data = validated_data.pop('procedure')
        super().update(instance, validated_data)

        authorisation = instance.authorisation
        for attr, value in authorisation_data.items():
            setattr(authorisation, attr, value)
        authorisation.save()

        return instance
