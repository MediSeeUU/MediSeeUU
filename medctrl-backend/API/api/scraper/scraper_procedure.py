# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

# This file can be accesed by the scraper via the procudure enpoint.
# When the scraper scrapes infromation about procudures, that data
# is posted to the procudure endpoint from where the data is 
# processed in this file. If the new data is validated, it will
# be updated in the database.
#-------------------------------------------------------------

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
                if override:
                    errors = self.add_procedure(procedure, current_procedure)

                    # Reset manually updated status
                    current_procedure.manually_updated = False
                    current_procedure.save()

                elif current_procedure:

                    # Skip this procedure if it has been manually edited
                    if current_procedure.manually_updated and not override:
                        procedure["errors"] = "Procedure already manually updated"
                        failed_procedures.append(procedure)
                        continue

                    errors = self.update_flex_procedure(procedure, current_procedure)
                    nullErrors = self.update_null_values(procedure)
                    if errors:
                        errors.extend(nullErrors)
                    else:
                        errors = nullErrors
                else:
                    errors = self.add_procedure(procedure, None)

                # if status is failed, add medicine to the failed list
                if errors and (len(errors) > 0):
                    procedure["errors"] = errors
                    failed_procedures.append(procedure)
            except Exception as e:
                procedure["errors"] = str(e)
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
            return []
        else:
            return procedure_serializer.errors

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
            return []
        return serializer.errors

    def update_null_values(self, data):
        current_procedure = (
            Procedure.objects.filter(eunumber=data.get("eunumber"))
            .filter(procedurecount=data.get("procedurecount"))
            .first()
        )

        procedure = model_to_dict(current_procedure)
        newData = {
            "eunumber": data.get("eunumber"),
            "procedurecount": data.get("procedurecount"),
        }

        for attr in procedure:
            if (getattr(current_procedure, attr) is None) and (
                not (data.get(attr) is None)
            ):
                newData[attr] = data.get(attr)

        if len(newData.keys()) > 2:
            return self.add_procedure(newData, current_procedure)


# if item does not exist in the database (model), add it with the serializer
def add_lookup(model, serializer, item):
    lookup = model.objects.filter(pk=item).first()
    if not lookup and serializer.is_valid():
        serializer.save()
