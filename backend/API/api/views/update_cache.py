# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

# For each user all data is fetched from the database when opening
# the dashboard and stored in memory cache.
# This improves the performance of the GET requests by several seconds.
# -------------------------------------------------------------------
from django.core.cache import cache
from rest_framework.settings import settings

from api.models.human_models import MedicinalProduct
from api.models.orphan_models import OrphanProduct
from api.serializers.medicine_serializers.public import PublicMedicinalProductSerializer, OrphanProductSerializer
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
            human_queryset = MedicinalProduct.objects.all()
            human_serializer = PublicMedicinalProductSerializer(human_queryset, many=True)
            cache.set(
                "human_cache", human_serializer.data, None
            )  # We set cache timeout to none so it never expires

            orphan_queryset = OrphanProduct.objects.all()
            orphan_serializer = OrphanProductSerializer(orphan_queryset, many=True)
            cache.set(
                "orphan_cache", orphan_serializer.data, None
            )  # We set cache timeout to none so it never expires

            logging.info("Updated cache")
        except Exception as e:
            logger.warning(f"An error has occurred while updating cache: {str(e)}")


update_cache()
