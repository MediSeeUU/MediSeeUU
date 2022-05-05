from rest_framework import permissions
from rest_framework.response import Response
#from api..serializers import UserSerializer

class MainUser(generics.RetrieveAPIView):
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = UserSerializer

  def get_object(self):
    user = self.request.user
    return user
