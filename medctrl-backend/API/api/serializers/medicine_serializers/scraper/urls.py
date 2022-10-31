from rest_framework import serializers
from api.models.medicine_models import (
    Medicine,
)


class UrlsSerializer(serializers.ModelSerializer):
    """
    Endpoint for the scraper to view all urls already scraped.
    """
    class Meta:
        """
        Meta information
        """
        model = Medicine
        fields = ("eu_pnumber", "ema_url", "ec_url", "aut_url", "smpc_url", "epar_url", "omar_url", "odwar_url")