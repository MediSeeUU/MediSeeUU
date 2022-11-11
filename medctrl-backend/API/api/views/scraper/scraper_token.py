# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
import time

import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from knox.models import AuthToken
from django.contrib.auth import logout
from django.contrib.auth.models import User

import logging
import datetime
import threading

logger = logging.getLogger(__name__)


class ScraperToken(APIView):
    """
    Generates a view for token communication between the scraper and the backend
    """

    def post(self, request):
        """
        Deletes the token for the scraper user
        Returns:
            Response: The response object of the request
        """
        #     invoke the logout function
        self.delete_token(request)
        return Response(status=200)

    # This function is a stub
    def delete_token(self, request):
        logger.info("in delete token")
        logger.info(request)
        logout(request)
        logger.info("LOGGED OUT")

    def get(self, request):
        """
        Handles incoming get requests for a token and sends a token to the token_handler server using the
        `send_token(self, data)` function

        Args:
            request: The get request object

        Returns:
            Response: The response object of the request
        """
        # Maybe change dynamically
        user_string = "scraper"
        user = User.objects.get(username=user_string)

        if user is None:
            logger.error("User " + user_string + " does not exist")
            return Response(status=403)

        duration = 1  # standard duration, make sure to delete token when communication is complete

        instance, token = AuthToken.objects.create(
            user, datetime.timedelta(days=duration)
        )

        logger.info("token has been made for " + str(user))

        x = threading.Thread(target=self.send_token, args=({'token': token},))
        x.start()
        return Response(status=200)

    def send_token(self, data):
        """
        Receives a token and sends it to a specific url corresponding to the token_handler from the flask server

        Args:
            data (obj): The token in dict form
        """
        time.sleep(1)
        url = 'http://127.0.0.1:5000/token/'
        response = requests.post(url, data)
        if response.status_code == 200:
            logger.info("Token has been sent")
        else:
            logger.info("Token could not be send")
            logger.info(response)
