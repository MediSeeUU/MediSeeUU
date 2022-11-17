# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
import django.db.models
from rest_framework import serializers
from functools import partial
from api.models.medicine_models import (
    MedicinalProduct,
    LegalBases,
    IngredientsAndSubstances,
    HistoryAuthorisationStatus,
    HistoryAuthorisationType,
    HistoryBrandName,
    HistoryMAH,
    HistoryOD,
    HistoryPrime,
)
from api.serializers.medicine_serializers.public import (
    MarketingAuthorisationSerializer,
    AuthorisationStatusSerializer,
    AuthorisationTypeSerializer,
    BrandNameSerializer,
    MAHSerializer,
    OrphanDesignationSerializer,
    PrimeSerializer,
)


class FlattenMixin(object):
    """
    Flattens the specified related objects in this representation
    """

    def to_representation(self, obj):
        # Get the current object representation
        representation = super().to_representation(obj)
        if hasattr(self.Meta, "flatten"):
            # Iterate the specified related objects with their serializer
            for field, serializer_class in self.Meta.flatten:
                if hasattr(obj, field):
                    serializer = serializer_class(context=self.context)
                    obj_rep = serializer.to_representation(getattr(obj, field))
                    if field in representation:
                        representation.pop(field)
                    # Include their fields, prefixed, in the current representation
                    for key in obj_rep:
                        representation[key] = obj_rep[key]
        return representation


class HistoryMixin(object):
    def to_representation(self, obj):
        representation = super().to_representation(obj)
        if hasattr(self.Meta, "history"):
            # Iterate the specified history objects with their serializer
            for field, serializer, model in self.Meta.history:
                queryset = model.objects.filter(eu_pnumber=obj.eu_pnumber)
                if queryset:
                    if field.endswith("_initial"):
                        queryset = queryset[0]
                    else:
                        queryset = queryset[len(queryset) - 1]
                    data = serializer(instance=queryset, read_only=True).data
                    for key in data:
                        representation[field] = data[key]
        return representation
