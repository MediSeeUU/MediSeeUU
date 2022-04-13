from rest_framework import viewsets
from api.serializers.medicine_serializers import MedicineSerializer
from api.models.medicine_models import Medicine


class MedicineViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions for medicine.
    """

    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
