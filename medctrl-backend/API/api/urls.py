from django.urls import path, include
from rest_framework.routers import DefaultRouter
from knox import views as knox_views

from api.views.medicine_views import (
    ProcedureViewSet,
    MedicineViewSet,
)
from api.views.account_views import LoginAPI
from api.views.other import SavedSelectionViewSet
from api.views.other import Medicine_info
from api.scraper.router import url_patterns as scraper_routes


#Direct routes (viewSets)
router = DefaultRouter()
router.register(r"medicine", MedicineViewSet, basename="medicine")
router.register(r"procedure/(?P<eunumber>\d+)", ProcedureViewSet, basename="procedure")
router.register(r"saveselection", SavedSelectionViewSet, basename="saveselection")

#indirect routes (../name.as_vieuw)
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
    path("scraper/", include(scraper_routes)),
    path("detailedData/", Medicine_info.as_view()),
]
