from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response


class ScraperMedicine(APIView):
    """
    Class which provides an interface for the scraper to interact with the database.
    """

    def post(self, request, format=None):
        # get "medicine" key from request
        medicine = request.data.get("medicine")

        print(medicine)

        return Response("OK", status=200)


url_patterns = [
    path("medicine", ScraperMedicine.as_view(), name="medicine"),
]
