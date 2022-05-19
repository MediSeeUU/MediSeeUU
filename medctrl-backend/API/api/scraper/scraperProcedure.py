from django.core import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.decorators import permission_classes
from api.serializers.medicine_serializers import (
    ProcedureSerializer,
    ProcedureFlexVarUpdateSerializer,
    LookupProceduretypeSerializer,
)
from api.models.medicine_models import (
    Lookupproceduretype,
    Procedure,
)


class ScraperProcedure(APIView):
    """
    Class which provides an interface for the scraper to interact with the database for procedures.
    """

    # Permission on this endpoint when user can add procedure
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return Procedure.objects.all()

    def post(self, request, format=None):
        # initialize list to return failed updates/adds, so these can be checked manually
        failedProcedures = []
        for procedure in request.data:
            try:
                # check if procedure already exists, procedures are unique on the combination eunumber procedurecount
                currentProcedure = (
                    Procedure.objects.filter(eunumber=procedure.get("eunumber"))
                    .filter(procedurecount=procedure.get("procedurecount"))
                    .first()
                )
                if currentProcedure:
                    status = self.updateFlexProcedure(procedure, currentProcedure)
                else:
                    status = self.addProcedure(procedure)

                # if status is failed, add medicine to the failed list
                if not status:
                    failedProcedures.append(procedure)
            except:
                failedProcedures.append(procedure)

        return Response(failedProcedures, status=200)

    # update flexible variables for procedure
    def updateFlexProcedure(self, data, current):
        # initialise serializer
        procedureSerializer = ProcedureFlexVarUpdateSerializer(current, data=data)
        # if serializer is valid update procedure in the database
        if procedureSerializer.is_valid():
            procedureSerializer.save()
            return True
        else:
            return False

    # add procedure to the database
    def addProcedure(self, data):
        # initialise serializer
        serializer = ProcedureSerializer(None, data=data)
        # add variable to lookup table
        addLookup(
            Lookupproceduretype,
            LookupProceduretypeSerializer(None, data=data),
            data.get("proceduretype"),
        )
        # if serializer is valid, add procedure to teh database
        if serializer.is_valid():
            serializer.save()
            return True
        else:
            return False


# if item does not exist in the database (model), add it with the serializer
def addLookup(model, serializer, item):
    lookup = model.objects.filter(pk=item).first()
    if not lookup and serializer.is_valid():
        serializer.save()
