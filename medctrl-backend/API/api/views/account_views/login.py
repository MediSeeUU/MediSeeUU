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

# Class used for logging in a user
class LoginAPI(KnoxLoginView):
    """Login API View"""

    permission_classes = (permissions.AllowAny,)

    # For each post request on '../account/login' this method is called
    def post(self, request, _format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super().post(request, format=_format)
