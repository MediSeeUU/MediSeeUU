# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

# For each user all data is fetched from the database when opening
# the dashboard and stored in memory cache.
# This improves the performance of the GET requests by several seconds.
# -------------------------------------------------------------------
from typing import Any
from collections import OrderedDict
from django.core.cache import cache
from rest_framework.settings import settings
from api.models.human_models import MedicinalProduct, models as human_models
from api.models.orphan_models import OrphanProduct, models as orphan_models
from api.models.get_dashboard_columns import insert_extra_dashboard_columns
from api.serializers.medicine_serializers.public.human import PublicMedicinalProductSerializer
from api.serializers.medicine_serializers.public.orphan import OrphanProductSerializer
import logging

logger = logging.getLogger(__name__)


def get_human_cache() -> OrderedDict[str, Any]:
    """
    Tries to get human data from cache if caching is on, otherwise get data from database

    Returns:
        All medicinal product data
    """
    if settings.MEDICINES_CACHING:
        human_cache = cache.get("human_cache")
        if human_cache:
            return human_cache
    return update_human_cache()


def get_orphan_cache() -> OrderedDict[str, Any]:
    """
    Tries to get orphan data from cache if caching is on, otherwise get data from database

    Returns:
        All orphan product data
    """
    if settings.MEDICINES_CACHING:
        orphan_cache = cache.get("orphan_cache")
        if orphan_cache:
            return orphan_cache
    return update_orphan_cache()


def update_human_cache() -> OrderedDict[str, Any]:
    """
    Gets all human data from database and updates cache if cache is on

    Returns:
        All medicinal product data
    """
    human_queryset = MedicinalProduct.objects.all()
    human_serializer = PublicMedicinalProductSerializer(human_queryset, many=True)
    # Insert extra dashboard columns defined in the models
    human_cache = insert_extra_dashboard_columns(human_serializer.data, human_models)
    if settings.MEDICINES_CACHING:
        cache.set(
            "human_cache", human_cache, None
        )  # We set cache timeout to none so it never expires
    return human_cache


def update_orphan_cache() -> OrderedDict[str, Any]:
    """
    Gets all orphan data from database and updates cache if cache is on

    Returns:
        All orphan product data
    """
    orphan_queryset = OrphanProduct.objects.all()
    orphan_serializer = OrphanProductSerializer(orphan_queryset, many=True)
    # Insert extra dashboard columns defined in the models
    orphan_cache = insert_extra_dashboard_columns(orphan_serializer.data, orphan_models)
    if settings.MEDICINES_CACHING:
        cache.set(
            "orphan_cache", orphan_cache, None
        )  # We set cache timeout to none so it never expires
    return orphan_cache


def update_cache():
    """
    Adds all medicinal and orphan data to cache memory of the server
    """
    if not settings.MEDICINES_CACHING:
        logger.info("Caching turned off, skipping cache update")
    else:
        try:
            update_human_cache()
            update_orphan_cache()
            logger.info("Updated cache")
        except Exception as e:
            logger.warning(f"An error has occurred while updating cache: {str(e)}")


update_cache()
