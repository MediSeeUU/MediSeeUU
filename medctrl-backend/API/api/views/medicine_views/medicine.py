from rest_framework import viewsets
from api.serializers.medicine_serializers import PublicMedicineSerializer
from api.models.medicine_models import Medicine
from rest_framework import permissions
from api.serializers.user_serializers import UserSerializer
from django.contrib.auth.models import Group
from django.core.exceptions import FieldError
from rest_framework.response import Response


class MedicineViewSet(viewsets.ReadOnlyModelViewSet):
    # Here we should make the distinction in access level --> change serializer based on access level

    permission_classes = [permissions.IsAuthenticatedOrReadOnly] #permissions.IsAuthenticated
    serializer_class = PublicMedicineSerializer

    def get_queryset(self):
        serializer_class = UserSerializer
        user = self.request.user

        queryset = Medicine.objects.all()
        
        if user.is_anonymous:
            permA = Group.objects.get(name="anonymous").permissions.all()
        else:
            permB = user.get_all_permissions(obj=None)

        if user.is_anonymous:
            perm = [str(x.codename).split('.')[1] for x in permA if "." in x.codename]
        else:
            perm = [x.split('.')[1] for x in permB if "." in x]

        try:
            filteredSet = Medicine.objects.values(*perm)
        except FieldError as e:
            #return Response({'Error': "Wrong permissions set" + (str(e).split('.')[0])})
            filteredSet = []
        except:
            filteredSet = []
            
        return filteredSet
