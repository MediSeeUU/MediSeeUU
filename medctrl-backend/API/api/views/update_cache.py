# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

# For each user all data is fetched from the database when opening
# the dashboard and stored in memory cache.
# This improves the performance of the GET requests by several seconds.
# -------------------------------------------------------------------
from django.core.cache import cache
from rest_framework.settings import settings

from api.serializers.medicine_serializers.public import PublicMedicinalProductSerializer
from api.serializers.medicine_serializers.scraper import UrlsSerializer
from api.models.medicine_models import MedicinalProduct
import logging

logger = logging.getLogger(__name__)


def update_cache():
    """
    Adds all medicine and urls data to cache memory of the server
    """
    if not settings.MEDICINES_CACHING:
        logger.info("Caching turned off, skipping cache update")
    else:
        try:
            queryset = MedicinalProduct.objects.all()
            medicine_serializer = PublicMedicinalProductSerializer(queryset, many=True)
            cache.set(
                "medicine_cache", medicine_serializer.data, None
            )  # We set cache timeout to none so it never expires
            urls_serializer = UrlsSerializer(queryset, many=True)
            cache.set(
                "urls_cache", urls_serializer.data, None
            )  # We set cache timeout to none so it never expires
        except Exception as e:
            logger.warning(f"An error has occurred while updating cache: {str(e)}")
