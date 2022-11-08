# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
import requests
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.views import APIView
from knox.models import AuthToken
from django.contrib.auth import logout
from django.contrib.auth.models import User

import logging
import datetime

logger = logging.getLogger(__name__)

# class GetToken(BaseBackend):

class ScraperToken(APIView):
    """
    Generates a view for token communication between the scraper and the backend
    """
    def post(self, request):
        """
        Deletes the token for the scraper user
        Returns:
            object:
        """
    #     invoke the logout function
        self.delete_token(request)
        return Response(status=200)

    def delete_token(self, request):
        logger.info("in delete token")
        logger.info(request)
        logout(request)
        logger.info("LOGGED OUT")


    def get(self, request):
        """

        Args:
            self:
            request:

        Returns:

        """
        # Maybe change dynamically
        user_string = "scraper"
        user = User.objects.get(username=user_string)

        if user is None:
            logger.error("User " + user_string + " does not exist")
            return Response(status=403)

        duration = 1  # standard duration, make sure to delete token when communication is complete

        logger.info("user: " + str(user))
        logger.info("duration: " + str(duration))

        instance, token = AuthToken.objects.create(
            user, datetime.timedelta(days=duration)
        )

        logger.info("token: " + str(token))
        self.send_token({'token': token})

        return Response(status=200)

    def send_token(self, data):
        url = 'http://127.0.0.1:5000/token/'
        response = requests.post(url, data)
        logger.info(response)
