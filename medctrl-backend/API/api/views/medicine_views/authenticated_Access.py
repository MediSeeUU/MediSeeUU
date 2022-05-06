from rest_framework import permissions, generics
from rest_framework.response import Response
from api.serializers.user_serializers import UserSerializer

class AuthenticatedUser(generics.RetrieveAPIView):
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = UserSerializer

  def get_object(self):
    user = self.request.user
    return user
