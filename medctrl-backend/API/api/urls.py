from django.urls import path, include
from rest_framework.routers import DefaultRouter
from knox import views as knox_views

from api.views.medicine_views import ProcedureViewSet, MedicineViewSet
from api.views.account_views import RegisterAPI, LoginAPI

router = DefaultRouter()
router.register(r"procedure", ProcedureViewSet, basename="procedure")
router.register(r"medicine", MedicineViewSet , basename="medicine")

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
