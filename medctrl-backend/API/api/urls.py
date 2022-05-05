from django.urls import path, include
from rest_framework.routers import DefaultRouter
from knox import views as knox_views

from api.views.medicine_views import ProcedureViewSet
from api.views.account_views import RegisterAPI, LoginAPI
from api.views.access_level_views import PublicAccessViewSet


router = DefaultRouter()
router.register(r"procedures", ProcedureViewSet, basename="procedures")
router.register(r"public", PublicAccessViewSet , basename="public")

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
