# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from collections import OrderedDict


class RelatedMixin(object):
    """
    Selects the fields of the specified related object and inserts it in a flat representation.

    Use it in a serializer by inheriting from this class and specifying a related attribute in the Meta class.
    Specify a field name and a serializer.

    Example:
        .. code-block:: python

            class yourSerializer(RelatedMixin, serializers.ModelSerializer)
                class Meta:
                    related = [
                        ("ingredients_and_substances", IngredientsAndSubstancesSerializer),
                        ("marketing_authorisation", MarketingAuthorisationSerializer),
                    ]
    """
    def to_representation(self, obj) -> OrderedDict:
        # Get the current object representation
        representation = super().to_representation(obj)
        if hasattr(self.Meta, "related"):
            # Iterate the specified related objects with their serializer
            for field, serializer_class in self.Meta.related:
                if hasattr(obj, field):
                    serializer = serializer_class(context=self.context)
                    obj_rep = serializer.to_representation(getattr(obj, field))
                    if field in representation:
                        representation.pop(field)
                    # Include their fields, prefixed, in the current representation
                    for key in obj_rep:
                        representation[key] = obj_rep[key]
        return representation


class ListMixin(object):
    """
    Selects the items of the specified related list object and inserts it in a flat representation.

    Use it in a serializer by inheriting from this class and specifying a list attribute in the Meta class.
    Specify a field name and a serializer.

    Example:
        .. code-block:: python

            class yourSerializer(ListMixin, serializers.ModelSerializer)
                class Meta:
                    list = [
                        ("eu_legal_basis", LegalBasesSerializer),
                    ]
    """
    def to_representation(self, obj) -> OrderedDict:
        # Get the current object representation
        representation = super().to_representation(obj)
        if hasattr(self.Meta, "list"):
            # Iterate the specified related objects with their serializer
            for field, serializer_class in self.Meta.list:
                if hasattr(obj, field):
                    serializer = serializer_class(context=self.context, many=True)
                    obj_rep = serializer.to_representation(getattr(obj, field))
                    representation[field] = []
                    for key in obj_rep:
                        for value in key.values():
                            representation[field].append(value)
        return representation


class HistoryMixin(object):
    """
    Selects the items of the specified related history object and inserts it in a flat representation.

    Use it in a serializer by inheriting from this class and specifying a history attribute in the Meta class.
    Specify a field name and a serializer. The serializer must be sorted by date.

    An entry in the history list must be a tuple with four items:
        - The field name, this must be same as the `related_name` attribute of the foreign key.
        - The serializer of the history model.
        - A boolean which indicates if the initial entry in the history should be displayed.
        - A boolean which indicates if the current entry in the history should be displayed.

    Example:
        .. code-block:: python

            class yourSerializer(HistoryMixin, serializers.ModelSerializer)
                class Meta:
                    history = [
                        ("eu_aut_status", AuthorisationStatusSerializer, False, True),
                        ("eu_aut_type", AuthorisationTypeSerializer, True, True),
                    ]
    """
    def to_representation(self, obj) -> OrderedDict:
        # Get the current object representation
        representation = super().to_representation(obj)
        if hasattr(self.Meta, "history"):
            # Iterate the specified history objects with their serializer
            for field, serializer_class, initial, current in self.Meta.history:
                if hasattr(obj, field):
                    history = getattr(obj, field).all().order_by("change_date")
                    data = serializer_class(history, many=True).data
                    if data:
                        if initial:
                            representation[f"{field}_initial"] = next(iter(data))[field]
                        if current:
                            representation[f"{field}_current"] = next(reversed(data))[field]
        return representation
