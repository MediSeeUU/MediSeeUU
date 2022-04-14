from django.urls import path, include
from rest_framework.routers import DefaultRouter
from knox import views as knox_views

from api.views.medicine_views import (
    MedicineViewSet,
    ProcedureViewSet,
    LegalBasisViewSet,
    LegalScopeViewSet,
    AtcCodeViewSet,
)
from api.views.account_views import RegisterAPI, LoginAPI


router = DefaultRouter()
router.register(r"medicine", MedicineViewSet, basename="medicine")
router.register(r"legalbasis", LegalBasisViewSet, basename="legalbasis")
router.register(r"legalscope", LegalScopeViewSet, basename="legalscope")
router.register(r"atccode", AtcCodeViewSet, basename="atccode")
router.register(r"procedures", ProcedureViewSet, basename="procedures")

urlpatterns = [
    path("", include(router.urls)),
    # Account routes
    path(
        "account/",
        include(
            [
                path("register/", RegisterAPI.as_view(), name="register"),
                path("login/", LoginAPI.as_view(), name="login"),
                path("logout/", knox_views.LogoutView.as_view(), name="logout"),
                path(
                    "logoutall/", knox_views.LogoutAllView.as_view(), name="logoutall"
                ),
            ]
        ),
    ),
]
