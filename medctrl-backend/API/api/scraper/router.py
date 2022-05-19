from django.urls import path
from .scraperMedicine import ScraperMedicine
from .scraperProcedure import ScraperProcedure

# url patterns for the scraper endpoints
url_patterns = [
    path("medicine", ScraperMedicine.as_view(), name="medicine"),
    path("procedure", ScraperProcedure.as_view(), name="procedure"),
]
