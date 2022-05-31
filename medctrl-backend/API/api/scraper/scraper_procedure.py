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
    Class which provides an interface for the scraper
    to interact with the database for procedures.
    """

    # Permission on this endpoint when user can add procedure
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        """
        Specify queryset for DjangoModelPermissions
        """
        return Procedure.objects.all()

    def post(self, request):
        """
        post endpoint for procedures
        """
        # initialize list to return failed updates/adds, so these can be checked manually
        failed_procedures = []
        override = request.data.get("override")
        procedure_list = request.data.get("data")
        # get "procedure" key from request
        for procedure in procedure_list:
            try:
                # check if procedure already exists, procedures are
                # unique on the combination eunumber procedurecount
                current_procedure = (
                    Procedure.objects.filter(eunumber=procedure.get("eunumber"))
                    .filter(procedurecount=procedure.get("procedurecount"))
                    .first()
                )
                if override:
                    status = self.add_procedure(procedure, current_procedure)
                elif current_procedure:
                    status = self.update_flex_procedure(procedure, current_procedure)
                else:
                    status = self.add_procedure(procedure, None)

                # if status is failed, add medicine to the failed list
                if not status:
                    failed_procedures.append(procedure)
            except:
                failed_procedures.append(procedure)

        return Response(failed_procedures, status=200)

    # update flexible variables for procedure
    def update_flex_procedure(self, data, current):
        """
        update flexible variables for procedure
        """
        # initialise serializer
        procedure_serializer = ProcedureFlexVarUpdateSerializer(current, data=data)
        # if serializer is valid update procedure in the database
        if procedure_serializer.is_valid():
            procedure_serializer.save()
            return True
        else:
            return False

    # add procedure to the database
    def add_procedure(self, data, current):
        """
        add variables for procedure
        """
        # initialise serializer
        serializer = ProcedureSerializer(current, data=data)
        # add variable to lookup table
        add_lookup(
            Lookupproceduretype,
            LookupProceduretypeSerializer(None, data=data),
            data.get("proceduretype"),
        )
        # if serializer is valid, add procedure to teh database
        if serializer.is_valid():
            serializer.save()
            return True
        return False


# if item does not exist in the database (model), add it with the serializer
def add_lookup(model, serializer, item):
    lookup = model.objects.filter(pk=item).first()
    if not lookup and serializer.is_valid():
        serializer.save()
