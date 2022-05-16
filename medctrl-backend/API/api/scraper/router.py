from django.urls import path
from django.core import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models.medicine_models import Medicine, Authorisation
from api.serializers.medicine_serializers import MedicineSerializer, AuthorisationSerializer, LookupStatusSerializer
from api.serializers.medicine_serializers import MedicineFlexVarUpdateSerializer
from api.models.medicine_models import Procedure
from api.serializers.medicine_serializers import ProcedureSerializer, AuthorisationFlexVarUpdateSerializer, ProcedureFlexVarUpdateSerializer
from api.models.medicine_models import Lookupstatus, Lookupactivesubstance, Lookupatccode, Lookuplegalbasis, Lookuplegalscope, Lookupmedicinetype, Lookuprapporteur, Lookupproceduretype
from api.serializers.medicine_serializers import LookupStatusSerializer, LookupActiveSubstanceSerializer, LookupAtccodeSerializer, LookupLegalbasisSerializer, LookupLegalscopeSerializer, LookupMedicinetypeSerializer, LookupRapporteurSerializer, LookupProceduretypeSerializer

class ScraperMedicine(APIView):
    """
    Class which provides an interface for the scraper to interact with the database.
    """

    def post(self, request, format=None):
        # get "medicine" key from request
        for medicine in request.data:
            currentMedicine = Medicine.objects.filter(pk=medicine.get("eunumber")).first()
            if currentMedicine:
                self.updateFlexMedicine(medicine, currentMedicine)
            else:
                self.addMedicine(medicine)

        return Response("OK", status=200)

    def updateFlexMedicine(self, data, current):
        currentAuthorisation = Authorisation.objects.filter(pk=data.get("eunumber")).first()
        medicineSerializer = MedicineFlexVarUpdateSerializer(current, data=data)
        authorisationSerializer = AuthorisationFlexVarUpdateSerializer(currentAuthorisation, data=data)
        addLookup(Lookupstatus, LookupStatusSerializer(None, data=data), data.get("status"))
        addLookup(Lookupatccode, LookupAtccodeSerializer(None, data=data), data.get("atccode"))
        if (medicineSerializer.is_valid() and authorisationSerializer.is_valid()):
            medicineSerializer.save()
            authorisationSerializer.save()
    
    def addMedicine(self, data):
        serializer = MedicineSerializer(None, data=data)
        authorisationSerializer = AuthorisationSerializer(None, data=data)
        addLookup(Lookupstatus, LookupStatusSerializer(None, data=data), data.get("status"))
        addLookup(Lookupactivesubstance, LookupActiveSubstanceSerializer(None, data=data), data.get("activesubstance"))
        addLookup(Lookupatccode, LookupAtccodeSerializer(None, data=data), data.get("atccode"))
        addLookup(Lookuplegalbasis, LookupLegalbasisSerializer(None, data=data), data.get("legalbasis"))
        addLookup(Lookuplegalscope, LookupLegalscopeSerializer(None, data=data), data.get("legalscope"))
        addLookup(Lookupmedicinetype, LookupMedicinetypeSerializer(None, data=data), data.get("medicinetype"))
        addLookup(Lookuprapporteur, LookupRapporteurSerializer(None, data=data), data.get("rapporteur"))
        addLookup(Lookuprapporteur, LookupRapporteurSerializer(None, data={'rapporteur': data.get("corapporteur")}), data.get("corapporteur"))
        if serializer.is_valid():
            serializer.save()
        if authorisationSerializer.is_valid():
            authorisationSerializer.save()

    

class ScraperProcedure(APIView):
    """
    Class which provides an interface for the scraper to interact with the database.
    """

    def post(self, request, format=None):
        for procedure in request.data:
            currentProcedure = Procedure.objects.filter(eunumber=procedure.get("eunumber")).filter(procedurecount=procedure.get("procedurecount")).first()
            if currentProcedure:
                self.updateFlexProcedure(procedure, currentProcedure)
            else:
                self.addProcedure(procedure)

        return Response("OK", status=200)
    
    def updateFlexProcedure(self, data, current):
        procedureSerializer = ProcedureFlexVarUpdateSerializer(current, data=data)
        addLookup(Lookupproceduretype, LookupProceduretypeSerializer(None, data=data), data.get("proceduretype"))
        if (procedureSerializer.is_valid()):
            procedureSerializer.save()

    def addProcedure(self, data):
        serializer = ProcedureSerializer(None, data=data)
        addLookup(Lookupproceduretype, LookupProceduretypeSerializer(None, data=data), data.get("proceduretype"))
        if serializer.is_valid():
            serializer.save()

def addLookup(model, serializer, item):
    lookup = model.objects.filter(pk=item).first()
    if not lookup and serializer.is_valid():
        serializer.save()

url_patterns = [
    path("medicine", ScraperMedicine.as_view(), name="medicine"),
    path("procedure", ScraperProcedure.as_view(), name="procedure")
]
