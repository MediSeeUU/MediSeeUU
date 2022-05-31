from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

#Checks wether a user has valid login credenials using the knox authentication framework
class LoginAPI(KnoxLoginView):
    """Login API View"""

    permission_classes = (permissions.AllowAny,)

    #For each post request on '../account/login' this method is called
    def post(self, request, _format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super().post(request, format=_format)
