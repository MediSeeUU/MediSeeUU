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
from api.update_cache import update_cache
from django.forms.models import model_to_dict


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
                if current_procedure:
                    status = self.update_flex_procedure(procedure, current_procedure)
                    self.update_null_values(procedure)
                else:
                    status = self.add_procedure(procedure)

                # if status is failed, add medicine to the failed list
                if not status:
                    failed_procedures.append(procedure)
            except:
                failed_procedures.append(procedure)

        update_cache()
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
    def add_procedure(self, data):
        """
        add variables for procedure
        """
        # initialise serializer
        serializer = ProcedureSerializer(None, data=data)
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
    
    def update_null_values(self, data):
        current_procedure = (
                Procedure.objects.filter(eunumber=data.get("eunumber"))
                .filter(procedurecount=data.get("procedurecount"))
                .first()
            )

        procedure = model_to_dict(current_procedure)
        newData = {
            "eunumber": data.get("eunumber"),
            "procedurecount": data.get("procedurecount")
        }

        for attr in procedure:
            if (getattr(current_procedure, attr) is None) and (not (data.get(attr) is None)):
                newData[attr] = data.get(attr)
        
        if len(newData.keys()) > 2:
            self.add_procedure(newData, current_procedure)


# if item does not exist in the database (model), add it with the serializer
def add_lookup(model, serializer, item):
    lookup = model.objects.filter(pk=item).first()
    if not lookup and serializer.is_valid():
        serializer.save()
