from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import MedicineViewSet

router = DefaultRouter()
router.register(r'medicine', MedicineViewSet,basename="medicine")

urlpatterns = [
    path("", include(router.urls)),
]