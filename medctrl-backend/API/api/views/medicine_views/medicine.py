from rest_framework import viewsets
from api.serializers.medicine_serializers import PublicMedicineSerializer
from api.models.medicine_models import Medicine
from api.models.medicine_models import Procedure
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class MedicineViewSet(viewsets.ReadOnlyModelViewSet):
    # Here we should make the distinction in access level --> change serializer based on access level

    queryset = Medicine.objects.all()
    serializer_class = PublicMedicineSerializer
