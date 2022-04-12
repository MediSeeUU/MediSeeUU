from rest_framework import viewsets
from api.serializers import (
    ProcedureSerializer,
    MedicineSerializer,
    LegalBasisSerializer,
    LegalScopeSerializer,
    AtcCodeSerializer,
)
from api.models import Medicine, LegalBasis, LegalScope, AtcCode, Procedure


class MedicineViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions for medicine.
    """

    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer


class LegalBasisViewSet(
    viewsets.ModelViewSet
):  # should be only accessible by admin to add/update/delete etc. ?
    """
    This viewset automatically provides `list` and `retrieve` actions for Legal basis.
    """

    queryset = LegalBasis.objects.all()
    serializer_class = LegalBasisSerializer


class LegalScopeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions for Legal scope.
    """

    queryset = LegalScope.objects.all()
    serializer_class = LegalScopeSerializer


class AtcCodeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions for atc code.
    """

    queryset = AtcCode.objects.all()
    serializer_class = AtcCodeSerializer


class ProceduresViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions for atc code.
    """

    queryset = Procedure.objects.all()
    serializer_class = ProcedureSerializer
