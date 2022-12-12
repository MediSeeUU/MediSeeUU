# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

# This file contains all url paths (endpoints)
# that the scraper uses for updating the database.
# --------------------------------------------------

from django.urls import path, include
from rest_framework import routers
from api.views.scraper.post.scraper_post import ScraperMedicine
from .scraper_urls_view import UrlsViewSet
from .scraper_token import ScraperToken

router = routers.DefaultRouter()
router.register(r"urls", UrlsViewSet, basename="scraped_urls")

# url patterns for the scraper endpoints
url_patterns = [
    path(r"medicine/", ScraperMedicine.as_view(), name="medicine"),
    path(r"", include(router.urls))
]
