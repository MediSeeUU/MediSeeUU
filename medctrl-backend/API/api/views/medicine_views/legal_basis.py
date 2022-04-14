from rest_framework import viewsets
from api.serializers.medicine_serializers import LegalBasisSerializer
from api.models.medicine_models import LegalBasis


class LegalBasisViewSet(
    viewsets.ModelViewSet
):  # should be only accessible by admin to add/update/delete etc. ?
    """
    This viewset automatically provides `list` and `retrieve` actions for Legal basis.
    """

    queryset = LegalBasis.objects.all()
    serializer_class = LegalBasisSerializer
