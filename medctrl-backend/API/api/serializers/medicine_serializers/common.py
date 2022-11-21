# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)


class RelatedMixin(object):
    """
    Selects the fields of the specified related object and inserts it in a flat representation.

    Use it in a serializer by inheriting from this class and specifying a related attribute in the Meta class.
    Specify a field name and a serializer.

    Example:
        class yourSerializer(RelatedMixin, serializers.ModelSerializer)
            class Meta:
                related = [
                    ("ingredients_and_substances", IngredientsAndSubstancesSerializer),
                    ("marketing_authorisation", MarketingAuthorisationSerializer),
                ]
    """

    def to_representation(self, obj):
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
        class yourSerializer(ListMixin, serializers.ModelSerializer)
            class Meta:
                list = [
                    ("eu_legal_basis", LegalBasesSerializer),
                ]
    """
    def to_representation(self, obj):
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
    Specify a field name and a serializer.

    If the field name ends with initial, the HistoryMixin will select the first item in the history object.
    Otherwise, it will select the current one.

    Example:
        class yourSerializer(HistoryMixin, serializers.ModelSerializer)
            class Meta:
                history = [
                    ("eu_aut_type_initial", AuthorisationTypeSerializer, HistoryAuthorisationType),
                    ("eu_aut_type_current", AuthorisationTypeSerializer, HistoryAuthorisationType),
                ]
    """
    def to_representation(self, obj):
        representation = super().to_representation(obj)
        if hasattr(self.Meta, "history"):
            # Iterate the specified history objects with their serializer
            for field, serializer, model in self.Meta.history:
                queryset = model.objects.filter(eu_pnumber=obj.eu_pnumber)
                if queryset:
                    if field.endswith("initial"):
                        queryset = queryset[0]
                    else:
                        queryset = queryset[len(queryset) - 1]
                    data = serializer(instance=queryset, read_only=True).data
                    for key in data:
                        representation[field] = data[key]
        return representation
