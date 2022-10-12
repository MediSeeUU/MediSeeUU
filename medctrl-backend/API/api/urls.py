# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

# This file contains all routes (endpoints) that are accessible
# by a user. Each route connects to a 'view', which can be found
# in the 'views' folder. We distinguish between APIView's and ViewSets.
# In 'urlpatterns' paths are specified. APIView's use '.as_view()' as
# an additional argument where ViewSets use 'as_viewViewSet' as an additional
# argument. ViewSets can also be used in a router, APIView's can not.
# -----------------------------------------------------------------------

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from knox import views as knox_views

from api.views.medicine_views import (
    #ProcedureViewSet,
    MedicineViewSet,
)
from api.views.account_views import LoginAPI
from api.views.other import SavedSelectionViewSet
from api.views.other import Medicine_info
from api.scraper.router import url_patterns as scraper_routes


# Only viewSets can be registered at a router.
# The router is used for better organization of the code.
router = DefaultRouter()
router.register(r"medicine", MedicineViewSet, basename="medicine")
#router.register(r"procedure/(?P<eunumber>\d+)", ProcedureViewSet, basename="procedure")
router.register(r"saveselection", SavedSelectionViewSet, basename="saveselection")

# urlpatterns is the default way of adding routes (endpoints).
urlpatterns = [
    path("", include(router.urls)),  # Includes all router paths as patterns
    # Account routes (../account/#PATH)
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
    # Other routes
    path("scraper/", include(scraper_routes)),
    path("structureData/", Medicine_info.as_view()),
]
