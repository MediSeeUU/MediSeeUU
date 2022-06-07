# For each user all data is fetched from the database when opening 
# the dashboard and strored in memory cache.
# This improves the peformance of the 'Get' requests by serval seconds.
#-------------------------------------------------------------------

from django.core.cache import cache
from rest_framework.settings import settings

from api.serializers.medicine_serializers import PublicMedicineSerializer
from api.models.medicine_models import Medicine

# Adds all medicine data to cache memeory of the server
def update_cache():
    if settings.MEDICINES_CACHING:
        queryset = Medicine.objects.all()
        serializer = PublicMedicineSerializer(queryset, many=True)
        cache.set(
            "medicine_cache", serializer.data, None
        )  # We set cache timeout to none so it never expires
