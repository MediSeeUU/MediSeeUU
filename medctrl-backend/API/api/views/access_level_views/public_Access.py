
# from api.models.medicine_models.medicine import Medicine
# from rest_framework.response import Response

# def publicAccess(request):
#     columns = Medicine.objects.all()
#     print("OUTPUT...........................................................................................", columns)
#     print(columns[0].eunumber)
#     return Response() 

from rest_framework import viewsets
from api.serializers.access_level_serializers import MedicineSerializer
from api.models.medicine_models import Medicine

class PublicAccessViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions for atc code.
    """

    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer