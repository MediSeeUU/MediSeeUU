# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from rest_framework import serializers
from api.models.orphan_models import (
    OrphanProduct,
)


class OrphanProductSerializer(serializers.ModelSerializer):
    """
    OrphanProduct table serializer for the scraper endpoints
    """

    class Meta:
        """
        Meta information
        """

        model = OrphanProduct
        fields = "__all__"
