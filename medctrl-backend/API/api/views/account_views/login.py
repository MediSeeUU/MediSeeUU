# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

# This file contains all the logic for signing in on the webpage
# It checks whether a user has valid login credentials using the knox authentication framework
# The 'login' function is a default function in the django framework used for validating
# a user and creating a token.
# ------------------------------------------------------------------

from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView


class LoginAPI(KnoxLoginView):
    """
    Class used for logging in a user, derived from the KnoxLoginView
    """    
    permission_classes = (permissions.AllowAny,)

    def post(self, request, _format=None):
        """
        This method handles the user logins. For each post request on 
        '../account/login' this method is called.

        Args:
            request (httpRequest): The login request from the user side
            _format (optional): the format for the given request. Defaults to None.

        Returns:
            httpRequest: The request has been modified based on the success of the login.
        """        
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super().post(request, format=_format)
