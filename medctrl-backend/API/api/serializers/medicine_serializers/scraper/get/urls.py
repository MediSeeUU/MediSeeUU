from rest_framework import serializers
from api.models.human_models import (
    MedicinalProduct,
)


class UrlsSerializer(serializers.ModelSerializer):
    """
    Endpoint for the scraper to view all urls already scraped.
    """
    class Meta:
        """
        Meta information
        """
        model = MedicinalProduct
        fields = ("eu_pnumber", "ema_url", "ec_url")
