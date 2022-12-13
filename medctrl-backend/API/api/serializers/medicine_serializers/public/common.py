# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from collections import OrderedDict
from django.db.models import Model
from typing import Tuple
from api.models.get_dashboard_columns import get_data_key


def serialize_data(mixin: object, model: Model, attribute_name: str, many: bool = False) \
        -> list[Tuple[str, OrderedDict[str, str]]]:
    """

    Args:
        mixin:
        model:
        attribute_name:
        many:

    Returns:

    """

    result = []
    if hasattr(mixin.Meta, attribute_name):
        # Iterate the specified related objects with their serializer
        for field, serializer_class in getattr(mixin.Meta, attribute_name):
            # Check if the model has a relation to the field
            if hasattr(model, field):
                obj_field = getattr(model, field)
                # If relation is not null
                if obj_field:
                    # Serialize data
                    serializer = serializer_class(context=mixin.context, many=many)
                    obj_rep = serializer.to_representation(obj_field)
                    result.append((field, obj_rep))
    return result


class RelatedMixin:
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
    def to_representation(self, obj: Model) -> OrderedDict[str, str]:
        """
        Overrides the default `to_representation` method to add the related fields

        Args:
            obj (Model): An instance of the model being serialized

        Returns:
            OrderedDict[str, str]: The representation with the related fields added
        """
        # Get the current object representation
        representation = super().to_representation(obj)
        serialized_data = serialize_data(self, obj, "related")
        for field, obj_rep in serialized_data:
            if field in representation:
                representation.pop(field)
            for key in obj_rep:
                representation[key] = obj_rep[key]
        return representation


class ListMixin:
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
    def to_representation(self, obj: Model) -> OrderedDict[str, str]:
        """
        Overrides the default `to_representation` method to add the list fields

        Args:
            obj (Model): An instance of the model being serialized

        Returns:
            OrderedDict[str, str]: The representation with the list fields added
        """
        # Get the current object representation
        representation = super().to_representation(obj)
        serialized_data = serialize_data(self, obj, "list", True)
        for field, obj_rep in serialized_data:
            representation[field] = []
            for key in obj_rep:
                for value in key.values():
                    representation[field].append(value)
        return representation


class HistoryMixin:
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
    def to_representation(self, obj: Model) -> OrderedDict[str, str]:
        """
        Overrides the default `to_representation` method to add the history fields

        Args:
            obj (Model): An instance of the model being serialized

        Returns:
            OrderedDict[str, str]: The representation with the history fields added
        """
        # Get the current object representation
        representation = super().to_representation(obj)

        initial_serialized_data = serialize_data(self, obj, "initial_history")
        for field, obj_rep in initial_serialized_data:
            if field in representation:
                representation.pop(field)
            for key in obj_rep:
                representation[field] = obj_rep[key]

        if hasattr(self.Meta, "current_history"):
            # Iterate the specified history objects with their serializer
            for field, serializer_class in self.Meta.current_history:
                if hasattr(obj, field):
                    history = getattr(obj, field).all().order_by("change_date").last()
                    if history:
                        data = serializer_class(history).data
                        if data:
                            field_name = get_data_key(serializer_class.Meta.model, field)
                            representation[field_name] = data[field]
        return representation


class AnyBoolsList:
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

    def to_representation(self, obj: Model) -> OrderedDict[str, str]:
        """
        Overrides the default `to_representation` method to add the history fields

        Args:
            obj (Model): An instance of the model being serialized

        Returns:
            OrderedDict[str, str]: The representation with the history fields added
        """
        representation = super().to_representation(obj)
        return representation

        for related_name, serializer_class, fields in getattr(self.Meta, "any_bools_list"):
            if hasattr(obj, related_name):
                obj_field = getattr(obj, related_name)
                # If relation is not null
                if obj_field:
                    # Serialize data
                    serializer = serializer_class(context=self.context, many=True)
                    obj_rep = serializer.to_representation(obj_field)
                    for field in fields:
                        pass
