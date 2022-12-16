# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

# This file contains all functions for the 'urls view' endpoint.
# All data is fetched form the cache and filtered on the access level
# of the user.
# ------------------------------------------------------------------------------

from rest_framework import viewsets
from rest_framework import permissions
from api.serializers.medicine_serializers.scraper.get import UrlsSerializer
from api.models.human_models import MedicinalProduct
from rest_framework.response import Response
from django.core.cache import cache
from api.views.other import permission_filter


class UrlsViewSet(viewsets.ViewSet):
    """
    View set for the URLS in the Medicine model
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, _):
        """
        Returns a list of urls according to the access level of the user

        Returns:
            httpResponse: Response with the list of filtered urls
        """        
        cache_urls = cache.get("urls_cache")

        # if the data is not present in the cache, we just obtain the data from the database
        if not cache_urls:
            queryset = MedicinalProduct.objects.all()
            serializer = UrlsSerializer(queryset, many=True)
            cache_urls = serializer.data
            cache.set("urls_cache", cache_urls, None)

        user = self.request.user
        perms = permission_filter(user)

        # filters urls according to access level of the user
        filtered_urls = list(map(
            lambda obj: {x: y for x, y in obj.items() if x in perms}, cache_urls
        ))

        response = {}
        for urls in filtered_urls:
            eu_number = urls["eu_pnumber"]
            del urls["eu_pnumber"]
            response[eu_number] = urls

        return Response(response)
