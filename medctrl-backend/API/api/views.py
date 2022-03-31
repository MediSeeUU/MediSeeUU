from rest_framework import viewsets
from api.serializers import MedicineSerializer
from api.models import Medicine

class MedicineViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer