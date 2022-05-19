from django.urls import path
from .scraper_medicine import ScraperMedicine
from .scraper_procedure import ScraperProcedure

# url patterns for the scraper endpoints
url_patterns = [
    path("medicine", ScraperMedicine.as_view(), name="medicine"),
    path("procedure", ScraperProcedure.as_view(), name="procedure"),
]
