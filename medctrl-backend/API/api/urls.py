from django.urls import path, include
from rest_framework.routers import DefaultRouter
from knox import views as knox_views

from api.views.medicine_views import (
    ProcedureViewSet,
    MedicineViewSet,
)
from api.views.account_views import LoginAPI
from api.views import SavedSelectionViewSet

router = DefaultRouter()
router.register(r"medicine", MedicineViewSet, basename="medicine")
router.register(r"procedure/(?P<eunumber>\d+)", ProcedureViewSet, basename="procedure")
router.register(r"saveselection", SavedSelectionViewSet, basename="saveselection")

urlpatterns = [
    path("", include(router.urls)),
    # Account routes
    path(
        "account/",
        include(
            [
                path("login/", LoginAPI.as_view(), name="login"),
                path("logout/", knox_views.LogoutView.as_view(), name="logout"),
                path(
                    "logoutall/", knox_views.LogoutAllView.as_view(), name="logoutall"
                ),
            ]
        ),
    ),
]
