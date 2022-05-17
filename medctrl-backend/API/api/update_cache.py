from django.core.cache import cache

from api.serializers.medicine_serializers import PublicMedicineSerializer
from api.models.medicine_models import Medicine

def update_cache():
    queryset = Medicine.objects.all()
    serializer = PublicMedicineSerializer(queryset, many=True)
    cache.set("medicine_cache", serializer.data, None)
