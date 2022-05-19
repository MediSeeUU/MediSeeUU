from django.core import serializers
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers.medicine_serializers import (
    AuthorisationFlexVarUpdateSerializer,
    MedicineFlexVarUpdateSerializer,
    MedicineSerializer,
    AuthorisationSerializer,
    LookupStatusSerializer,
    LookupActiveSubstanceSerializer,
    LookupAtccodeSerializer,
    LookupLegalbasisSerializer,
    LookupLegalscopeSerializer,
    LookupMedicinetypeSerializer,
    LookupRapporteurSerializer,
)
from api.models.medicine_models import (
    Lookupstatus,
    Lookupactivesubstance,
    Lookupatccode,
    Lookuplegalbasis,
    Lookuplegalscope,
    Lookupmedicinetype,
    Lookuprapporteur,
    Medicine,
    Authorisation,
)


class ScraperMedicine(APIView):
    """
    Class which provides an interface for the scraper to interact with the database models medicine and authorisation.
    """

    # Permission on this endpoint when user can add medicine
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return Medicine.objects.all()

    def post(self, request, format=None):
        # initialize list to return failed updates/adds, so these can be checked manually
        failedMedicines = []
        # get "medicine" key from request
        for medicine in request.data:
            try:
                # check if medicine already exists based on eunumber
                currentMedicine = Medicine.objects.filter(
                    pk=medicine.get("eunumber")
                ).first()
                # if exists update the medicine otherwise add it, update works only on flexible variables
                if currentMedicine:
                    status = self.updateFlexMedicine(medicine, currentMedicine)
                else:
                    status = self.addMedicine(medicine)
                # if status is failed, add medicine to the failed list
                if not status:
                    failedMedicines.append(medicine)
            except:
                failedMedicines.append(medicine)

        return Response(failedMedicines, status=200)

    # update the flexible variables of medicine and authorisation
    def updateFlexMedicine(self, data, current):
        currentAuthorisation = Authorisation.objects.filter(
            pk=data.get("eunumber")
        ).first()
        medicineSerializer = MedicineFlexVarUpdateSerializer(current, data=data)
        authorisationSerializer = AuthorisationFlexVarUpdateSerializer(
            currentAuthorisation, data=data
        )
        # add variables to lookup table
        addLookup(
            Lookupstatus, LookupStatusSerializer(None, data=data), data.get("status")
        )
        addLookup(
            Lookupatccode, LookupAtccodeSerializer(None, data=data), data.get("atccode")
        )
        # if authorisation not exists, add authorisation
        if not currentAuthorisation:
            authorisationSerializer = AuthorisationSerializer(None, data=data)

        # update medicine and authorisation
        if medicineSerializer.is_valid() and authorisationSerializer.is_valid():
            medicineSerializer.save()
            authorisationSerializer.save()
            return True
        return False

    def addMedicine(self, data):
        # initialise serializers voor addition
        serializer = MedicineSerializer(None, data=data)
        authorisationSerializer = AuthorisationSerializer(None, data=data)
        # add variables to lookup table
        addLookup(
            Lookupstatus, LookupStatusSerializer(None, data=data), data.get("status")
        )
        addLookup(
            Lookupactivesubstance,
            LookupActiveSubstanceSerializer(None, data=data),
            data.get("activesubstance"),
        )
        addLookup(
            Lookupatccode, LookupAtccodeSerializer(None, data=data), data.get("atccode")
        )
        addLookup(
            Lookuplegalbasis,
            LookupLegalbasisSerializer(None, data=data),
            data.get("legalbasis"),
        )
        addLookup(
            Lookuplegalscope,
            LookupLegalscopeSerializer(None, data=data),
            data.get("legalscope"),
        )
        addLookup(
            Lookupmedicinetype,
            LookupMedicinetypeSerializer(None, data=data),
            data.get("medicinetype"),
        )
        addLookup(
            Lookuprapporteur,
            LookupRapporteurSerializer(None, data=data),
            data.get("rapporteur"),
        )
        addLookup(
            Lookuprapporteur,
            LookupRapporteurSerializer(
                None, data={"rapporteur": data.get("corapporteur")}
            ),
            data.get("corapporteur"),
        )
        # add medicine and authorisation
        if serializer.is_valid():
            serializer.save()
        else:
            return False
        if authorisationSerializer.is_valid():
            authorisationSerializer.save()
        else:
            return False
        return True
