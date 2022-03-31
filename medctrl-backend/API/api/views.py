from rest_framework import viewsets
from api.serializers import MedicineSerializer, LegalBasisSerializer, LegalScopeSerializer, AtcCodeSerializer
from api.models import Medicine, LegalBasis, LegalScope, AtcCode

class MedicineViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer

class LegalBasisViewSet(viewsets.ModelViewSet): #should be only accessible by admin to add/update/delete etc. ?
    queryset = LegalBasis.objects.all()
    serializer_class = LegalBasisSerializer

class LegalScopeViewSet(viewsets.ModelViewSet):
    queryset = LegalScope.objects.all()
    serializer_class = LegalScopeSerializer

class AtcCodeViewSet(viewsets.ModelViewSet):
    queryset = AtcCode.objects.all()
    serializer_class = AtcCodeSerializer