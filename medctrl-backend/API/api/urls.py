from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (
    ProceduresViewSet,
    MedicineViewSet,
    LegalBasisViewSet,
    LegalScopeViewSet,
    AtcCodeViewSet,
)

router = DefaultRouter()
router.register(r"medicine", MedicineViewSet, basename="medicine")
router.register(r"legalbasis", LegalBasisViewSet, basename="legalbasis")
router.register(r"legalscope", LegalScopeViewSet, basename="legalscope")
router.register(r"atccode", AtcCodeViewSet, basename="atccode")
router.register(r"procedures", ProceduresViewSet, basename="procedures")

urlpatterns = [
    path("", include(router.urls)),
]
