# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

class FlattenMixin(object):
    """
    Flattens the specified related objects in this representation
    """
    def to_representation(self, obj):
        # Get the current object representation
        representation = super().to_representation(obj)
        if hasattr(self.Meta, 'flatten'):
            # Iterate the specified related objects with their serializer
            for field, serializer_class in self.Meta.flatten:
                serializer = serializer_class(context=self.context)
                obj_rep = serializer.to_representation(getattr(obj, field))
                if field in representation:
                    representation.pop(field)
                # Include their fields, prefixed, in the current representation
                for key in obj_rep:
                    representation[key] = obj_rep[key]
        return representation
