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

from api.views.medicine_views import HumanMedicineViewSet, OrphanMedicineViewSet
from api.views.histories_views import HumanHistoriesViewSet, OrphanHistoriesViewSet
from api.views.account_views import LoginAPI
from api.views.other import SavedSelectionViewSet, HumanOrphanViewSet
from api.views.structure_data.medicine import HumanMedicineInfo, OrphanMedicineInfo
from api.views.structure_data.history import HumanHistoryInfo, OrphanHistoryInfo
from api.views.scraper.router import url_patterns as scraper_routes

# Only viewSets can be registered at a router.
# The router is used for better organization of the code.
router = DefaultRouter()

router.register(r"saveSelection", SavedSelectionViewSet, basename="saveSelection")
router.register(r"medicine/human", HumanMedicineViewSet, basename="medicine/human")
router.register(r"medicine/orphan", OrphanMedicineViewSet, basename="medicine/orphan")
router.register(r"medicine/humanHistories", HumanHistoriesViewSet, basename="medicine/humanHistories")
router.register(r"medicine/orphanHistories", OrphanHistoriesViewSet, basename="medicine/orphanHistories")

# human orphan splits
router.register(r"structureData", HumanOrphanViewSet, basename="structureData")
router.register(r"medicine", HumanOrphanViewSet, basename="medicine")


# urlpatterns is the default way of adding routes (endpoints)
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
    path("structureData/human/", HumanMedicineInfo.as_view()),
    path("structureData/orphan/", OrphanMedicineInfo.as_view()),
    path("structureData/humanHistories/", HumanHistoryInfo.as_view()),
    path("structureData/orphanHistories/", OrphanHistoryInfo.as_view()),
]
