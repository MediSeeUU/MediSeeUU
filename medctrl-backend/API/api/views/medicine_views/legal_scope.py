from rest_framework import viewsets
from api.serializers.medicine_serializers import LegalScopeSerializer
from api.models.medicine_models import LegalScope


class LegalScopeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions for Legal scope.
    """

    queryset = LegalScope.objects.all()
    serializer_class = LegalScopeSerializer
