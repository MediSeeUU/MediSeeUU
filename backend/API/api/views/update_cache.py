# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

# For each user all data is fetched from the database when opening
# the dashboard and stored in memory cache.
# This improves the performance of the GET requests by several seconds.
# -------------------------------------------------------------------
from django.core.cache import cache
from rest_framework.settings import settings

from api.models.human_models import MedicinalProduct, models as human_models
from api.models.orphan_models import OrphanProduct, models as orphan_models
from api.models.get_dashboard_columns import insert_extra_dashboard_columns
from api.serializers.medicine_serializers.public.human import PublicMedicinalProductSerializer
from api.serializers.medicine_serializers.public.orphan import OrphanProductSerializer
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
            # Insert extra dashboard columns defined in the models
            human_cache = insert_extra_dashboard_columns(human_serializer.data, human_models)
            cache.set(
                "human_cache", human_cache, None
            )  # We set cache timeout to none so it never expires

            orphan_queryset = OrphanProduct.objects.all()
            orphan_serializer = OrphanProductSerializer(orphan_queryset, many=True)
            # Insert extra dashboard columns defined in the models
            orphan_cache = insert_extra_dashboard_columns(orphan_serializer.data, orphan_models)
            cache.set(
                "orphan_cache", orphan_cache, None
            )  # We set cache timeout to none so it never expires

            logging.info("Updated cache")
        except Exception as e:
            logger.warning(f"An error has occurred while updating cache: {str(e)}")


update_cache()
