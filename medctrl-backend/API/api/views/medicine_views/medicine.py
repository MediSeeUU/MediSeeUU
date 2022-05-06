from rest_framework import viewsets
from api.serializers.medicine_serializers import PublicMedicineSerializer
from api.models.medicine_models import Medicine
from api.models.medicine_models import Procedure

class MedicineViewSet(viewsets.ModelViewSet):
    # Here we should make the distinction in access level --> change serializer based on access level
    
    queryset = Medicine.objects.all()
    serializer_class = PublicMedicineSerializer
