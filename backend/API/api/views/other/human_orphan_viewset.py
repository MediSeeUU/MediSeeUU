# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

# This file contains the view for the endpoint that
# is concerned with additional information about all
# fields in the database.
# ---------------------------------------------------------

from rest_framework import viewsets
from rest_framework.response import Response


class HumanOrphanViewSet(viewsets.ViewSet):
    """
    Viewset for the Structure views
    """

    def list(self, request):
        """
        Returns a human and orphan url of structured data

        Returns:
            httpResponse: Response with the list of filtered urls
        """
        current_url = request.build_absolute_uri()
        redirect_urls = {
            "human": current_url + "human/",
            "orphan": current_url + "orphan/",
            "human histories:": current_url + "humanHistories/",
            "orphan histories:": current_url + "orphanHistories/",
            "procedures": current_url + "procedures/"
        }
        return Response(redirect_urls)
