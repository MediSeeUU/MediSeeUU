from rest_framework import viewsets
from api.serializers.access_level_serializers import MedicineSerializer
from api.models.medicine_models import Medicine

class PublicAccessViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions for atc code.
    """

    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
